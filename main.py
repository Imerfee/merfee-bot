from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from flask import Flask

API_TOKEN = '7426766382:AAG-Fw82VsIKowP_c3zVEoaVQQoa_LHWXeU'  # Укажите ваш токен

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

app = Flask(__name__)

# Стартовое сообщение бота
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Выберите язык. /choose_language")

# Обработчик команды выбора языка
@dp.message_handler(commands=['choose_language'])
async def cmd_choose_language(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("English", "Русский")
    await message.answer("Выберите язык:", reply_markup=markup)

# Логика выбора языка
@dp.message_handler(lambda message: message.text in ["English", "Русский"])
async def language_choice(message: types.Message):
    if message.text == "English":
        await message.answer("You selected English.")
    elif message.text == "Русский":
        await message.answer("Вы выбрали русский.")

# Вебхук для обработки запросов (не обязательно, если вы хотите использовать поллинг)
@app.route('/' + API_TOKEN, methods=["POST"])
async def handle_webhook(request):
    json_str = await request.get_data(as_text=True)
    update = types.Update.de_json(json_str)
    await dp.process_update(update)
    return "OK", 200

if __name__ == '__main__':
    # Запуск бота
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
