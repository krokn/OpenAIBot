import telebot

bot = telebot.TeleBot('6718573593:AAHVZng3giJHCTsO9m7ieF7qa3Z22Cghp3Y')



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