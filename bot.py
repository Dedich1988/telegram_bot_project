import telebot
from telebot import types
from decouple import config
import pika
import peewee
import rivescript
from database import Section, Product  # Импортируйте модели для разделов и товаров

# Подключение к базе данных (замените на свой путь и имя базы данных)
from peewee import SqliteDatabase
db = SqliteDatabase('my_database.db')

# Создание экземпляра Rivescript
rs = rivescript.RiveScript(utf8=True)
rs.load_directory('rivescripts')
rs.sort_replies()

# Получение токена бота из .env файла
BOT_TOKEN = config('BOT_TOKEN')

# Настройка бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=2)

    # Получение списка разделов из базы данных
    sections = Section.select()

    # Создание кнопок с разделами
    section_buttons = [section.name for section in sections]
    markup.add(*[types.KeyboardButton(text) for text in section_buttons])

    bot.send_message(user_id, "Добро пожаловать в витрину кондитерской! Выберите раздел:", reply_markup=markup)

# Обработка текстовых команд
@bot.message_handler(func=lambda message: message.text in [section.name for section in Section.select()])
def handle_section(message):
    user_id = message.from_user.id
    section_name = message.text

    # Получение товаров выбранного раздела из базы данных
    products = Product.select().join(Section).where(Section.name == section_name)

    for product in products:
        # Отправка информации о товаре и фотографии
        # Примечание: URL фотографии будет зависеть от настроек сервера
        photo_url = f"https://your-droplet-url.com/photos/{product.photo_filename}"

        bot.send_photo(user_id, photo_url, caption=f"{product.name}\n{product.description}")

# Обработка всех остальных сообщений через Rivescript
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_input = message.text

    # Получение ответа от Rivescript
    reply = rs.reply(str(user_id), user_input)

    # Отправка ответа пользователю
    bot.send_message(user_id, reply)

# Запуск бота
bot.polling(none_stop=True)
