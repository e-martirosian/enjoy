import time
from threading import Thread

import cv2
import numpy as np
import pyautogui
import telebot
from PIL import Image
from passwords import TOKEN_TELEGRAM

send_boolean = {}
bot = telebot.TeleBot(TOKEN_TELEGRAM, parse_mode='html')
threads = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    global threads
    chat_id = str(message.chat.id)
    bot.send_message(message.chat.id, 'Игра началась... ' + str(message.chat.id))
    if chat_id not in threads:
        send_boolean[chat_id] = True
        threads[chat_id] = Thread(target=schedule_loop, args=(chat_id,))
        threads[chat_id].start()


@bot.message_handler(commands=['stop'])
def stop_sending(message):
    global threads
    chat_id = str(message.chat.id)
    send_boolean[chat_id] = False
    bot.send_message(message.chat.id, 'Игра закончилась...')
    if chat_id in threads:
        threads[chat_id].join()
        threads.pop(chat_id)


def schedule_loop(chat_id):
    while True:
        if chat_id is not None:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            im.save('test.png')

            if send_boolean[chat_id]:
                img = open('test.png', 'rb')
                bot.send_photo(chat_id, img, timeout=1000)
                img.close()
            else:
                break
            time.sleep(2)


bot.polling()
