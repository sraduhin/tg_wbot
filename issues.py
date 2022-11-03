from db import db, get_or_create_user, save_feedback
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from utils import format_issue, main_keyboard


def issue_start(update, context):
    print('issue_start')
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    context.user_data['username'] = update.message.chat.username
    context.user_data['data'] = {}
    user_issue = update.message.text
    if user_issue == 'Благодарность!':
        context.user_data['data']['type'] = 'respect'
        context.bot.send_message(chat_id=update.effective_chat.id, text='У вас есть лестные отзывы?')
        context.bot.send_message(chat_id=update.effective_chat.id, text='Их любим мы.)')
    else:
        context.user_data['data']['type'] = 'other'
        chat_id = update.effective_chat.id
        articul_pic_filename = 'images/epifanzev.png'
        context.bot.send_photo(
            chat_id=chat_id, photo=open(articul_pic_filename, 'rb')
        )
    update.message.reply_text('Для отмены, наберите /cancel')
    return 'get_description'


def ask_before_send(update, context):
    issue_content = format_issue(context.user_data)
    keyboard = [
        [InlineKeyboardButton('Отправить', callback_data='_')]
    ]
    context.bot.send_message(chat_id=update.effective_chat.id, text=issue_content,
                             reply_markup=InlineKeyboardMarkup(keyboard), 
                             parse_mode=ParseMode.HTML)
    return 'get_description'


def get_description(update, context):
    print('get_description')
    print(context.user_data['data'])
    if context.user_data['data'].get('details'):
        context.user_data['data']['details'] += f'\n{update.message.text}'
    else:
        context.user_data['data']['details'] = update.message.text
    return ask_before_send(update, context)


def end_conversation(update, context):
    print('end_conversation')
    update.callback_query.answer()
    update.callback_query.edit_message_reply_markup(reply_markup=None)
    user = get_or_create_user(
        db, update.effective_user,
        update.callback_query.message.chat.id
    )
    save_feedback(db, user['user_id'], context.user_data['data'])
    context.bot.send_message(chat_id=update.effective_chat.id, text='Спасибо, за за обратную связь!',
                             reply_markup=main_keyboard())
    return ConversationHandler.END