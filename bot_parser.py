from logging import log
import telebot
from telebot import types
import email
import imaplib
from time import sleep
from loguru import logger
from email_test import emailCheck

bot = telebot.TeleBot('1966502335:AAGZIqTdt16OJ72ct_j8I9T0IJVKWAC2gbQ')


dict_bot = {
    'start': 'Доброго времени суток\nВведите /email для того чтобы выполнить',
    }


username = 'Рудольф'
age = 12
answ = f"Привет, {username}, тебе {age} лет"
logger.info(f"Бот запущен")
logger.debug(f"Сообщение - {answ}")
logger.error("Бот запущен")

# @bot.message_handler(commands=list(dict_bot))
# def bot_command(message):
#     key = (message.text).replace('/','')
#     bot.send_message(message.chat.id, dict_bot.get(key))

    
# @bot.message_handler(content_types=['text'])
# def bot_text_command(message):
#         if message.text == '/email':
#             bot.send_message(message.chat.id,answer(message))


@bot.message_handler(commands=['start'])
def bot_command_start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg'))
    markup.add(telebot.types.InlineKeyboardButton(text='Подробнее про бота', callback_data='more'))
    markup.add(telebot.types.InlineKeyboardButton(text='Сказать идею', callback_data='say'))
    bot.send_message(message.chat.id, text="Здравствуйте {0.first_name},для дальнейшей работы выберите нужную кнопку.".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['help'])
def bot_command_help(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='На главную', callback_data='owner'))
    bot.send_message(message.chat.id,text='Выберите пункт',reply_markup=markup)


@bot.message_handler(commands=['settings'])
def bot_command_settings(message):
    bot.send_message(message.chat.id,'Скоро тут будут настройки!')


@bot.message_handler(commands=['home'])
def bot_command_settings(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Показать полностью', callback_data='view_all'))
    markup.add(telebot.types.InlineKeyboardButton(text='Отметить прочитанным', callback_data='mark_read'))
    markup.add(telebot.types.InlineKeyboardButton(text='Ответить', callback_data='answer'))
    markup.add(telebot.types.InlineKeyboardButton(text='Удалить', callback_data='delete'))
    bot.send_message(message.chat.id,text='Выберите нужный пункт',reply_markup=markup)

@bot.message_handler(commands=['email'])
def bot_command_email(message):
    email_list = emailCheck().get_email()
    for item in email_list:
        answ = f"*От*: {item.get('sender')}\n*Тема*: {item.get('subject')}\n*Дата*: {item.get('date_send')}\n*Статус*: {item.get('type')}\n"
        bot.send_message(message.chat.id, answ, parse_mode='Markdown')

    # mail = imaplib.IMAP4_SSL('imap.gmail.com')
    # mail.login('xde.test.070', '6c7c6b7b7x')
    # mail.select("INBOX")
    # (retcode, messages) = mail.search(None, '(UNSEEN)')
    # if retcode == 'OK':
    #     n = 0
    #     for num in messages[0].split():
    #         n = n + 1
    #         typ, data = mail.fetch(num, '(RFC822)')
    #         for respone_part in data:
    #             if isinstance(respone_part, tuple):
    #                 original = email.message_from_string('respone_part[1]')
    #                 print(original['From'])
    #                 data = original['Subject']
    #                 print(data)
    #                 typ, data = mail.store(num, '+FLAGS', '\\Seen')
            

                    
    # bot.send_message(message.chat.id,mail)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за выбор нашего бота!')
    answer = ''
    if call.data == 'reg':
        answer = 'Вы выбрали пункт Зарегистрироваться!'
    elif call.data == 'more':
        answer = 'Вы выбрали пункт Подробнее про бота!'
    elif call.data == 'say':
        answer = 'Вы выбрали пункт Сказать идею!'
    elif call.data == 'owner':
        answer = 'Перемещаю вас на главную страницу!'
    elif call.data == 'view_all':
        answer = 'Посмотреть всё'
    elif call.data == 'mark_read':
        answer = 'Отметить прочитанным'
    elif call.data == 'answer':
        answer = 'Ответить'
    elif call.data == 'delete':
        answer = 'Удалить'

    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)



bot.polling(none_stop = True)