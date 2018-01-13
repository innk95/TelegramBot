import config
import telebot
from telebot import types
import os
from TriPinvgvinaFilmsApi import get_tPin_films_api
from screeshot import get_screenshot
import base64
from pprint import pprint

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['text'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Три Пингвина (Мадагаскар)', callback_data='theater1'))
    bot.send_message(message.chat.id, 'Привет! В какой кинотеатр пойдем?(правда выбор не велик)', reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def films(call):
    json_data = get_tPin_films_api()

    if call.data == 'theater1':
        k = types.InlineKeyboardMarkup()
        for elem in json_data.get('ANS'):
            data = elem['name'][:10]
            k.add(types.InlineKeyboardButton(text=elem['name'], callback_data = data ))
        bot.send_message(call.message.chat.id, 'Давай выберем фильм!', reply_markup=k)

    for elem in json_data.get('ANS'):
        if elem['name'][:10] == call.data:
            k = types.InlineKeyboardMarkup()
            for ticket in elem['tickets']:
                seance_name = ticket['time'] + ' (' + ticket['title'] +')'
                k.add(types.InlineKeyboardButton(seance_name, callback_data=ticket['id']))
            bot.send_message(call.message.chat.id, 'На какое время?', reply_markup=k)

    for elem in json_data.get('ANS'):
        for ticket in elem['tickets']:
            if ticket['id'] == call.data:
                bot.send_message(call.message.chat.id, 'Сейчас подгрузим фотку')
                url = 'https://madagascarkino.ru/ticket/cheb/sale/get?performance=' + ticket['id']
                screenshot = get_screenshot(url)
                bot.send_photo(call.message.chat.id, screenshot, caption='Ну а дальше не работает) пока что')




bot.polling()
