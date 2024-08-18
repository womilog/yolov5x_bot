import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import os
import shutil
from TerraYolo.TerraYolo import TerraYoloV5

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# возьмем переменные окружения из .env
load_dotenv()

# загружаем токен бота
TOKEN = os.environ.get("TOKEN")  # ВАЖНО !!!!!

# инициализируем класс YOLO
WORK_DIR = r'E:\python\yuu_bot'
os.makedirs(WORK_DIR, exist_ok=True)
yolov5 = TerraYoloV5(work_dir=WORK_DIR)

OBJECT_CLASSES = {
    'all': 'Все объекты',
    'person': 'Люди',
    'vehicle': 'Транспорт',
    'animal': 'Животные'
}

async def help(update, context):
    await update.message.reply_text("Это справочное сообщение")

def get_keyboard():
    keyboard = [
        [InlineKeyboardButton(text, callback_data=key) for key, text in OBJECT_CLASSES.items()]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Вызвана команда /start")
    await update.message.reply_text(
        'Выберите тип объектов для распознавания:',
        reply_markup=get_keyboard()
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    logger.info(f"Нажата кнопка с callback_data: {query.data}")
    await query.answer()

    selected_class = query.data
    context.user_data['selected_class'] = selected_class

    await query.edit_message_text(
        f'Выбрано: {OBJECT_CLASSES[selected_class]}. Теперь отправьте фото для распознавания'
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document.mime_type.startswith('image'):
        await detection(update, context, is_document=True)
    else:
        await update.message.reply_text('Пожалуйста, отправьте изображение.')

async def detection(update: Update, context: ContextTypes.DEFAULT_TYPE, is_document=False):
    logger.info("Начало функции detection")
    try:
        shutil.rmtree('images')
        shutil.rmtree(f'{WORK_DIR}/yolov5/runs')
    except Exception as e:
        logger.error(f"Ошибка при удалении директорий: {e}")

    my_message = await update.message.reply_text(
        'Мы получили от тебя фотографию. Идёт распознавание объектов...'
    )

    if is_document:
        new_file = await update.message.document.get_file()
        file_name = update.message.document.file_name
    else:
        new_file = await update.message.photo[-1].get_file()
        file_name = str(new_file.file_path).split('/')[-1]

    os.makedirs('images', exist_ok=True)
    image_path = os.path.join('images', file_name)
    await new_file.download_to_drive(image_path)

    test_dict = {
        'weights': 'yolov5x.pt',
        'source': 'images',
        'conf': 0.85
    }

    selected_class = context.user_data.get('selected_class', 'all')
    logger.info(f"Выбранный класс: {selected_class}")
    if selected_class != 'all':
        if selected_class == 'person':
            test_dict['classes'] = '0'
        elif selected_class == 'vehicle':
            test_dict['classes'] = '2 3 5 7'
        elif selected_class == 'animal':
            test_dict['classes'] = '15 16 17 18 19 20 21 22 23 24 25'

    yolov5.run(test_dict, exp_type='test')

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=my_message.message_id)

    await update.message.reply_text('Распознавание объектов завершено')
    await update.message.reply_photo(f"{WORK_DIR}/yolov5/runs/detect/exp/{file_name}")

def main():
    application = Application.builder().token(TOKEN).build()
    logger.info('Бот запущен...')

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.PHOTO, detection))
    application.add_handler(MessageHandler(filters.Document.IMAGE, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help))

    application.run_polling()

if __name__ == "__main__":
    main()