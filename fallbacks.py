from random import choice
from telegram.ext import ConversationHandler
from utils import main_keyboard


def cancel(update, context):
    print('cancel')
    update.message.reply_text('/cancel', reply_markup=main_keyboard())
    return ConversationHandler.END


def wtf(update, context):
    print('wtf')
    replies = ['Что?', 'Меня писал соседский ребенок, не понимаю', 'Такие буквы не знаю', 'Извините, я подвис']
    update.message.reply_text(f'{choice(replies)}. /cancel')