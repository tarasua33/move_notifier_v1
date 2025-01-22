# import telebot
# from telebot import types
# import cv2
# import sqlite3
# import json

# # name = ''
#
#
# @bot.message_handler(commands=['register'])
# def register(message):
#     conn = sqlite3.connect('users.sql')
#     cur = conn.cursor()
#
#     cur.execute('''
#         CREATE TABLE IF NOT EXISTS users
#             (id INT auto_increment primary key,
#             name varchar(50),
#             pass varchar(50),
#             chat_id varchar(50)
#             )
#     ''')
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     bot.send_message(message.chat.id, "Start registration, Please enter password:")
#     bot.register_next_step_handler(message, user_pass)
#
#
# def user_pass(message):
#     password = message.text.strip()
#
#     conn = sqlite3.connect('users.sql')
#     cur = conn.cursor()
#
#     cur.execute('''
#             SELECT * FROM users
#             WHERE name = "%s"
#         ''' % message.from_user.id)
#     users = cur.fetchall()
#     answer = ""
#
#     if len(users) == 0:
#         cur.execute('''
#                 INSERT INTO users (name, pass, chat_id) VALUES ("%s", "%s", "%s")
#             ''' % (message.from_user.id, password, message.chat.id))
#
#         answer = "Registration completed"
#     else:
#         answer = "You are already registered"
#
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     mark_up = types.InlineKeyboardMarkup()
#     mark_up.add(types.InlineKeyboardButton('Show all users', callback_data='users'))
#     bot.send_message(message.chat.id, answer, reply_markup=mark_up)
#     # bot.send_message(message.chat.id, message)
#
#
# @bot.callback_query_handler(func=lambda callback: True)
# def callback_handler(callback):
#     if callback.data == 'users':
#         show_users(callback)
#
#
# def show_users(callback):
#     conn = sqlite3.connect('users.sql')
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall()
#
#     list = ''
#     for line in users:
#         list += f'Login: {line[1]}, pass: {line[2]}, chat_id: {line[3]} \n'
#     bot.send_message(callback.message.chat.id, f'<b> {list} </b>', parse_mode='html')
#
#     cur.close()
#     conn.close()


# def send_to_telegram(frame):
#     # bot = Bot(token=bot_token)
#     # with open(photo_path, 'rb') as photo:
#
#     path = './detected_face.jpg'
#     cv2.imwrite(path, frame)

    # bot = telebot.TeleBot(ID)
    # conn = sqlite3.connect('users.sql')
    # cur = conn.cursor()
    # cur.execute('SELECT * FROM users')
    # users = cur.fetchall()
    #
    # with open(path, 'rb') as photo:
    #     for line in users:
    #         bot.send_photo(chat_id=line[3], photo=photo)


# bot.polling(none_stop=True)