from telegram import ReplyKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Благодарность!'],
        ['Проблема с товаром'],
        ['Хочу картинку с котиком'],
        ['Другое']
    ])