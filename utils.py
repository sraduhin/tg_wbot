import os
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Благодарность!'],
        ['Проблема с товаром'],
        # ['Хочу картинку с котиком'],
        ['Другое']
    ], one_time_keyboard=True)


def submit_inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Отправить', callback_data='True')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def save_message_id(update, context):
    print('save_message_id')
    update.callback_query.answer()
    message_id = update.callback_query.message.message_id
    return message_id
    
def show_choice_and_get_answer(update, context):
    print('show_choice_and_get_answer')
    print(update.callback_query.message.message_id)
    answer = update.callback_query.data
    update.callback_query.edit_message_reply_markup(reply_markup=None)
    # context.bot.editMessageReplyMarkup(chat_id=update.effective_chat.id, message_id=save_message_id(update, context), reply_markup=None)
    text = f"<b>Вы указали</b>: {answer}"
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
        problem_content = f"<b>Артикул</b>: {problem['product_type']}\n" + problem_content
    if 'details' in problem:
        problem_content += f"\n<b>Комментарий</b>: {problem['details']}"
    if 'photos' in problem:
        print(problem)
        problem_content += f"\nТак же есть {get_photos_count(problem)} фото"
    return problem_content


def format_issue(issue):
    print('format_issue')
    issue_content = f"""<b>Имя</b>: {issue['username']}"""
    if 'details' in issue['data']:
        issue_content += f"\n<b>Комментарий</b>: {issue['data']['details']}"
    if 'photos' in issue['data']:
        issue_content += f"\nТак же есть {get_photos_count(issue['data'])} фото"
    return issue_content


def get_user_photo(update, context):
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Фото сохранено')
    return file_name


def get_feedback_type(request_result):
    result = []
    for fdbck in request_result:
        print(fdbck['feedback'])
        if fdbck.get('feedback'):
            result.append(
                {
                    '_id': fdbck['_id'],
                    'username': fdbck['username'],
                    'description': fdbck['feedback'].get('problem_kind') or fdbck['feedback'].get('type')
                }
            )
    return result
