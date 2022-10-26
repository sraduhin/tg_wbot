from bson import ObjectId
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from utils import format_feedback, main_keyboard, get_feedback_type
from db import db, get_or_create_user


def admin(update, context):
    print('admin')
    user = get_or_create_user(
        db, update.effective_user,
        update.message.chat.id
    )
    print(user)
    if user.get('admin') is True:
        request = db.feedbacks.find({'status_open': True})
        request = get_feedback_type(request)
        keyboard = [
            [
                InlineKeyboardButton(
                    f"@{feedback['username']} {feedback['description']}",
                    callback_data=f"admin_request|{feedback['_id']}"
                )
            ] for feedback in request
        ]
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Привет {user['first_name']}! У тебя активные обращения",
            reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('images/not_admin.jpg', 'rb'))


def show_feedback(update, context):
    answer = update.callback_query.data
    answer = answer.split('|')[-1]
    feedback = db.feedbacks.find_one({"_id": ObjectId(answer)})
    photos = feedback['feedback'].get('photos')
    feedback = format_feedback(feedback)
    context.bot.send_message(chat_id=update.effective_chat.id, text=feedback,
                             parse_mode=ParseMode.HTML)
    if photos:
        for photo in photos:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photo, 'rb'))


def greet_user(update, context):
    user = get_or_create_user(
        db, update.effective_user,
        update.message.chat.id
    )
    update.message.reply_text('Добрый день! Выберете интересующий вас вопрос!', reply_markup=main_keyboard())


def talk_to_me(update, context):
    text = update.message.text
    update.message.reply_text(text, reply_markup=main_keyboard())
