import pyautogui
import cv2
import numpy as np
from PIL import Image
import telebot
import time
from threading import Thread
import sys


TOKEN_TELEGRAM = ''
send_boolean = {}
bot = telebot.TeleBot(TOKEN_TELEGRAM, parse_mode='html')
chat_id = None
thread1 = None

@bot.message_handler(commands=['start'])
def start_message(message):
    global chat_id,thread1
    bot.send_message(message.chat.id, 'Игра началась... '+str(message.chat.id))
    chat_id = str(message.chat.id)
    thread1 = Thread(target=schedule_loop, args=(bot,))
    thread1.start()

@bot.message_handler(commands=['stop'])
def stop_sending(message):
    global thread1
    chat_id = str(message.chat.id)
    send_boolean[chat_id] = False
    bot.send_message(message.chat.id, 'Игра закончилась...')
    thread1.join()

def schedule_loop(bot):
    global chat_id
    while True:
        if chat_id is not None:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            im.save('test.png')

            if chat_id not in send_boolean:
                img = open('test.png', 'rb')
                bot.send_photo(chat_id, img, timeout = 1000)
                img.close()
            else:
                break
                bot.stop_bot()
                sys.exit()
            time.sleep(2)
            
bot.polling()

