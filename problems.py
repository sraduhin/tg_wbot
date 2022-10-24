from db import db, get_or_create_user, save_problem
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from utils import show_choice_and_get_answer, format_problem, main_keyboard, get_user_photo
from products import PRODUCTS


def problem_start(update, context):
    print('problem_start')
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Печаль...',)
    context.user_data['username'] = update.message.chat.username
    keyboard = [
        [InlineKeyboardButton(f"{product['name']}. {product['wb_articul']}", callback_data=product['wb_articul'])] for product in PRODUCTS
    ]
    keyboard.append([InlineKeyboardButton('Помощь. Где узнать артикул?', callback_data='HELP_TO_FIND_ARTICUL')])
    context.bot.send_message(chat_id=update.effective_chat.id, text='Укажите артикул товара, по которому хотите оставить обращение',
                            reply_markup=InlineKeyboardMarkup(keyboard))
    return 'product_type'


def product_type(update, context):
    print('product_type')
    context.user_data['problem'] = {}
    context.user_data['problem']['product_type'] = show_choice_and_get_answer(update, context)
    keyboard = [
        [InlineKeyboardButton('Товар с браком', callback_data='Товар с браком')],
        [InlineKeyboardButton('Товар не соответствует заказу', callback_data='Товар не соответствует заказу')],
        [InlineKeyboardButton('Другое', callback_data='Другое')],
    ]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Укажите, что не так с товаром',
                            reply_markup=InlineKeyboardMarkup(keyboard))
    return 'problem_type'


def skip_product(update, context):
    update.callback_query.answer()
    context.user_data['problem']['product_type'] = 'Не указано'
    update.message.reply_text(
        'Вы можете описать проблему, приложить фото, либо пропустить этот шаг, нажав /skip'  # Noqa: E501
    )
    context.user_data['problem'] = {}
    return 'get_details'


def help_find_articul(update, context):
    print('help_find_articul')
    update.callback_query.answer()
    keyboard = [
        [InlineKeyboardButton('Пример', callback_data='EXAMPLE')],
        [InlineKeyboardButton('Оставить обращение без указания артикула', callback_data='Без артикула')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Вы можете посмотреть артикул товара на вкладке заказы своего личного кабинета, либо на странице товара.',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return 'product_type'


def get_articul_example(update, context):
    print('get_articul_example')
    chat_id = update.effective_chat.id
    articul_pic_filename = 'images/help_to_find_articul.jpg'
    context.bot.send_photo(
        chat_id=chat_id, photo=open(articul_pic_filename, 'rb')
    )
    return 'product_type'


def problem_type(update, context):
    print('problem_type')
    context.user_data['problem']['problem_kind'] = show_choice_and_get_answer(update, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Вы можете описать проблему подробнее, приложить фото, либо пропустить этот шаг, нажав /skip')
    return 'get_description'


def get_photo(update, context):
    print('get_photo')
    if 'photo' not in context.user_data['problem']:
        context.user_data['problem']['photos'] = []
    context.user_data['problem']['photos'].append(
        get_user_photo(update, context)
    )
    print(update)
    if context.user_data['problem'].get('details'):
        context.user_data['problem']['details'] += f'\n{update.message.caption}'
    else:
        context.user_data['problem']['details'] = update.message.caption
    ask_before_send(update, context)
    return 'get_description'


def ask_before_send(update, context):
    problem_content = format_problem(context.user_data['problem'])
    keyboard = [
        [InlineKeyboardButton('Отправить', callback_data='SEND_CONVERSATION')]
    ]
    context.bot.send_message(chat_id=update.effective_chat.id, text=problem_content,
                             reply_markup=InlineKeyboardMarkup(keyboard), 
                             parse_mode=ParseMode.HTML)
    return 'get_description'


def get_description(update, context):
    print('get_description')
    print(context.user_data['problem'])
    if context.user_data['problem'].get('details'):
        context.user_data['problem']['details'] += f'\n{update.message.text}'
    else:
        context.user_data['problem']['details'] = update.message.text
    return ask_before_send(update, context)


def skip_details(update, context):
    print('skip_details')
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_problem(db, user['user_id'], context.user_data['problem'])
    context.bot.send_message(chat_id=update.effective_chat.id, text='Спасибо, за ваше обращение!',
                             reply_markup=main_keyboard())
    return ConversationHandler.END


def end_conversation(update, context):
    print('end_conversation')
    update.callback_query.answer()
    update.callback_query.edit_message_reply_markup(reply_markup=None)
    user = get_or_create_user(
        db, update.effective_user,
        update.callback_query.message.chat.id
    )
    save_problem(db, user['user_id'], context.user_data['problem'])
    context.bot.send_message(chat_id=update.effective_chat.id, text='Спасибо, за ваше обращение!',
                             reply_markup=main_keyboard())
    return ConversationHandler.END
