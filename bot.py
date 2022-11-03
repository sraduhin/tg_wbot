import logging
import fallbacks
import problems
import issues
from telegram.ext import (CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, 
    Filters, Updater)
from handlers import admin, show_feedback, greet_user, talk_to_me


from settings import API_KEY

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(API_KEY,
                    use_context=True)

    db = mybot.dispatcher

    db.add_handler(CommandHandler('admin', admin))
    db.add_handler(CommandHandler('start', greet_user))
    problem = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Проблема с товаром)$'), problems.problem_start)
        ],
        states={
            'product_type': [
                CallbackQueryHandler(problems.get_articul_example, pattern='^' + 'EXAMPLE' + '$'),
                CallbackQueryHandler(problems.product_type, pattern='^' + 'Без артикула' + '$'),
                CallbackQueryHandler(problems.product_type, pattern='^' + '[a-zA-Z0-9]{6,}' + '$'),
                CallbackQueryHandler(problems.help_find_articul, pattern='^' + 'HELP_TO_FIND_ARTICUL' + '$'),
                #MessageHandler(Filters.text, problems.product_type)
            ],
            'problem_type': [CallbackQueryHandler(problems.problem_type)],
            'get_description': [
                CallbackQueryHandler(problems.end_conversation),
                CommandHandler('skip', problems.skip_details),
                MessageHandler(Filters.text & ~Filters.regex('^[/]'), problems.get_description),
                MessageHandler(Filters.photo, problems.get_photo)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', fallbacks.cancel),
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, fallbacks.wtf)
        ]
    )
    issue = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Благодарность!)$'), issues.issue_start),
            MessageHandler(Filters.regex('^(Другое)$'), issues.issue_start)
        ],
        states={
            'get_description': [
                CallbackQueryHandler(issues.end_conversation),
                MessageHandler(Filters.text & ~Filters.regex('^[/]'), problems.get_description),
                MessageHandler(Filters.photo, problems.get_photo)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', fallbacks.cancel),
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, fallbacks.wtf)
        ]
    )

    db.add_handler(problem)
    db.add_handler(issue)
    db.add_handler(CallbackQueryHandler(show_feedback, pattern='^' + 'admin_request'))
    db.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('bot has been started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()