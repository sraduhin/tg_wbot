import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from settings import API_KEY

logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    print('/start called')
    my_keyboard = ReplyKeyboardMarkup([['Где найти артикул?']])
    update.message.reply_text('Добрый день!', reply_markup=my_keyboard)


def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


def send_articul_example(update, context):
    chat_id = update.effective_chat.id
    articul_pic_filename = 'images/find_articul.png'
    context.bot.send_photo(chat_id=chat_id, photo=open(articul_pic_filename, 'rb'))
    


def main():
    mybot = Updater(API_KEY,
                    use_context=True)
    db = mybot.dispatcher
    db.add_handler(CommandHandler('start', greet_user))
    db.add_handler(CommandHandler('articul', send_articul_example))
    db.add_handler(MessageHandler(Filters.regex('^(Где найти артикул\?)$'), send_articul_example))
    db.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('bot has been started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()