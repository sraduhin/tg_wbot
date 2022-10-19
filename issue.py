from itertools import chain
from telegram import ReplyKeyboardMarkup


def issue_start(update, context):
    update.message.reply_text('Печаль...')
    return 'issue_make_choice'


def issue_make_choice(update, context):
    print('choice called')
    reply_keyboard = [
        ['Мягкая коробка', 'Жесткая коробка'],
        ['Полужесткая белая', 'Полужесткая серая']
    ]
    update.message.reply_text('Выберете товар, по которому хотите оставить обращение',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    choice = update.message.text
    print(choice)
    if not choice in chain(*reply_keyboard):
        return 'issue_make_choice'
    return 'issue_type'


def issue_type(update, context):
    print('next step')
    issue_type = update.message.text