# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from langdetect import detect
import apiai
import json

ADMIN_TOKEN = "416682801:AAHygzvxHclVevhrwIufoUuNCAgJueh2GpI"
CLIENT_DIALOGFLOW_TOKEN = "2888676629bc4ea3b2ac1733420fe92e"


updater = Updater(token=ADMIN_TOKEN)  # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hey!')


def text_message(bot, update):
    request = apiai.ApiAI(CLIENT_DIALOGFLOW_TOKEN).text_request()  # Токен API к Dialogflow

    message_text = update.message.text

    request.lang = detect(message_text)  # На каком языке будет послан запрос
    request.session_id = 'GoodyBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)

    request.query = message_text  # Посылаем запрос к ИИ с сообщением от юзера

    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ

    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Did not catch that :(')


# Хендлеры
start_command_handler = CommandHandler('start', start_command)
text_message_handler = MessageHandler(Filters.text, text_message)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# Начинаем поиск обновлений
updater.start_polling(clean=True)
