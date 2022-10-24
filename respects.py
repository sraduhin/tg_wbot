from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from handlers import get_user_photo


def thanks_start(update, context):
    print('thanks_start')
    update.message.reply_text('Будем рады прочитать лестные слова о нас!\nМожете приложить фото для коллекции.', reply_markup=ReplyKeyboardRemove())
    context.user_data['username'] = update.message.chat.username
    context.user_data['respect'] = {}
    return 'get_respect'


def get_photo(update, context):
    print('get_photo')
    if not 'photo' in context.user_data['problem']:
        context.user_data['problem']['photos'] = []
    context.user_data['problem']['photos'].append(get_user_photo(update, context))
    ask_before_send(update, context)
    return 'end_conversation'


def ask_before_send(update, context):
    respect_content = format_problem(context.user_data['problem'])
    reply_keyboard = [['Отправляем!']]
    update.message.reply_text(
        problem_content,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode=ParseMode.HTML
    )

def get_respect(update, context):
    print('get_respect')
    context.user_data['respect']['details'] = update.message.text
    ask_before_send(update, context)
    return 'end_conversation'


def skip_details(update, context):
    print('skip_details')
    ask_before_send(update, context)
    return 'end_conversation'


def new_comment(update, context):
    print('new_comment')
    context.user_data['problem']['details'] += f'\n{update.message.text}'
    ask_before_send(update, context)
    return 'end_conversation'


def end_conversation(update, context):
    print('end_conversation')
    update.message.reply_text('Спасибо, за ваше обращение', reply_markup=main_keyboard())
    return ConversationHandler.END
