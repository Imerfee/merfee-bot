import os
import telebot
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from telebot import types

# Ваш токен для бота
TOKEN = '7426766382:AAG-Fw82VsIKowP_c3zVEoaVQQoa_LHWXeU'
bot = telebot.TeleBot(TOKEN)

# Загружаем ключ из переменной окружения
SERVICE_ACCOUNT_FILE = '/etc/secrets/google_credentials.json'

# Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Авторизация для работы с Google Sheets
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

# Открытие Google Таблицы
worksheet = gc.open('1-sxuDqMpyU5R_ANEgZbtXY44HV84X3BgvUw4pL1Zg1c').sheet1

# Приветственное сообщение на разных языках
texts = {
    'en': {
        'welcome': 'Welcome to the Merfee exchange. Choose a language:',
        'choose_language': 'Choose a language:',
        'choose_currency': 'Choose a currency you want to give:',
        'exchange': 'Choose a currency you want to receive:',
        'amount': 'Enter the amount you want to exchange:',
        'confirm': 'Do you want to exchange?'
    },
    'ru': {
        'welcome': 'Добро пожаловать в обмен валют Merfee. Выберите язык:',
        'choose_language': 'Выберите язык:',
        'choose_currency': 'Выберите валюту, которую хотите отдать:',
        'exchange': 'Выберите валюту, которую хотите получить:',
        'amount': 'Введите сумму для обмена:',
        'confirm': 'Вы хотите обменять?'
    }
}

# Функция, которая отправляет сообщения пользователю
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("English"))
    markup.add(types.KeyboardButton("Русский"))
    bot.send_message(message.chat.id, texts['ru']['welcome'], reply_markup=markup)

# Обработка выбора языка
@bot.message_handler(func=lambda message: message.text in ['English', 'Русский'])
def language_choice(message):
    language = 'en' if message.text == 'English' else 'ru'
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, texts[language]['choose_currency'], reply_markup=markup)
    # Сохраняем выбранный язык для дальнейшего использования
    bot.register_next_step_handler(message, currency_choice, language)

# Функция для выбора валюты
def currency_choice(message, language):
    # Получаем список валют из Google Таблицы
    currencies = worksheet.col_values(1)  # Предположим, что валюты находятся в первом столбце
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for currency in currencies:
        markup.add(types.KeyboardButton(currency))
    bot.send_message(message.chat.id, texts[language]['choose_currency'], reply_markup=markup)
    bot.register_next_step_handler(message, exchange_choice, language)

# Функция для выбора валюты для обмена
def exchange_choice(message, language):
    currency_to_give = message.text
    bot.send_message(message.chat.id, texts[language]['amount'])
    bot.register_next_step_handler(message, amount_choice, language, currency_to_give)

# Ввод суммы
def amount_choice(message, language, currency_to_give):
    amount = message.text
    # Находим валюту, которую мы хотим получить, из Google Таблицы
    # Предположим, что у нас есть данные о валютных курсах
    row = worksheet.find(currency_to_give).row
    exchange_rate = worksheet.cell(row, 2).value  # Валютный курс во втором столбце
    amount_in_new_currency = float(amount) * float(exchange_rate)
    
    # Отправляем результат
    bot.send_message(message.chat.id, f'{texts[language]["exchange"]}: {currency_to_give} {amount} = {amount_in_new_currency} in another currency.')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(texts[language]['confirm']))
    markup.add(types.KeyboardButton("Contact Manager"))
    bot.send_message(message.chat.id, texts[language]['confirm'], reply_markup=markup)

# Отправка запроса на обмен
@bot.message_handler(func=lambda message: message.text in [texts['ru']['confirm'], 'Contact Manager'])
def process_exchange(message):
    if message.text == texts['ru']['confirm']:
        bot.send_message('your_telegram_id', 'User wants to exchange currency.')
    elif message.text == 'Contact Manager':
        bot.send_message('your_telegram_id', 'User wants to contact the manager.')

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
