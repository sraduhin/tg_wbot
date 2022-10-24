import logging
import problems
import respects
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler, 
    ConversationHandler,
    MessageHandler, 
    Filters, 
    Updater
)
from handlers import greet_user, talk_to_me, get_user_photo

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
                MessageHandler(Filters.regex('^(Пример)$'), problems.get_articul_example),
                MessageHandler(Filters.regex('^(Помощь. Где узнать артикул)\?$'), problems.help_find_articul),
                MessageHandler(Filters.regex('^(Вернуться к списку товаров)$'), problems.repeat_choice),
                MessageHandler(Filters.regex('^(Оставить обращение без указания артикула)$'), problems.skip_product),
                MessageHandler(Filters.text, problems.product_type)
            ],
            'problem_details': [MessageHandler(Filters.text, problems.problem_details)],
            'get_details': [
                CommandHandler('skip', problems.skip_details),
                MessageHandler(Filters.photo, problems.get_photo),
                MessageHandler(Filters.text, problems.get_details)
            ],
            'end_conversation': [
                CallbackQueryHandler(problems.submit_submit, per_message=True),
                MessageHandler(Filters.regex('^(Отправляем!)$'), problems.end_conversation),
                MessageHandler(Filters.photo, problems.get_photo),
                MessageHandler(Filters.text, problems.new_comment)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, wtf)
        ]
    )
    respect = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Благодарность!)$'), respects.thanks_start)
        ],
        states={
            'get_respect': [
                MessageHandler(Filters.text, respects.get_respect)
            ],
            'get_details': [
                MessageHandler(Filters.photo, respects.get_photo),
                MessageHandler(Filters.text, respects.get_respect)
            ],
            'end_conversation': [
                MessageHandler(Filters.regex('^(Отправляем!)$'), respects.end_conversation),
                MessageHandler(Filters.photo, respects.get_photo),
                MessageHandler(Filters.text, respects.new_comment)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, wtf)
        ]
    )

    db.add_handler(problem)
    db.add_handler(respect)
    db.add_handler(MessageHandler(Filters.photo, get_user_photo))
    db.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('bot has been started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()