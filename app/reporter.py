# from telebot import TeleBot
import time
import sqlite3
from cv2 import imwrite
from logging import info


class Reporter:
    def __init__(self, bot_token):
        self.__bot_token = bot_token
        info("Reporter/ init/ created")

    @staticmethod
    def save_frame(frame):
        save_path = f"img/detected_image{time.time()}.jpg"
        imwrite(save_path, frame)
        return save_path

    def report(self, frame):
        path = Reporter.save_frame(frame)

        # bot = TeleBot(token=self.__bot_token)
        #
        # conn = sqlite3.connect('users.sql')
        # cur = conn.cursor()
        # cur.execute('SELECT * FROM users')
        # users = cur.fetchall()
        #
        # for line in users:
        #     Reporter.send_to_telegram(path, line[1], bot)

    @staticmethod
    def send_to_telegram(photo_path, chat_id, bot):
        with open(photo_path, 'rb') as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)
