# Импорт всего для взаимодействия с тг
import telebot
from telebot import types
from config import TELEGRAM_TOKEN

from free_search import perform_pixabay_search
from ultimate_search import perform_google_reverse_image_search
from yandex_search import perform_yandex_reverse_image_search

# Создаем бота для Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    help_message = (

        "Команда 💫 Поиск Royalty Free изображений  позволяет вам искать изображения не "
        "ограниченные правами на использование. Поиск поддерживается на русском и английском языках, "
        "введите текстовый запрос, "
        "и я найду для вас соответствующие изображения с использованием Pixabay API.\n\n"
        "Команда 💫 Поиск Google Reverse Images реализует поиск изображений по отправленному фото "
        "с использованием Google Reverse Image Search API.\n\n"
        "Команда 💫 Поиск Yandex Reverse Images реализует поиск изображений по отправленному фото "
        "с использованием Yandex Reverse Image Search API.\n\n"
        "После ввода любого запроса поиска 🔎, я отправлю вам результаты отдельными сообщениями ✉️.\n\n"
        "Для перезапуска бота вы всегда можете ввести /start \n\n"
        "Больше информации обо мне вы сможете найти посетив.."
    )
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    start_message = (
        "Привет, меня зовут Bloodhound, я скромный бот ищейка🔎.\n"
        "Разверните меню кнопок для выбора интересующей команды.\n"
        "Вы также можете ввести /help чтобы узнать обо мне больше.\n"
        " \n"
        "Выбирайте кнопку и полетели🚀🚀🚀"
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
    bot.send_message(message.chat.id, "Пожалуйста, отправьте мне фото для поиска.")
    bot.register_next_step_handler(message, process_yandex_bh_search)


# Добавляем функцию обработки следующего шага
def process_next_step_yandex_bh_search(message):
    if message.text.lower() == '/start':
        start(message)
    else:
        # Если не /start, предполагаем, что это текстовый запрос для нового поиска
        process_yandex_bh_search(message)


def process_yandex_bh_search(message):
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

    # Perform Google Reverse Image Search using SerpApi
    search_results = perform_yandex_reverse_image_search(photo_url)

    # Send the search results as separate messages
    for result in search_results:
        bot.send_message(chat_id, result)

    # Спрашиваем, хочет ли пользователь выполнить повторный поиск
    bot.send_message(chat_id, "Если желаете выполнить повторный поиск, отправьте новое фото. "
                              "Или нажмите /start для выбора новой команды.")
    bot.register_next_step_handler(message, process_next_step_yandex_bh_search)


# Команда /ultimatebhsearch
@bot.message_handler(commands=['ultimatebhsearch'])
def ultimate_bh_search(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте мне фото для поиска.")
    bot.register_next_step_handler(message, process_ultimate_bh_search)


# Добавляем функцию обработки следующего шага
def process_next_step_ultimate_bh_search(message):
    if message.text.lower() == '/start':
        start(message)
    else:
        # Если не /start, предполагаем, что это текстовый запрос для нового поиска
        process_ultimate_bh_search(message)


def process_ultimate_bh_search(message):
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

    # Perform Google Reverse Image Search using SerpApi
    search_results = perform_google_reverse_image_search(photo_url)

    # Send the search results as separate messages
    for result in search_results:
        bot.send_message(chat_id, result)

    # Спрашиваем, хочет ли пользователь выполнить повторный поиск
    bot.send_message(chat_id, "Если желаете выполнить повторный поиск, отправьте новое фото. "
                              "Или нажмите /start для выбора новой команды.")
    bot.register_next_step_handler(message, process_next_step_ultimate_bh_search)


# Команда /freebhsearch
@bot.message_handler(commands=['freebhsearch'])
def free_bh_search(message):
    bot.send_message(message.chat.id, "Напишите текстовый запрос желаемого роялти фри фото.")
    bot.register_next_step_handler(message, process_free_bh_search)


def process_free_bh_search(message):
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

    # Спрашиваем, хочет ли пользователь выполнить повторный поиск
    bot.send_message(chat_id, "Если желаете выполнить повторный поиск, введите новый текстовый запрос. "
                              "Или нажмите /start для выбора новой команды.")
    bot.register_next_step_handler(message, process_next_step_free_bh_search)


def process_next_step_free_bh_search(message):
    if message.text.lower() == '/start':
        start(message)
    else:
        # Если не /start, предполагаем, что это текстовый запрос для нового поиска
        process_free_bh_search(message)


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
