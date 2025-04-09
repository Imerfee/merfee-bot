import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import json

# Ваш токен бота
TOKEN = "7426766382:AAG-Fw82VsIKowP_c3zVEoaVQQoa_LHWXeU"
bot = telebot.TeleBot(TOKEN)

# Подключение к Google Таблицам
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path_to_your_credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1-sxuDqMpyU5R_ANEgZbtXY44HV84X3BgvUw4pL1Zg1c').sheet1

# Приветственное сообщение и выбор языка
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("English"), KeyboardButton("Русский"), KeyboardButton("Deutsch"), KeyboardButton("Français"))
    bot.send_message(message.chat.id, "Welcome to Merfee Bot! Please choose your language.", reply_markup=markup)

# Обработка выбора языка
@bot.message_handler(func=lambda message: message.text in ['English', 'Русский', 'Deutsch', 'Français'])
def set_language(message):
    user_lang = message.text
    # Сохраняем выбор языка в базе данных или в памяти (для простоты можно хранить в dict)
    bot.send_message(message.chat.id, "Please choose the currency you want to buy.")
    # Добавить логику для отображения выбора валюты.

# Функция для выбора валюты и расчёта курса
@bot.message_handler(func=lambda message: message.text == "Choose currency")
def choose_currency(message):
    # Запросим курс для выбранных валют
    rates = sheet.get_all_records()  # Получаем все записи из таблицы
    for rate in rates:
        # Пример: rate['BTC'] — это колонка с курсом для BTC
        # Вычислим, сколько клиент получит за его сумму, используя формулы на основе данных из таблицы.
        pass

# Заключительный шаг — кнопка для отправки заявки в ЛС
@bot.message_handler(func=lambda message: message.text == "Exchange")
def send_request_to_user(message):
    bot.send_message("@imerfee", f"New exchange request: {message.text}")

bot.polling()
