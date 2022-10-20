from itertools import chain
from math import prod
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def issue_start(update, context):
    print('issue_start')
    update.message.reply_text('Печаль...', reply_markup=ReplyKeyboardRemove())
    reply_keyboard = [
        ['Мягкая коробка', 'Жесткая коробка'],
        ['Полужесткая белая', 'Полужесткая серая']
    ]
    update.message.reply_text('Выберете товар, по которому хотите оставить обращение',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return 'issue_type'

def issue_type(update, context):
    product_type = update.message.text
    print('product_type=', product_type)
    reply_keyboard = [['Товар с браком'], ['Товар не соответствует заказу'], ['Другое']]
    update.message.reply_text('Укажите, что не так с товаром',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return 'issue_details'


def issue_details(update, context):
    product_problem = update.message.text
    print('product_problem=', product_problem)
    update.message.reply_text('Спасибо! Можете добавить чуть больше деталей, добавить фото или пропустить этот шаг введя /skip')


