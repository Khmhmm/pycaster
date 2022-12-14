import telebot
from telebot import types
import requests
import os
import random

SERVICE_HTTP = 'http://0.0.0.0:5000'

PAUSE_PHRASES = [
    'Пауза! Удар!',
    'Пауза.'
]

CLOSE_PHRASES = [
    'Закрываем браузер',
    'Один момент'
]

with open('tokenstore.txt', 'r') as f:
    token = f.read()
bot = telebot.TeleBot(token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    buttonA = types.KeyboardButton('/help')
    buttonB = types.KeyboardButton('/pause')
    buttonC = types.KeyboardButton('/close')
    markup.row(buttonA, buttonB, buttonC)

    bot.send_message(message.from_user.id, '''
Привет! Я нужен чтобы воспроизводить контент на локальном веб-сервере.
- 🤗 для этого надо написать /show ссылка, или же /show iframe! Кстати, ссылки с ютуба долго запускаются, это особенности самого сайта.
- с недавних пор необязательно писать /show, можно просто прислать мне ссылку или айфрейм
- 🤔 iframe может иметь вид <iframe src="https://site.site/video1"></iframe> и тому подобное
- 🤓 чтобы его получить надо найти на сайте "код для вставки"
- 😞 некоторые сайты не пишут в коде для вставки https или http, укажи его самостоятельно! К сожалению, я недостаточно умён, чтобы проверить, по какому протоколу мне взять видео
- 🥱 чтобы поставить на паузу используй /pause
- 😴 чтобы закрыть видео можешь отправить новое через /show или использовать команду /close
- 🧐 если не можешь разобраться, давай я тебе помогу! Просто пришли мне следующее сообщение:
/show https://www.youtube.com/watch?v=coDqPuZXS9c
- 🧐 если через iframe, то попробуй это:
/show <iframe src="https://www.youtube.com/embed/coDqPuZXS9c"></iframe>
- я понимаю и короткие ссылки на ютуб, например: https://www.youtu.be/coDqPuZXS9c
''', reply_markup=markup)


@bot.message_handler(commands=['show', 'play'])
def show(message, cleared=False):
    link = ' '.join(message.text.split(' ')[1:]) if not cleared else message.text
    try:
        resp = requests.post(SERVICE_HTTP + '/show',
        json={'link': link})

        keyboard = types.InlineKeyboardMarkup()
        # key_yes = types.InlineKeyboardButton(text='Пауза', callback_data='pause')
        # keyboard.add(key_yes)
        key_no= types.InlineKeyboardButton(text='Закрыть', callback_data='close')
        keyboard.add(key_no)

        if resp.status_code == 200:
            bot.send_message(message.from_user.id, text=f'Запрос успешно отправлен!', reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, f'Запрос вернул ошибку с кодом {resp.status_code}')

    except Exception as exc:
        bot.send_message(message.from_user.id, f'Во время попытки отправить запрос возникла ошибка, привожу ее стектрейс:\n{exc}')
        print(exc)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "pause":
        pause('')
    elif call.data == "close":
        close('')
    else:
        print(call.data)



@bot.message_handler(commands=['pause'])
def pause(message):
    try:
        resp = requests.get(SERVICE_HTTP + '/pause')

        if isinstance(message, str):
            return

        if resp.status_code == 200 or resp.status_code == 500:
            txt = PAUSE_PHRASES[random.randint(0, len(PAUSE_PHRASES)-1)]
            bot.send_message(message.from_user.id, txt)
        else:
            bot.send_message(message.from_user.id, f'Запрос вернул ошибку с кодом {resp.status_code}')

    except Exception as exc:
        bot.send_message(message.from_user.id, f'Во время попытки отправить запрос возникла ошибка, привожу ее стектрейс:\n{exc}')
        print(exc)


@bot.message_handler(commands=['close'])
def close(message):
    try:
        resp = requests.get(SERVICE_HTTP + '/close')

        if isinstance(message, str):
            return

        if resp.status_code == 200 or resp.status_code == 500:
                txt = CLOSE_PHRASES[random.randint(0, len(CLOSE_PHRASES)-1)]
                bot.send_message(message.from_user.id, txt)
        else:
            bot.send_message(message.from_user.id, f'Запрос вернул ошибку с кодом {resp.status_code}')

    except Exception as exc:
        bot.send_message(message.from_user.id, f'Во время попытки отправить запрос возникла ошибка, привожу ее стектрейс:\n{exc}')
        print(exc)


@bot.message_handler(func=lambda message: 'https://youtube.com' in message.text or 'https://youtu.be' in message.text or '<iframe src=' in message.text)
def show_quick_youtube(message):
    show(message, cleared=True)


bot.polling(none_stop=True, interval=1)