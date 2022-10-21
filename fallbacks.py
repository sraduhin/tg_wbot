from random import choice

def wtf(update, context):
    print('wtf')
    replies = ['Что?', 'Меня писал соседский ребенок, не понимаю', 'Такие буквы не знаю', 'Извините, я подвис']
    update.message.reply_text(choice(replies))