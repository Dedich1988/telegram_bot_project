# bot.py

import telebot
from telebot import types
from decouple import config
import rivescript
from order import handle_order_description
import menu
from database import Section, Product

# Создание экземпляра Rivescript
rs = rivescript.RiveScript(utf8=True)
rs.load_directory('rivescripts')
rs.sort_replies()

# Получение токена бота из .env файла
BOT_TOKEN = config('BOT_TOKEN')

# Настройка бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработка команд /start, /menu и /help
@bot.message_handler(commands=['start', 'menu', 'help'])
def handle_commands(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Приветствую вас в фермерском магазине 'Натуральное изобилие'! Чтобы посмотреть наши товары, вам достаточно написать одну из следующих фраз:\n\n- 'Покажи ассортимент'\n- 'Просмотреть продукцию'\n- 'Открыть меню товаров'\n- 'Показать что есть в магазине'\n\nВыберите удобный вариант, и я с удовольствием покажу вам наш богатый выбор натуральных продуктов!")
        menu.show_start(bot, message)
    elif message.text == '/menu':
        menu.show_menu(bot, message)
    elif message.text == '/help':
        bot.send_message(message.chat.id, 'This is the help message.')

# Обработка описания продукта для заказа и текстовых команд через RiveScript
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message: telebot.types.Message):
    user_id = message.from_user.id
    user_input = message.text

    # Обработка описания продукта для заказа
    if user_input.startswith('/order'):
        handle_order_description(bot, message, rs)

    # Обработка текстовых команд через RiveScript
    rs_reply = rs.reply(str(user_id), user_input)

    # Вызов функций меню через маркеры RiveScript
    if "{show_menu}" in rs_reply:
        # Вызов функции для отображения меню
        menu.show_menu(bot, message)
    elif rs_reply.startswith("{show_products}"):
        section_name = rs_reply.split()[1]
        menu.show_products(bot, message, section_name)

    # Добавляем проверку, если сообщение точно соответствует имени раздела
    elif Section.select().where(Section.name == user_input).exists():
        menu.show_products(bot, message, user_input)  # Вызов функции для отображения продуктов данной секции

    else:
        # Отправка ответа RiveScript пользователю
        bot.send_message(user_id, rs_reply)

# Запуск бота
bot.polling(none_stop=True)
