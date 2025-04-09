import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

# Ваш токен от бота Telegram
TOKEN = '7426766382:AAG-Fw82VsIKowP_c3zVEoaVQQoa_LHWXeU'  # Замените на ваш

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Приветствие и меню выбора языка
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("English")
    btn2 = types.KeyboardButton("Русский")
    btn3 = types.KeyboardButton("Deutsch")
    btn4 = types.KeyboardButton("Français")
    markup.add(btn1, btn2, btn3, btn4)
    await message.answer("Welcome to Merfee Exchange! Please choose your language:", reply_markup=markup)

# Обработка выбора языка
@dp.message_handler(lambda message: message.text in ['English', 'Русский', 'Deutsch', 'Français'])
async def choose_language(message: types.Message):
    language = message.text
    await message.answer(f'You have selected: {language}', reply_markup=types.ReplyKeyboardRemove())

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
