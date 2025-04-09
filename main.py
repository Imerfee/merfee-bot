import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = "7426766382:AAG-Fw82VsIKowP_c3zVEoaVQQoa_LHWXeU"
bot = telebot.TeleBot(TOKEN)

# Временное хранилище для хранения выбранного языка
user_lang = {}

# Тексты по языкам
texts = {
    'ru': {
        'welcome': "Добро пожаловать в Merfee! Выберите валюту, которую хотите обменять.",
        'language_selected': "Язык установлен: Русский",
        'choose_language': "Пожалуйста, выберите язык:",
        'languages': ["🇬🇧 English", "🇷🇺 Русский", "🇩🇪 Deutsch", "🇫🇷 Français"],
        'choose_currency': "Пожалуйста, выберите валюту, которую хотите купить:",
        'choose_sell_currency': "Теперь выберите валюту, которую хотите продать:",
        'enter_amount': "Введите сумму для обмена:"
    },
    'en': {
        'welcome': "Welcome to Merfee! Please choose the currency you want to exchange.",
        'language_selected': "Language set: English",
        'choose_language': "Please choose your language:",
        'languages': ["🇬🇧 English", "🇷🇺 Russian", "🇩🇪 German", "🇫🇷 French"],
        'choose_currency': "Please choose the currency you want to buy:",
        'choose_sell_currency': "Now, choose the currency you want to sell:",
        'enter_amount': "Enter the amount you want to exchange:"
    },
    'de': {
        'welcome': "Willkommen bei Merfee! Wählen Sie, was Sie tauschen möchten.",
        'language_selected': "Sprache eingestellt: Deutsch",
        'choose_language': "Bitte wählen Sie eine Sprache:",
        'languages': ["🇬🇧 Englisch", "🇷🇺 Russisch", "🇩🇪 Deutsch", "🇫🇷 Französisch"],
        'choose_currency': "Bitte wählen Sie die Währung, die Sie kaufen möchten:",
        'choose_sell_currency': "Wählen Sie nun die Währung, die Sie verkaufen möchten:",
        'enter_amount': "Geben Sie den Betrag ein, den Sie tauschen möchten:"
    },
    'fr': {
        'welcome': "Bienvenue sur Merfee ! Veuillez choisir ce que vous souhaitez échanger.",
        'language_selected': "Langue définie : Français",
        'choose_language': "Veuillez choisir une langue :",
        'languages': ["🇬🇧 Anglais", "🇷🇺 Russe", "🇩🇪 Allemand", "🇫🇷 Français"],
        'choose_currency': "Veuillez choisir la monnaie que vous souhaitez acheter :",
        'choose_sell_currency': "Choisissez maintenant la monnaie que vous souhaitez vendre :",
        'enter_amount': "Entrez le montant que vous souhaitez échanger :"
    }
}

import os
from google.oauth2.service_account import Credentials
import json

# Загружаем ключ из переменной окружения
creds = Credentials.from_service_account_info(
    json.loads(os.getenv('GOOGLE_API_CREDENTIALS')),  # Чтение ключа из переменной окружения
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

# Подключение к Google Таблицам
import gspread
client = gspread.authorize(creds)
sheet = client.open_by_key('your_spreadsheet_key').sheet1
# Приветственное сообщение и выбор языка
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for lang in texts['en']['languages']:
        markup.add(KeyboardButton(lang))
    bot.send_message(message.chat.id, texts['en']['choose_language'], reply_markup=markup)

# Обработка выбора языка
@bot.message_handler(func=lambda message: message.text in ['English', 'Русский', 'Deutsch', 'Français'])
def set_language(message):
    user_lang[message.chat.id] = message.text
    bot.send_message(message.chat.id, texts[user_lang[message.chat.id]]['language_selected'])
    bot.send_message(message.chat.id, texts[user_lang[message.chat.id]]['welcome'])

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("USDT"), KeyboardButton("BTC"), KeyboardButton("ETH"))
    markup.add(KeyboardButton("UAH"), KeyboardButton("CHF"))
    bot.send_message(message.chat.id, texts[user_lang[message.chat.id]]['choose_currency'], reply_markup=markup)

# Обработка выбора валюты для покупки
@bot.message_handler(func=lambda message: message.text in ['USDT', 'BTC', 'ETH', 'UAH', 'CHF'])
def choose_currency_to_sell(message):
    user_id = message.chat.id
    bot.send_message(user_id, texts[user_lang[user_id]]['choose_sell_currency'])

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("USDT"), KeyboardButton("BTC"), KeyboardButton("ETH"))
    markup.add(KeyboardButton("UAH"), KeyboardButton("CHF"))
    bot.send_message(user_id, texts[user_lang[user_id]]['choose_sell_currency'], reply_markup=markup)

# Запрос суммы для обмена
@bot.message_handler(func=lambda message: message.text in ['USDT', 'BTC', 'ETH', 'UAH', 'CHF'])
def request_amount(message):
    user_id = message.chat.id
    bot.send_message(user_id, texts[user_lang[user_id]]['enter_amount'])

# Обработка обмена
@bot.message_handler(func=lambda message: message.text == 'Обменять')
def send_request_to_user(message):
    bot.send_message("@imerfee", f"Заявка на обмен от @{message.chat.username}: {message.text}")
    bot.send_message(message.chat.id, "Заявка отправлена!")

bot.polling()
