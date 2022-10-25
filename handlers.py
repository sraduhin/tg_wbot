from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils import main_keyboard
from db import db, get_or_create_user, get_problems


def admin(update, context):
    print('admin')
    user = get_or_create_user(
        db, update.effective_user,
        update.message.chat.id
    )
    print(user)
    if user.get('admin') is True:
        request = get_problems(db)
        keyboard = [
            [InlineKeyboardButton(f"{issue['username']}\n{issue['problem'].get('problem_kind')}", callback_data='_')] for issue in request
        ]
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Привет {user['first_name']}! У тебя активные обращения",
            reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('images/not_admin.jpg', 'rb'))

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
