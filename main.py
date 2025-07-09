# Импорт всего для взаимодействия с тг
import telebot
from telebot import types
from config import TELEGRAM_TOKEN

from free_search import perform_pixabay_search
from ultimate_search import perform_google_reverse_image_search
from yandex_search import perform_yandex_reverse_image_search
from db import init_db, can_use_search, update_usage

init_db()

# Создаем бота для Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)


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
    start_message = (
        "Привет, меня зовут Bloodhound, я скромный бот ищейка🔎.\n"
        "Разверните меню кнопок для выбора интересующей команды.\n"
        "Вы также можете ввести /help чтобы узнать обо мне больше.\n\n"
        "Каждый тип поиска доступен раз в сутки из-за ограничений хостинга 🖥\n"
        "Этот бот не создан в коммерческих целях и не собирает ваши данные 🔐\n"
        "Прошу отнестись с пониманием к ограничениям. Благодарю за использование моего бота 🚀🚀🚀"
    )

    # Создаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Поиск Royalty Free изображений")
    button2 = types.KeyboardButton("Поиск Google Reverse Images")
    button3 = types.KeyboardButton("Поиск Yandex Reverse Images")
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, start_message, reply_markup=markup)


# Команда /yandexbhsearch
@bot.message_handler(commands=['yandexbhsearch'])
def yandex_bh_search(message):
    user_id = message.from_user.id
    if not can_use_search(user_id, 'yandex_reverse'):
        bot.send_message(message.chat.id, "Извините, лимит на этот тип поиска исчерпан до завтра 😢")
        return
    bot.send_message(message.chat.id, "Пожалуйста, отправьте мне фото для поиска.")
    bot.register_next_step_handler(message, process_yandex_bh_search)


def process_yandex_bh_search(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if the user sent a photo
    if not message.photo:
        bot.send_message(chat_id, "Пожалуйста, отправьте фото.")
        return

    # Get the file_id of the largest photo
    file_id = message.photo[-1].file_id

    # Get the file path using file_id
    file_path = bot.get_file(file_id).file_path

    # Construct the public URL for the photo
    photo_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"

    # Perform Yandex Reverse Image Search using SerpApi
    search_results = perform_yandex_reverse_image_search(photo_url)

    # Send the search results as separate messages
    for result in search_results:
        bot.send_message(chat_id, result)

    update_usage(user_id, 'yandex_reverse')  # Обновляем дату использования

    info_message = (
        "Каждый тип поиска доступен раз в сутки из-за ограничений хостинга 🖥\n"
        "Этот бот не создан в коммерческих целях и не собирает ваши данные 🔐 \n"
        "Прошу отнестись с пониманием к ограничениям. Благодарю за использование моего бота 🚀\n\n"
        "Для нового поиска нажмите /start"
    )
    bot.send_message(chat_id, info_message)


# Команда /ultimatebhsearch
@bot.message_handler(commands=['ultimatebhsearch'])
def ultimate_bh_search(message):
    user_id = message.from_user.id
    if not can_use_search(user_id, 'google_reverse'):
        bot.send_message(message.chat.id, "Извините, лимит на этот тип поиска исчерпан до завтра 😢")
        return
    bot.send_message(message.chat.id, "Пожалуйста, отправьте мне фото для поиска.")
    bot.register_next_step_handler(message, process_ultimate_bh_search)


def process_ultimate_bh_search(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if the user sent a photo
    if not message.photo:
        bot.send_message(chat_id, "Пожалуйста, отправьте фото.")
        return

    # Get the file_id of the largest photo
    file_id = message.photo[-1].file_id

    # Get the file path using file_id
    file_path = bot.get_file(file_id).file_path

    # Construct the public URL for the photo
    photo_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"

    # Perform Google Reverse Image Search
    search_results = perform_google_reverse_image_search(photo_url)

    # Send the search results as separate messages
    for result in search_results:
        bot.send_message(chat_id, result)

    update_usage(user_id, 'google_reverse')  # Обновляем дату использования

    info_message = (
        "Каждый тип поиска доступен раз в сутки из-за ограничений хостинга 🖥\n"
        "Этот бот не создан в коммерческих целях и не собирает ваши данные 🔐 \n"
        "Прошу отнестись с пониманием к ограничениям. Благодарю за использование моего бота 🚀\n\n"
        "Для нового поиска нажмите /start"
    )
    bot.send_message(chat_id, info_message)


# Команда /freebhsearch
@bot.message_handler(commands=['freebhsearch'])
def free_bh_search(message):
    user_id = message.from_user.id
    if not can_use_search(user_id, 'pixabay'):
        bot.send_message(message.chat.id, "Извините, лимит на этот тип поиска исчерпан до завтра 😢")
        return
    bot.send_message(message.chat.id, "Напишите текстовый запрос желаемого royalty free фото.")
    bot.register_next_step_handler(message, process_free_bh_search)


def process_free_bh_search(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    query = message.text

    # Check if the user provided a non-empty query
    if not query:
        bot.send_message(chat_id, "Мне не удалось выполнить ваш запрос. Пожалуйста, введите текстовый запрос.")
        return

    # Perform Pixabay search
    search_results = perform_pixabay_search(query)

    # Send each link as a separate message
    for result in search_results:
        bot.send_message(chat_id, result)

    update_usage(user_id, 'pixabay')  # Обновляем дату использования

    info_message = (
        "Каждый тип поиска доступен раз в сутки из-за ограничений хостинга 🖥\n"
        "Этот бот не создан в коммерческих целях и не собирает ваши данные 🔐 \n"
        "Прошу отнестись с пониманием к ограничениям. Благодарю за использование моего бота 🚀\n\n"
        "Для нового поиска нажмите /start"
    )
    bot.send_message(chat_id, info_message)


# Обработка любых текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text.lower() == 'поиск royalty free изображений':
        free_bh_search(message)
    elif message.text.lower() == 'поиск google reverse images':
        ultimate_bh_search(message)
    elif message.text.lower() == 'поиск yandex reverse images':
        yandex_bh_search(message)
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет! Чтобы начать, нажмите /start")
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю. Нажмите /start для списка команд.")


# Start the bot polling
bot.polling(none_stop=True, interval=0)
