import os
from utils import main_keyboard

def greet_user(update, context):
    print('greet_user')
    update.message.reply_text('Добрый день! Выберете интересующий вас вопрос!', reply_markup=main_keyboard())


def talk_to_me(update, context):
    print('talk_to_me')
    text = update.message.text
    text = f'Ок! Ваша проблема {text}'
    print(text)
    update.message.reply_text(text, reply_markup=main_keyboard())


def send_articul_example(update, context):
    print('send_articul_example')
    chat_id = update.effective_chat.id
    articul_pic_filename = 'images/find_articul.png'
    context.bot.send_photo(chat_id=chat_id, photo=open(articul_pic_filename, 'rb'), reply_markup=main_keyboard())


def get_user_photo(update, context):
    print('get_user_photo')
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Фото сохранено')