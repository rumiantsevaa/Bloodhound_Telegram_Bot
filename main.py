import telebot
from telebot import types
from config import TELEGRAM_TOKEN
from free_search import perform_pixabay_search
from ultimate_search import perform_google_reverse_image_search
from yandex_search import perform_yandex_reverse_image_search
from db import init_db, can_use_search, update_usage
import requests
import magic
import time
import re

init_db()
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Глобальное хранилище ожиданий фото
waiting_for_photo = {}

def validate_image(file_url):
    try:
        response = requests.get(file_url, timeout=10)
        mime = magic.from_buffer(response.content, mime=True)
        if not mime.startswith("image/"):
            return False
        if len(response.content) > 5 * 1024 * 1024:  # 5MB limit
            return False
        return True
    except Exception as e:
        print(f"[VALIDATION ERROR] {e}")
        return False

def is_valid_query(query):
    query = query.strip()
    if not (3 <= len(query) <= 100):
        return False
    return re.fullmatch(r'[а-яА-Яa-zA-Z0-9\s]+', query) is not None

# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    help_message = (
        "Команда 💫 Поиск Royalty Free изображений позволяет вам искать изображения не "
        "ограниченные правами на использование. Поиск поддерживается на русском и английском языках.\n\n"
        "Команда 💫 Поиск Google Reverse Images реализует поиск изображений по отправленному фото.\n\n"
        "Команда 💫 Поиск Yandex Reverse Images реализует поиск изображений по отправленному фото.\n\n"
        "Каждый тип поиска доступен раз в сутки из-за ограничений хостинга.\n\n"
        "Этот бот создан в ознакомительных целях 🔎 ,и не собирает информацию в коммерческих/личных целях 🔐\n\n"
        "Для перезапуска бота вы всегда можете ввести /start\n\n"
        "Больше информации обо мне вы сможете найти посетив: https://github.com/rumiantsevaa/Bloodhound_Telegram_Bot"
    )
    bot.send_message(message.chat.id, help_message)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    user_id = message.from_user.id
    waiting_for_photo.pop(user_id, None)
    start_message = (
        "Привет, меня зовут Bloodhound, я скромный бот ищейка🔎.\n"
        "Разверните меню кнопок для выбора интересующей команды.\n"
        "Вы также можете ввести /help чтобы узнать обо мне больше.\n\n"
        "Каждый тип поиска доступен раз в сутки из-за ограничений хостинга 🖥\n"
        "Этот бот не создан в коммерческих целях и не собирает ваши данные 🔐\n"
        "Прошу отнестись с пониманием к ограничениям. Благодарю за использование моего бота 🚀🚀🚀"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Поиск Royalty Free изображений"),
        types.KeyboardButton("Поиск Google Reverse Images"),
        types.KeyboardButton("Поиск Yandex Reverse Images")
    )
    bot.send_message(message.chat.id, start_message, reply_markup=markup)

@bot.message_handler(commands=['freebhsearch'])
def free_bh_search(message):
    user_id = message.from_user.id
    waiting_for_photo.pop(user_id, None)
    if not can_use_search(user_id, 'pixabay'):
        bot.send_message(message.chat.id, "Извините, лимит на этот тип поиска исчерпан до завтра 😢")
        return
    bot.send_message(message.chat.id, "Напишите текстовый запрос желаемого royalty free фото.")
    bot.register_next_step_handler(message, process_free_bh_search)

def process_free_bh_search(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    query = message.text.strip()
    if not query or not is_valid_query(query):
        bot.send_message(chat_id, "Некорректный запрос. Используйте только буквы и цифры, длиной от 3 до 100 символов.")
        return
    search_results = perform_pixabay_search(query)
    for result in search_results:
        bot.send_message(chat_id, result)
    update_usage(user_id, 'pixabay')
    bot.send_message(chat_id,
        "Каждый тип поиска доступен раз в сутки из-за ограничений хостинга 🖥\n"
        "Этот бот не создан в коммерческих целях и не собирает ваши данные 🔐\n"
        "Для нового поиска нажмите /start")

@bot.message_handler(commands=['ultimatebhsearch'])
def ultimate_bh_search(message):
    user_id = message.from_user.id
    waiting_for_photo[user_id] = 'google_reverse'
    if not can_use_search(user_id, 'google_reverse'):
        bot.send_message(message.chat.id, "Извините, лимит на этот тип поиска исчерпан до завтра 😢")
        return
    bot.send_message(message.chat.id, "Пожалуйста, отправьте мне фото для поиска.")

@bot.message_handler(commands=['yandexbhsearch'])
def yandex_bh_search(message):
    user_id = message.from_user.id
    waiting_for_photo[user_id] = 'yandex_reverse'
    if not can_use_search(user_id, 'yandex_reverse'):
        bot.send_message(message.chat.id, "Извините, лимит на этот тип поиска исчерпан до завтра 😢")
        return
    bot.send_message(message.chat.id, "Пожалуйста, отправьте мне фото для поиска.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id not in waiting_for_photo:
        bot.send_message(chat_id,
            "Для функций поиска по изображению необходимо сначала выбрать тип поиска кнопками внизу ⤵️")
        return

    search_type = waiting_for_photo.pop(user_id)

    file_id = message.photo[-1].file_id
    file_path = bot.get_file(file_id).file_path
    photo_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"

    if not validate_image(photo_url):
        bot.send_message(chat_id, "❌ Файл не является корректным изображением или превышает допустимый размер.")
        return

    try:
        if search_type == 'google_reverse':
            results = perform_google_reverse_image_search(photo_url)
            update_usage(user_id, 'google_reverse')
        elif search_type == 'yandex_reverse':
            results = perform_yandex_reverse_image_search(photo_url)
            update_usage(user_id, 'yandex_reverse')
        else:
            bot.send_message(chat_id, "Ошибка: неизвестный тип поиска.")
            return

        for result in results:
            bot.send_message(chat_id, result)

        bot.send_message(chat_id,
            "Каждый тип поиска доступен раз в сутки из-за ограничений хостинга 🖥\n"
            "Этот бот не создан в коммерческих целях и не собирает ваши данные 🔐\n"
            "Для нового поиска нажмите /start")

    except Exception as e:
        bot.send_message(chat_id, "Произошла ошибка при обработке изображения. Попробуйте позже.")
        print(f"[ERROR] Ошибка в handle_photo: {e}")

@bot.message_handler(content_types=['document', 'video', 'audio', 'file'])
def handle_non_image_file(message):
    bot.send_message(message.chat.id,
        "Для функций поиска по изображению необходимо выбрать подходящий тип поиска кнопками внизу "
        "и приложить изображение со сжатием как фотографию. Файлы без сжатия не принимаются.")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    text = message.text.lower()
    user_id = message.from_user.id
    waiting_for_photo.pop(user_id, None)

    if text == 'поиск royalty free изображений':
        free_bh_search(message)
    elif text == 'поиск google reverse images':
        ultimate_bh_search(message)
    elif text == 'поиск yandex reverse images':
        yandex_bh_search(message)
    elif text == 'привет':
        bot.send_message(message.chat.id, "Привет! Чтобы начать, нажмите /start")
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю. Нажмите /start для списка команд.")

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"[FATAL ERROR] polling crashed: {e}")
            time.sleep(15)
