import telebot
import requests
from telebot import types
import time
import queue

request_queue = queue.Queue(maxsize=3)

import openai

KEY = 'API_KEY'
KEY_BOT = 'BOT_KEY'
last_request_time = 0
bot = telebot.TeleBot(KEY_BOT)

openai.api_key = KEY
selected_model = None

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет, я твой универсальный бот. Готов тебе помочь \nВ этом чат-боте вы можете пользоваться следующими командами: \n /dalle - позволяет использовать chat-gpt-3.5-turbo \n /gpt - позволяет использовать DALL·E \n /help - позволяет посмотреть все команды доступные в этом боте')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'В этом чат-боте вы можете пользоваться следующими командами: \n /dalle - позволяет использовать chat-gpt-3.5-turbo \n /gpt - позволяет использовать DALL·E \n /help - позволяет посмотреть все команды доступные в этом боте')


@bot.message_handler(commands=['gpt'])
def select_gpt(message):
    global selected_model
    current_time = time.time()

    if request_queue.full():
        bot.send_message(message.chat.id, 'Слишком много запросов. Пожалуйста, подождите.')
        return

    request_queue.put(current_time)
    selected_model = 'gpt'
    bot.send_message(message.chat.id, 'Вы выбрали GPT. Введите ваш запрос:')

@bot.message_handler(commands=['dalle'])
def select_dalle(message):
    global selected_model
    selected_model = 'dalle'
    bot.send_message(message.chat.id, 'Вы выбрали DALL-E. Введите ваш запрос:')
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
        if 'data' in result:
            data_list = result['data']
            if len(data_list) > 0:
                first_data = data_list[0]
                if 'url' in first_data:
                    image_url = first_data['url']
                else:
                    print('Ошибка: ключ "url" отсутствует во вложенном объекте')
            else:
                print('Ошибка: список "data" пуст')
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

bot.polling(none_stop=True)