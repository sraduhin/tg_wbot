import logging
import problems
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler, 
    ConversationHandler,
    MessageHandler, 
    Filters, 
    Updater
)
from handlers import greet_user, talk_to_me, simple_handler, submit_submit

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
            MessageHandler(Filters.regex('^(Проблема с товаром)$'), problems.problem_start)
        ],
        states={
            'product_type': [
                CallbackQueryHandler(problems.product_type, pattern='^' + '[a-zA-Z0-9]{6,}' + '$'),
                CallbackQueryHandler(problems.help_find_articul, pattern='^' + 'HELP_TO_FIND_ARTICUL' + '$'),
                CallbackQueryHandler(problems.get_articul_example, pattern='^' + 'EXAMPLE' + '$'),
                CallbackQueryHandler(problems.skip_product, pattern='^' + 'Оставить обращение без указания артикула' + '$'),
                #MessageHandler(Filters.text, problems.product_type)
            ],
            'problem_type': [CallbackQueryHandler(problems.problem_type)],
            'get_description': [
                CallbackQueryHandler(problems.end_conversation),
                CommandHandler('skip', problems.skip_details),
                MessageHandler(Filters.text, problems.get_description),
                MessageHandler(Filters.photo, problems.get_photo)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, wtf)
        ]
    )


    db.add_handler(problem)
    db.add_handler(MessageHandler(Filters.regex('^(someshit)$'), simple_handler))
    # db.add_handler(CallbackQueryHandler(submit_submit))
    db.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('bot has been started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()