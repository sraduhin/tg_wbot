import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import greet_user, talk_to_me, get_user_photo
from problem import (
    end_conversation,
    get_articul_example,
    get_details,
    help_find_articul,
    new_comment,
    get_photo,
    problem_start,
    problem_details,
    product_type,
    repeat_choice,
    skip_details,
    skip_product,
    wtf
)
from thanks import (
    thanks_start,
    get_respect,
    wtf
)
from fallbacks import wtf

from settings import API_KEY

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(API_KEY,
                    use_context=True)
    
    db = mybot.dispatcher
    
    db.add_handler(CommandHandler('start', greet_user))
    problem = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Проблема с товаром)$'), problem_start)
        ],
        states={
            'product_type': [
                MessageHandler(Filters.regex('^(Пример)$'), get_articul_example),
                MessageHandler(Filters.regex('^(Помощь. Где узнать артикул)\?$'), help_find_articul),
                MessageHandler(Filters.regex('^(Вернуться к списку товаров)$'), repeat_choice),
                MessageHandler(Filters.regex('^(Оставить обращение без указания артикула)$'), skip_product),
                MessageHandler(Filters.text, product_type)
            ],
            'problem_details': [MessageHandler(Filters.text, problem_details)],
            'get_details': [
                CommandHandler('skip', skip_details),
                MessageHandler(Filters.photo, get_photo),
                MessageHandler(Filters.text, get_details)
            ],
            'end_conversation': [
                MessageHandler(Filters.regex('^(Отправляем!)$'), end_conversation),
                MessageHandler(Filters.photo, get_photo),
                MessageHandler(Filters.text, new_comment)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, wtf)
        ]
    )
    thanks = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Благодарность)$'), thanks_start)
        ],
        states={
            'get_respect': [
                MessageHandler(Filters.text, get_respect)
            ],
            'problem_details': [MessageHandler(Filters.text, problem_details)],
            'get_details': [
                CommandHandler('skip', skip_details),
                MessageHandler(Filters.photo, get_photo),
                MessageHandler(Filters.text, get_details)
            ],
            'end_conversation': [
                MessageHandler(Filters.regex('^(Отправляем!)$'), end_conversation),
                MessageHandler(Filters.photo, get_photo),
                MessageHandler(Filters.text, new_comment)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, wtf)
        ]
    )
    
    db.add_handler(problem)
    db.add_handler(thanks)
    db.add_handler(MessageHandler(Filters.photo, get_user_photo))
    db.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('bot has been started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()