from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os


# возьмем переменные окружения из .env
load_dotenv()

# загружаем токен бота
TOKEN =  os.environ.get("УКАЖИТЕ ВАШ ТОКЕН ИЗ .env") # ВАЖНО !!!!!


'''
    Примеры работы с разными типами сообщений: текст, изображения, голосовые сообщения.
'''


# функция команды /start
async def start(update, context):
    await update.message.reply_text('Привет! Этот бот предназначен для демонстрации работы обработчиков сообщений.')

# функция для текстовых сообщений
async def text(update, context):
    await update.message.reply_text(update.message.text.upper())

# функция для изображений
async def image(update, context):
    await update.message.reply_text('Эй! Мы получили от тебя фотографию!')

# функция для голосовых сообщений
async def voice(update, context):
    await update.message.reply_text('Голосовое сообщение получено!')


def main():

    # точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик сообщений с изображениями
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()


if __name__ == "__main__":
    main()