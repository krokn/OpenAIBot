import telebot
import webbrowser
from telebot import types

import os

import openai
KEY = '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'
bot = telebot.TeleBot('6718573593:AAHVZng3giJHCTsO9m7ieF7qa3Z22Cghp3Y')

openai.api_key = KEY
@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id,'Привет, я твой CHAT-GPT-BOT. Готов тебе помочь')

@bot.message_handler(content_types=['text'])
def main(message):
    user_message = message.text
    system_msg = 'You are a helpful assistant who understands data science.'
    reply = ''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_msg},
                  {"role": "user", "content": user_message}],
        max_tokens=200,
        temperature=0.3,
        n=1,
        stop=None,
        timeout=15
    )
    if response and response.choices:
        reply = response['choices'][0]['message']['content']
    else:
        reply = 'Ой что то не так'

    bot.send_message(message.chat.id, reply)

bot.polling(none_stop=True)
