import telebot
from decouple import config
import rivescript
from order import handle_order_description
import menu
from database import Section

# Создание экземпляра Rivescript
rs = rivescript.RiveScript(utf8=True)
rs.load_directory('rivescripts')
rs.sort_replies()

# Получение токена бота из .env файла
BOT_TOKEN = config('BOT_TOKEN')

# Настройка бота
bot = telebot.TeleBot(BOT_TOKEN)

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

# Обработка выбора секции через обработчик
@bot.message_handler(func=lambda message: message.text in [section.name for section in Section.select()])
def handle_section_choice(message):
    section_name = message.text
    menu.show_products(bot, message, section_name)

# Запуск бота
bot.polling(none_stop=True)
