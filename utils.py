import os
import re
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Благодарность!'],
        ['Проблема с товаром'],
        ['Хочу картинку с котиком'],
        ['Другое']
    ], one_time_keyboard=True)


def submit_inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Отправить', callback_data='True')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def show_choice_and_get_answer(update, context):
    update.callback_query.answer()
    answer = update.callback_query.data
    if answer == 'Без артикула':
        return answer
    text = f"<b>Вы указали</b>: {answer}"
    update.callback_query.edit_message_reply_markup(reply_markup=None)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    return answer


def get_photos_count(data):
    len_photos = len(data['photos'])
    if len_photos == 1:
        return 'одно'
    return 'несколько' if len_photos > 3 else 'парочку'


def format_problem(problem):
    print('format_problem')
    problem_content = f"""<b>Проблема</b>: {problem['problem_kind']}"""
    if 'product_type' in problem:
        problem_content = f"<b>Товар</b>: Коробка {problem['product_type']}\n" + problem_content
    if 'details' in problem:
        problem_content += f"\n<b>Комментарий</b>: {problem['details']}"
    if 'photos' in problem:
        print(problem)
        problem_content += f"\nТак же есть {get_photos_count(problem)} фото"
    return problem_content


def format_respect(respect):
    print('format_respect')
    respect_content = f"""<b>Имя</b>: {respect['problem_kind']}"""
    if 'product_type' in respect:
        respect_content = f"<b>Товар</b>: Коробка {respect['product_type']}\n" + respect_content
    if 'details' in respect:
        respect_content += f"\n<b>Комментарий</b>: {respect['details']}"
    if 'photos' in respect:
        print(respect)
        respect_content += f"\nТак же есть {get_photos_count(respect)} фото"
    return respect_content


def get_user_photo(update, context):
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Фото сохранено')
    return file_name