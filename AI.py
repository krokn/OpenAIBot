import telebot
import webbrowser
from telebot import types

bot = telebot.TeleBot('6718573593:AAHVZng3giJHCTsO9m7ieF7qa3Z22Cghp3Y')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://www.youtube.com')
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete_photo')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='change_text')
    markup.row(btn1)
    markup.row(btn2,btn3)
    bot.reply_to(message, 'Мерзость то какая', reply_markup=markup)

@bot.message_handler(commands=['site','website'])
def main(message):
    webbrowser.open('https://www.youtube.com')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id,f"Привет! {message.from_user.first_name} {message.from_user.last_name}")


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f"Привет! {message.from_user.first_name} {message.from_user.last_name}")
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.polling(none_stop=True)