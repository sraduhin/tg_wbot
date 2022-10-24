import os
from utils import main_keyboard
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


def submit_submit(update, context):
    update.callback_query.answer()
    text = f"Спасибо, за ваше обращение! {update.callback_query.data}"
    update.callback_query.edit_message_caption(caption=text)


def get_user_photo(update, context):
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Фото сохранено')
    return file_name
