import telebot
from telebot import types
from decouple import config
import rivescript
from order import send_order, handle_order_description
from menu import show_menu, get_products_list  # Импорт функций из модуля menu

in_order_process = {}

# Создание экземпляра Rivescript
rs = rivescript.RiveScript(utf8=True)
rs.load_directory('rivescripts')
rs.sort_replies()

# Получение токена бота из .env файла
BOT_TOKEN = config('BOT_TOKEN')

# Настройка бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработка описания продукта для заказа

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_order(message: telebot.types.Message):
    handle_order_description(bot, message, rs, in_order_process)   # Передача аргумента in_order_process

# Обработка текстовых команд через RiveScript
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message: telebot.types.Message):
    user_id = message.from_user.id
    user_input = message.text
    rs_reply = rs.reply(str(user_id), user_input)

    if rs_reply.startswith("{show_menu}"):
        # Вызов функции для отображения меню
        show_menu(user_id)
    elif rs_reply.startswith("{get_section_list}"):
        # Вызов функции для получения списка разделов
        section_list = get_section_list()
        bot.send_message(user_id, section_list)
    elif rs_reply.startswith("{get_products_list}"):
        # Вызов функции для получения списка продуктов
        section_name = rs_reply.split()[1]  # Получаем имя раздела из ответа RiveScript
        product_list = get_products_list(user_id, section_name)
        bot.send_message(user_id, product_list)
    else:
        # Отправка ответа RiveScript пользователю
        bot.send_message(user_id, rs_reply)

# Запуск бота
bot.polling(none_stop=True)
