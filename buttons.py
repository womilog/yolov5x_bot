from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
import os



'''Этот скрипт создает бота для Telegram, 
   который может отправлять сообщения с различными типами клавиатур (inline и reply), 
   обрабатывать нажатия на кнопки и текстовые сообщения. '''





# возьмем переменные окружения из .env
load_dotenv()

# загружаем токен бота
TOKEN =  os.environ.get("УКАЖИТЕ ВАШ ТОКЕН ИЗ .env") # ВАЖНО !!!!!


# функция команды /start
async def start(update, context):

    # создаем список Inline кнопок
    keyboard = [[InlineKeyboardButton("Кнопка 1", callback_data="1"),
                InlineKeyboardButton("Кнопка 2", callback_data="2"),
                InlineKeyboardButton("Кнопка 3", callback_data="3")]]
    
    # создаем Inline клавиатуру
    reply_markup = InlineKeyboardMarkup(keyboard)

    # прикрепляем клавиатуру к сообщению
    await update.message.reply_text('Пример Inline кнопок', reply_markup=reply_markup)


# функция обработки нажатия на кнопки Inline клавиатуры
async def button(update, context):

    # параметры входящего запроса при нажатии на кнопку
    query = update.callback_query
    print(query)

    # отправка всплывающего уведомления
    await query.answer('Всплывающее уведомление!')
    
    # редактирование сообщения
    await query.edit_message_text(text=f"Вы нажали на кнопку: {query.data}")


# функция команды /help
async def help(update, context):

    # создаем список кнопок
    keyboard = [["Кнопка 1","Кнопка 2"]]

    # создаем Reply клавиатуру
    reply_markup = ReplyKeyboardMarkup(keyboard, 
                                       resize_keyboard=True, 
                                       one_time_keyboard=True)

    # выводим клавиатуру с сообщением
    await update.message.reply_text('Пример Reply кнопок', reply_markup=reply_markup)


# функция для текстовых сообщений
async def text(update, context):
    await update.message.reply_text('Текстовое сообщение получено', reply_markup=ReplyKeyboardRemove())


def main():

    # точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик нажатия Inline кнопок
    application.add_handler(CallbackQueryHandler(button))

    # добавляем обработчик команды /help
    application.add_handler(CommandHandler("help", help))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()


if __name__ == "__main__":
    main()