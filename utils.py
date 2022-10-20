import re
from telegram import ReplyKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Благодарность!'],
        ['Проблема с товаром'],
        ['Хочу картинку с котиком'],
        ['Другое']
    ])


def get_articul(text):
    return re.search(r'[a-zA-Z0-9]{6,}', text)[0]