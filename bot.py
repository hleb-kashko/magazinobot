import json
import os

import telebot
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

API_TOKEN = os.getenv('API_TOKEN')
items_json = 'items.json'

storage = StateMemoryStorage()
bot = telebot.TeleBot(API_TOKEN, state_storage=storage)


class States(StatesGroup):
    add_item = State()
    shop = State()


keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton('Добавить товар', callback_data='add_item'),
    InlineKeyboardButton('Я в магазине', callback_data='shop')
]])


@bot.message_handler(state="*", commands=['start'])
def send_welcome(message: Message):
    bot.send_message(chat_id=message.chat.id,
                     text=f'Дарова, {message.from_user.first_name}! '
                     f'Ты в магазе или желаешь дополнить список покупок?',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == 'add_item')
def ask_item(callback: CallbackQuery):
    bot.set_state(callback.from_user.id, States.add_item)
    bot.send_message(callback.message.chat.id, 'Чаво выторговать надобно?')


@bot.message_handler(state=States.add_item)
def add_item(message: Message):
    item = {"name": message.text}
    with open(items_json) as f:
        items = json.load(f)
    items['items'].append(item)
    with open(items_json, 'w') as f:
        json.dump(items, f, indent=4)
    bot.delete_state(message.from_user.id)
    bot.send_message(
        chat_id=message.from_user.id,
        text=
        f"Товар {item['name']} успешно добавлен. Что хочешь сделать дальше?",
        reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == 'shop')
def shop(callback: CallbackQuery):
    bot.send_message(callback.message.chat.id, 'dgdfhd')


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling()
