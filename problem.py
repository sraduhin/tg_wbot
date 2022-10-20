import re
from random import choice
from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from utils import main_keyboard
from settings import PRODUCT_ARTICULS


def problem_start(update, context):
    print('problem_start')
    context.user_data['username'] = update.message.chat.username
    update.message.reply_text('Печаль...', reply_markup=ReplyKeyboardRemove())
    choose_product(update, context)
    return 'problem_type'


def choose_product(update, context):
    reply_keyboard = [
        ['Мягкая коробка\n(98484896)', 'Жесткая коробка\n(98917907)'],
        ['Полужесткая белая\n(98915200)', 'Полужесткая серая\n(98915552)'],
        ['Помощь. Где узнать артикул?']
    ]
    update.message.reply_text('Укажите артикул товара, по которому хотите оставить обращение',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )


def problem_type(update, context):
    print('problem_type')
    text = update.message.text
    print(text)
    try:
        subtext = re.search(r'[a-zA-Z0-9]{6,}', text)[0]
    except:
        subtext = 'unknown'
    print(subtext)
    if not subtext in PRODUCT_ARTICULS:
        get_articul_example(update, context)
        choose_product(update, context)
        return 'problem_type'
    context.user_data['problem'] = {}
    context.user_data['problem']['product_type'] = update.message.text
    reply_keyboard = [['Товар с браком'], ['Товар не соответствует заказу'], ['Другое']]
    update.message.reply_text('Укажите, что не так с товаром',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return 'problem_details'


def get_articul_example(update, context):
    print('get_articul_example')
    update.message.reply_text('Вы можете посмотреть артикул товара на вкладке заказы своего личного кабинета, либо на странице товара.')
    chat_id = update.effective_chat.id
    articul_pic_filename = 'images/help_to_find_articul.jpg'
    context.bot.send_photo(chat_id=chat_id, photo=open(articul_pic_filename, 'rb'), reply_markup=main_keyboard())


def problem_details(update, context):
    print('problem_details')
    context.user_data['problem']['problem_kind'] = update.message.text
    update.message.reply_text('Вы можете описать проблему, приложить фото, либо пропустить этот шаг, нажав /skip')
    return 'get_details'


def get_details(update, context):
    print('get_details')
    context.user_data['problem']['details'] = update.message.text
    problem_content = format_problem(context.user_data['problem'])
    update.message.reply_text(problem_content, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def skip_details(update, context):
    print('skip_details')
    problem_content = format_problem(context.user_data['problem'])
    update.message.reply_text(problem_content, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def format_problem(problem):
    print('format_problem')
    problem_content = f"""<b>Товар</b>: {problem['product_type']}
<b>Проблема</b>: {problem['problem_kind']}"""
    if 'details' in problem:
        problem_content += f"\n<b>Комментарий</b>: {problem['details']}"
    return problem_content


def wtf(update, context):
    print('wtf')
    replies = ['Что?', 'Меня писал соседский ребенок, не понимаю', 'Такие буквы не знаю', 'Извините, я подвис']
    update.message.reply_text(choice(replies))