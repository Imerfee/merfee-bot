import os
import telebot
import json
from flask import Flask, request
from google.oauth2.service_account import Credentials
import gspread

# Загрузка ключа из переменной окружения
creds = Credentials.from_service_account_info(
    json.loads(os.getenv('GOOGLE_API_CREDENTIALS')),
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

# Подключение к Google Таблицам
client = gspread.authorize(creds)
sheet = client.open_by_key('1-sxuDqMpyU5R_ANEgZbtXY44HV84X3BgvUw4pL1Zg1c').sheet1

# Создание бота
TOKEN = '7426766382:AAG-Fw82VsIKowP_c3ZvEoaVQQoa_LHwXeU'
bot = telebot.TeleBot(TOKEN)

# Приветственное сообщение на разных языках
texts = {
    'en': {
        'welcome': 'Welcome to Merfee Exchange! Please choose your language:',
        'choose_language': 'Please choose a language:',
        'choose_currency': 'Please choose the currency you want to buy:'
    },
    'ru': {
        'welcome': 'Добро пожаловать в Merfee! Выберите язык:',
        'choose_language': 'Выберите язык:',
        'choose_currency': 'Выберите валюту, которую хотите купить:'
    }
}

# Инициализация Flask
app = Flask(__name__)

@app.route('/' + TOKEN, methods=["POST"])
def handle_webhook():
    json_str = request.get_data(as_text=True)  # Получаем данные из запроса
    update = telebot.types.Update.de_json(json_str)  # Преобразуем данные в формат для telebot
    bot.process_new_updates([update])  # Обрабатываем обновление
    return "OK", 200  # Отправляем успешный ответ на запрос

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lang in texts['en']['choose_language']:
        markup.add(telebot.types.KeyboardButton(lang))
    bot.send_message(message.chat.id, texts['en']['welcome'], reply_markup=markup)

# Запуск Flask сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
