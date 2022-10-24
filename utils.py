import re
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Благодарность!'],
        ['Проблема с товаром'],
        ['Хочу картинку с котиком'],
        ['Другое']
    ])


def submit_inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Отправить', callback_data='True')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def choose_product(update, context):
    reply_keyboard = [
        ['Мягкая коробка\n(98484896)', 'Жесткая коробка\n(98917907)'],
        ['Полужесткая белая\n(98915200)', 'Полужесткая серая\n(98915552)'],
        ['Помощь. Где узнать артикул?']
    ]
    update.message.reply_text('Укажите артикул товара, по которому хотите оставить обращение',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )


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