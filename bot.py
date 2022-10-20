import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import greet_user, talk_to_me, get_user_photo
from problem import (
    problem_start,
    problem_type,
    problem_details,
    get_details,
    skip_details,
    wtf
)
from settings import API_KEY, PRODUCT_ARTICULS

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(API_KEY,
                    use_context=True)
    
    db = mybot.dispatcher
    
    problem = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Проблема с товаром)$'), problem_start)
        ],
        states={
            'problem_type': [MessageHandler(Filters.text, problem_type)],
            'problem_details': [MessageHandler(Filters.text, problem_details)],
            'get_details': [CommandHandler('skip', skip_details),
                            MessageHandler(Filters.text, get_details)],
            
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, wtf)
        ]
    )
    
    db.add_handler(problem)
    db.add_handler(CommandHandler('start', greet_user))
    db.add_handler(MessageHandler(Filters.photo, get_user_photo))
    db.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('bot has been started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()