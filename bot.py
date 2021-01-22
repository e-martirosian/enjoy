import pyautogui
import cv2
import numpy as np
from PIL import Image
import telebot
import time
from passwords import TOKEN_TELEGRAM

bot = telebot.TeleBot(TOKEN_TELEGRAM, parse_mode='html')
send_boolean = {}


def send_screens(chat_id):
    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        im.save('test.png')

        if send_boolean[chat_id]:
            img = open('test.png', 'rb')
            bot.send_photo(chat_id, img)
            img.close()
        else:
            break

        time.sleep(5)


@bot.message_handler(commands=['start'])
def start_sending(message):
    chat_id = str(message.chat.id)
    print('start_sending chat_id:', chat_id)
    send_boolean[chat_id] = True
    send_screens(chat_id)


@bot.message_handler(commands=['stop'])
def stop_sending(message):
    chat_id = str(message.chat.id)
    print('stop_sending chat_id:', chat_id)
    send_boolean[chat_id] = False


@bot.message_handler(commands=['chat_id'])
def send_welcome(message):
    bot.reply_to(message, 'Your chat ID ' + str(message.chat.id))


bot.infinity_polling(True)