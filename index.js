require('dotenv').config(); // Для загрузки переменных окружения
const { Telegraf } = require('telegraf');

// Получаем токен бота из переменной окружения
const bot = new Telegraf(process.env.BOT_TOKEN);

// Приветственное сообщение при старте
bot.start((ctx) => {
  ctx.reply('Привет! Я готов к обмену валют. Напиши /help для справки.');
});

// Справка о боте
bot.help((ctx) => {
  ctx.reply('Этот бот поможет вам обменять валюту. Просто выберите нужные валюты.');
});

// Запуск бота
bot.launch();
