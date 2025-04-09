import telebot
from flask import Flask, request
import os

# Инициализация Flask приложения
app = Flask(__name__)

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("7426766382:AAG-Fw82VsIKowP_c3zVEoaVQQoa_LHWXeU")
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот.")

# Веб-хук для обработки сообщений
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    # Удаляем старый веб-хук и устанавливаем новый
    bot.remove_webhook()
    bot.set_webhook(url=f'https://your-service-name.onrender.com/{TOKEN}')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
