import os
import telebot
import json
import gs
import gsread
from google.oauth2.service_account import Credentials
from flask import Flask, request
from telebot import types

# Загрузка ключа из переменной окружения
creds = Credentials.from_service_account_info(
    json.loads(os.getenv('GOOGLE_API_CREDENTIALS')),
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

# Подключение к Google Таблицам
client = gsread.authorize(creds)
sheet = client.open_by_key('1-sxuDqMpyU5R_ANEgZbtXY44HV84X3BgvUw4pL1Zg1c').sheet1

# Создание бота
TOKEN = '7426766382:AAG-Fw82VsIKowP_c3ZvEoaVQQoa_LHwXeU'
bot = telebot.TeleBot(TOKEN)

# Приветственное сообщение на разных языках
texts = {
    'en': {
        'welcome': 'Welcome to Merfee Exchange! Please choose your language:',
        'choose_language': 'Please choose a language:',
        'choose_currency': 'Please choose the currency you want to buy:',
    },
    'ru': {
        'welcome': 'Добро пожаловать в Merfee! Выберите, что хотите обменять.',
        'choose_language': 'Выберите язык:',
        'choose_currency': 'Выберите валюту для покупки:',
    },
    # Добавьте другие языки, если нужно
}

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lang in texts['en']['languages']:  # Получить список языков из текстов
        markup.add(types.KeyboardButton(lang))
    bot.send_message(message.chat.id, texts['en']['choose_language'], reply_markup=markup)

# Обработка выбора языка
@bot.message_handler(func=lambda message: message.text in ['English', 'Русский', 'Deutsch', 'Français'])
def set_language(message):
    user_lang = message.text
    bot.send_message(message.chat.id, texts[user_lang]['welcome'])

# Обработка выбора валюты
@bot.message_handler(func=lambda message: message.text in ['USD', 'EUR', 'BTC', 'ETH'])
def choose_currency(message):
    currency = message.text
    bot.send_message(message.chat.id, texts[user_lang]['choose_currency'])

# Обработка входящих обновлений от Telegram
@bot.route('/' + TOKEN, methods=["POST"])
def handle_webhook(request):
    json_str = request.get_data(as_text=True)  # Получаем данные из запроса
    update = telebot.types.Update.de_json(json_str)  # Преобразуем данные в формат для telebot
    bot.process_new_updates([update])  # Обрабатываем обновление
    return "OK", 200  # Отправляем успешный ответ на запрос

# Запуск приложения Flask (вебхук)
app = Flask(__name__)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
