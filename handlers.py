from utils import main_keyboard, submit_inline_keyboard
from db import db, get_or_create_user


def greet_user(update, context):
    user = get_or_create_user(
        db, update.effective_user,
        update.message.chat.id
    )
    update.message.reply_text('Добрый день! Выберете интересующий вас вопрос!', reply_markup=main_keyboard())


def talk_to_me(update, context):
    text = update.message.text
    text = f'{(text).capitalize()}'
    update.message.reply_text(text, reply_markup=main_keyboard())


def simple_handler(update, context):
    chat_id = update.effective_chat.id
    articul_pic_filename = 'images/help_to_find_articul.jpg'
    context.bot.send_photo(
        chat_id=chat_id, photo=open(articul_pic_filename, 'rb'), reply_markup=submit_inline_keyboard()
    )

def submit_submit(update, context):
    print('submit_submit')
    update.callback_query.answer()
    print(update)
    text = f"Спасибо, за ваше обращение! Nice {update.callback_query.data}"
    update.callback_query.edit_message_caption(caption=text)