import telebot
import requests
from telebot import types

import openai

KEY = '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'
KEY_BOT = '6718573593:AAHVZng3giJHCTsO9m7ieF7qa3Z22Cghp3Y'

bot = telebot.TeleBot(KEY_BOT)

openai.api_key = KEY

selected_model = None

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет, я твой CHAT-GPT-BOT. Готов тебе помочь')

@bot.message_handler(commands=['gpt'])
def select_gpt(message):
    global selected_model
    selected_model = 'gpt'
    bot.send_message(message.chat.id, 'Вы выбрали GPT. Введите ваш запрос:')

@bot.message_handler(commands=['dalle'])
def select_dalle(message):
    global selected_model
    selected_model = 'dalle'
    bot.send_message(message.chat.id, 'Вы выбрали DALL-E. Введите путь к изображению:')

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if selected_model == 'gpt':
        generate_reply_gpt(message)
    elif selected_model == 'dalle':
        process_image_dalle(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, сначала выберите нейросеть.')

def generate_reply_gpt(message):
    user_message = message.text
    system_msg = 'You are a helpful assistant who understands data science.'
    reply = ''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_msg},
                  {"role": "user", "content": user_message}],
        max_tokens=3000,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=15
    )
    if response and response.choices:
        reply = response['choices'][0]['message']['content']
    else:
        reply = 'Ой что-то пошло не так'

    bot.send_message(message.chat.id, reply)

def process_image_dalle(message):
    user_message = message.text
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f'Bearer {KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json={"prompt": user_message}, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(result)
        if 'url' in result['data']:
            image_url = result['url']  # Получаем URL картинки из ответа
            send_image_to_telegram(image_url, message)
        else:
            bot.send_message(message.chat.id, 'Ошибка при обработке изображения: ключ "image" отсутствует в ответе')
    else:
        bot.send_message(message.chat.id, 'Ошибка при обработке изображения')

def send_image_to_telegram(image_url, message):
    telegram_api_url = f'https://api.telegram.org/bot{KEY_BOT}/sendPhoto'
    chat_id = message.chat.id

    payload = {
        'chat_id': chat_id,
        'photo': image_url
    }

    response = requests.post(telegram_api_url, data=payload)

    if response.status_code == 200:
        bot.send_message(message.chat.id, 'Картинка успешно отправлена в Telegram')
    else:
        bot.send_message(message.chat.id, 'Ошибка при отправке картинки в Telegram')

bot.polling(none_stop=True)