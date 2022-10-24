import re
from db import db, get_or_create_user, save_problem
from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from utils import choose_product, format_problem, main_keyboard, submit_inline_keyboard
from settings import PRODUCT_ARTICULS
from handlers import get_user_photo


def problem_start(update, context):
    print('problem_start')
    update.message.reply_text('Печаль...', reply_markup=ReplyKeyboardRemove())
    context.user_data['username'] = update.message.chat.username
    choose_product(update, context)
    return 'product_type'


def repeat_choice(update, context):
    choose_product(update, context)
    return 'product_type'


def product_type(update, context):
    print('product_type')
    text = update.message.text
    print(text)
    try:
        subtext = re.search(r'[a-zA-Z0-9]{6,}', text)[0]
    except:
        update.message.reply_text('Артикул не распознан')
        help_find_articul(update, context)
    print(subtext)
    if subtext not in PRODUCT_ARTICULS:
        help_find_articul(update, context)
    context.user_data['problem'] = {}
    context.user_data['problem']['product_type'] = update.message.text
    reply_keyboard = [
        ['Товар с браком'],
        ['Товар не соответствует заказу'],
        ['Другое']
    ]
    update.message.reply_text(
        'Укажите, что не так с товаром',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                         one_time_keyboard=True)
    )
    return 'problem_details'


def skip_product(update, context):
    update.message.reply_text(
        'Вы можете описать проблему, приложить фото, либо пропустить этот шаг, нажав /skip'  # Noqa: E501
    )
    context.user_data['problem'] = {}
    return 'get_details'


def help_find_articul(update, context):
    print('help_find_articul')
    reply_keyboard = [
        ['Пример', 'Вернуться к списку товаров'],
        ['Оставить обращение без указания артикула']
    ]
    update.message.reply_text(
        'Вы можете посмотреть артикул товара на вкладке заказы своего личного кабинета, либо на странице товара.',  # Noqa: E501
        reply_markup=ReplyKeyboardMarkup(reply_keyboard)
    )
    return 'product_type'


def get_articul_example(update, context):
    print('get_articul_example')
    print(update.message.text)
    chat_id = update.effective_chat.id
    articul_pic_filename = 'images/help_to_find_articul.jpg'
    context.bot.send_photo(
        chat_id=chat_id, photo=open(articul_pic_filename, 'rb')
    )
    return 'product_type'


def problem_details(update, context):
    print('problem_details')
    context.user_data['problem']['problem_kind'] = update.message.text
    update.message.reply_text('Вы можете описать проблему подробнее, приложить фото, либо пропустить этот шаг, нажав /skip')
    return 'get_details'


def get_photo(update, context):
    print('get_photo')
    if 'photo' not in context.user_data['problem']:
        context.user_data['problem']['photos'] = []
    context.user_data['problem']['photos'].append(
        get_user_photo(update, context)
    )
    ask_before_send(update, context)
    return 'end_conversation'


def ask_before_send(update, context):
    problem_content = format_problem(context.user_data['problem'])
    update.message.reply_text(
        problem_content,
        reply_markup=submit_inline_keyboard(),
        parse_mode=ParseMode.HTML
    )


def submit_submit(update, context):
    update.callback_query.answer()
    text = f"Спасибо, за ваше обращение! {update.callback_query.data}"
    update.callback_query.edit_message_caption(caption=text)


def get_details(update, context):
    print('get_details')
    context.user_data['problem']['details'] = update.message.text
    ask_before_send(update, context)
    return 'end_conversation'


def skip_details(update, context):
    print('skip_details')
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_problem(db, user['user_id'], context.user_data['problem'])
    update.message.reply_text('Спасибо, за ваше обращение',
                              reply_markup=main_keyboard())
    return ConversationHandler.END


def new_comment(update, context):
    print('new_comment')
    context.user_data['problem']['details'] += f'\n{update.message.text}'
    ask_before_send(update, context)
    return 'end_conversation'


def end_conversation(update, context):
    print('end_conversation')
    user = get_or_create_user(
        db, update.effective_user,
        update.message.chat.id
    )
    save_problem(db, user['user_id'], context.user_data['problem'])
    update.message.reply_text('Спасибо, за ваше обращение',
                              reply_markup=main_keyboard())
    return ConversationHandler.END
