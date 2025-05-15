# bot.py
import telebot
from telebot import types

API_TOKEN = '7901057707:AAGJAUaFb4y0lQU-QHEsF9JVNiQq07IjxHA'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_info = types.WebAppInfo("https://vlobolochkov.github.io/telegram-mini-app-planner/")
    btn = types.KeyboardButton("Открыть планировщик", web_app=web_app_info)
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в семейный планировщик!\nНажмите кнопку ниже, чтобы открыть приложение:",
        reply_markup=markup
    )

# Запуск бота
bot.infinity_polling()
