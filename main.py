import os
import telebot
from telebot import types
import gspread
from google.oauth2.service_account import Credentials
import json

# Загрузка ключа из переменной окружения
creds = Credentials.from_service_account_info(
    json.loads(os.getenv('GOOGLE_API_CREDENTIALS')), 
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

# Подключение к Google Таблицам
client = gspread.authorize(creds)
sheet = client.open_by_key('1-sxuDqMpyU5R_ANEgZbtXY44HV84X3BgvUw4pL1Zg1c').sheet1

# Создание бота
TOKEN = '7426766382:AAG-Fw82VsIKowP_c3zVEoaVQQoa_LHWXeU'
bot = telebot.TeleBot(TOKEN)

# Приветственное сообщение на разных языках
texts = {
    'en': {
        'welcome': 'Welcome to Merfee Exchange! Please choose your language:',
        'choose_language': 'Please choose a language:',
        'choose_currency': 'Please choose the currency you want to buy:',
        'choose_sell_currency': 'Please choose the currency you want to sell:',
        'enter_amount': 'Enter the amount you wish to exchange',
    },
    'ru': {
        'welcome': 'Добро пожаловать в Merfee! Выберите язык:',
        'choose_language': 'Выберите язык:',
        'choose_currency': 'Выберите валюту, которую хотите купить:',
        'choose_sell_currency': 'Выберите валюту, которую хотите продать:',
        'enter_amount': 'Введите сумму, которую хотите обменять',
    },
    'de': {
        'welcome': 'Willkommen bei Merfee! Bitte wählen Sie Ihre Sprache:',
        'choose_language': 'Wählen Sie eine Sprache:',
        'choose_currency': 'Bitte wählen Sie die Währung, die Sie kaufen möchten:',
        'choose_sell_currency': 'Bitte wählen Sie die Währung, die Sie verkaufen möchten:',
        'enter_amount': 'Geben Sie den Betrag ein, den Sie tauschen möchten',
    },
    'fr': {
        'welcome': 'Bienvenue sur Merfee! Veuillez choisir votre langue:',
        'choose_language': 'Veuillez choisir une langue:',
        'choose_currency': 'Veuillez choisir la monnaie que vous souhaitez acheter:',
        'choose_sell_currency': 'Veuillez choisir la monnaie que vous souhaitez vendre:',
        'enter_amount': 'Entrez le montant que vous souhaitez échanger',
    }
}

# Словарь для хранения выбранного языка пользователя
user_lang = {}

# Функция для отправки сообщения о выборе языка
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lang in texts['en']['choose_language']:
        markup.add(types.KeyboardButton(lang))
    bot.send_message(message.chat.id, texts[user_lang.get(message.chat.id, 'en')]['choose_language'], reply_markup=markup)

# Функция для обработки выбора языка
@bot.message_handler(func=lambda message: message.text in ['English', 'Русский', 'Deutsch', 'Français'])
def set_language(message):
    user_lang[message.chat.id] = message.text.lower()  # Сохраняем выбранный язык
    bot.send_message(message.chat.id, texts[user_lang[message.chat.id]]['choose_currency'])
    choose_currency(message)

# Функция для выбора валюты
def choose_currency(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    currencies = ["USD", "EUR", "BTC", "ETH", "UAH", "CHF"]  # Добавьте валюты из вашего списка
    for currency in currencies:
        markup.add(types.KeyboardButton(currency))
    bot.send_message(message.chat.id, texts[user_lang[message.chat.id]]['choose_currency'], reply_markup=markup)

# Функция для выбора валюты продажи
@bot.message_handler(func=lambda message: message.text in ["USD", "EUR", "BTC", "ETH", "UAH", "CHF"])  # Убедитесь, что это валидные валюты
def choose_sell_currency(message):
    user_lang[message.chat.id] = message.text  # Сохраняем валюту
    bot.send_message(message.chat.id, texts[user_lang[message.chat.id]]['choose_sell_currency'])

# Функция для получения суммы и расчёта
@bot.message_handler(func=lambda message: message.text.isdigit())  # Если введена сумма
def enter_amount(message):
    amount = int(message.text)
    # Получение курса валют из Google таблицы
    rate = sheet.cell(1, 2).value  # Пример: курс из таблицы
    result = amount * float(rate)
    bot.send_message(message.chat.id, f'You will receive: {result} in selected currency')

# Функция для отправки заявки в ЛС
@bot.message_handler(func=lambda message: message.text == "Exchange")
def process_exchange(message):
    bot.send_message('@imerfee', f'User {message.chat.id} has requested an exchange: {message.text}')  # Отправка в ЛС

# Запуск бота
bot.polling()
