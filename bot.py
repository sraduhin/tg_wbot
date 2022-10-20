import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import greet_user, send_articul_example, talk_to_me, get_user_photo
from issue import issue_start, issue_type, issue_details
from settings import API_KEY

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(API_KEY,
                    use_context=True)
    
    db = mybot.dispatcher
    
    issue = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Проблема с товаром)$'), issue_start)
        ],
        states={
            'issue_type': [MessageHandler(Filters.text, issue_type)],
            'issue_details': [MessageHandler(Filters.text, issue_details)]
        },
        fallbacks=[]
    )
    
    db.add_handler(CommandHandler('start', greet_user))
    db.add_handler(issue)
    # db.add_handler(CommandHandler('articul', send_articul_example))
    # db.add_handler(MessageHandler(Filters.regex('^(Проблема с товаром)$'), send_articul_example))
    db.add_handler(MessageHandler(Filters.photo, get_user_photo))
    # db.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('bot has been started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()