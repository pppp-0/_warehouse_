
import telebot
from telebot import types

TOKEN = '8070247743:AAEfDoSNT0aMyh3GVZZYQsAc5EsU_yi7Brs'

bot = telebot.TeleBot(TOKEN)

products = {
    "Кровать": {"вес": 13.6, "количество": 14},
    "Ёлка": {"вес": 8, "количество": 23},
    "Велосипед": {"вес": 8.5, "количество": 45},
    "Игрушка-пердушка": {"вес": 0.323, "количество": 120},
    "Статуэтка-слон": {"вес": 4.03, "количество": 32},
    "Вантуз": {"вес": 1.67, "количество": 56},
    "Веревка(20 метров)": {"вес": 5.6, "количество": 64},
    "Веревка(50 метров)": {"вес": 13.7, "количество": 48},
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я бот склада.\n"
        "Напишите /list — чтобы получить список товаров."
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['list'])
def list_products(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    buttons = [types.KeyboardButton(name) for name in products.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Выберите товар:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in products)
def send_product_info(message):
    name = message.text
    info = products[name]
    text = f"{name}, вес — {info['вес']} кг, количество — {info['количество']}"
    bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())

bot.polling()
