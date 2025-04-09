import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7426766382:AAG-Fw82VsIKowP_c3zVEoaVQQoa_LHWXeU"
bot = telebot.TeleBot(TOKEN)

# Временное хранилище выбора языка
user_lang = {}

# Тексты по языкам
texts = {
    'ru': {
        'welcome': "Добро пожаловать в Merfee! Выберите, что хотите обменять.",
        'language_selected': "Язык установлен: Русский",
        'choose_language': "Пожалуйста, выберите язык:",
        'languages': ["🇬🇧 English", "🇷🇺 Русский", "🇩🇪 Deutsch", "🇫🇷 Français"]
    },
    'en': {
        'welcome': "Welcome to Merfee! Please choose what you want to exchange.",
        'language_selected': "Language set: English",
        'choose_language': "Please choose your language:",
        'languages': ["🇬🇧 English", "🇷🇺 Russian", "🇩🇪 German", "🇫🇷 French"]
    },
    'de': {
        'welcome': "Willkommen bei Merfee! Wählen Sie, was Sie tauschen möchten.",
        'language_selected': "Sprache eingestellt: Deutsch",
        'choose_language': "Bitte wählen Sie eine Sprache:",
        'languages': ["🇬🇧 Englisch", "🇷🇺 Russisch", "🇩🇪 Deutsch", "🇫🇷 Französisch"]
    },
    'fr': {
        'welcome': "Bienvenue sur Merfee ! Veuillez choisir ce que vous souhaitez échanger.",
        'language_selected': "Langue définie : Français",
        'choose_language': "Veuillez choisir une langue :",
        'languages': ["🇬🇧 Anglais", "🇷🇺 Russe", "🇩🇪 Allemand", "🇫🇷 Français"]
    }
}

# Соответствие флага и кода языка
flag_to_lang = {
    "🇷🇺 Русский": 'ru',
    "🇬🇧 English": 'en',
    "🇩🇪 Deutsch": 'de',
    "🇫🇷 Français": 'fr',
    # для DE/FR с другими подписями:
    "🇷🇺 Russian": 'ru',
    "🇬🇧 Englisch": 'en',
    "🇫🇷 French": 'fr',
    "🇩🇪 German": 'de',
    "🇬🇧 Anglais": 'en',
    "🇷🇺 Russe": 'ru',
    "🇩🇪 Allemand": 'de',
    "🇫🇷 Français": 'fr'
}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for lang in texts['en']['languages']:
        markup.add(KeyboardButton(lang))
    bot.send_message(user_id, texts['en']['choose_language'], reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in flag_to_lang.keys())
def set_language(message):
    user_id = message.chat.id
    lang_code = flag_to_lang[message.text]
    user_lang[user_id] = lang_code
    bot.send_message(user_id, texts[lang_code]['language_selected'])
    bot.send_message(user_id, texts[lang_code]['welcome'])

bot.polling()
