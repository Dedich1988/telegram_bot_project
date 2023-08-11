import telebot
from telebot import types
from telebot.types import Message
from decouple import config
import pika
import rivescript
from database import Section, Product

# Подключение к базе данных
from peewee import SqliteDatabase
db = SqliteDatabase('my_database.db')

# Создание экземпляра Rivescript
rs = rivescript.RiveScript(utf8=True)
rs.load_directory('rivescripts')
rs.sort_replies()

# Определение функции send_order
def send_order(order):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'order_queue'
    channel.queue_declare(queue=queue_name)

    # Отправка заказа в очередь
    channel.basic_publish(exchange='', routing_key=queue_name, body=order)

    connection.close()

# Получение токена бота из .env файла
BOT_TOKEN = config('BOT_TOKEN')

# Настройка бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработка команды /start
@bot.message_handler(commands=['start', 'menu'])
def handle_start(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=2)

    sections = Section.select()

    section_buttons = [section.name for section in sections]
    markup.add(*[types.KeyboardButton(text) for text in section_buttons])

    bot.send_message(user_id, "Добро пожаловать в витрину кондитерской! Выберите раздел:", reply_markup=markup)

# Обработка команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    user_id = message.from_user.id
    help_text = (
        "Привет! Я бот витрины кондитерской. Вот что я могу:\n"
        "/start - начать использование бота\n"
        "/menu - показать меню разделов\n"
        "/help - показать это сообщение справки\n"
        "/заказ - оформить заказ"
    )
    bot.send_message(user_id, help_text)

# Обработка команды /заказ
@bot.message_handler(commands=['заказ'])
def handle_order_command(message: Message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Чтобы оформить заказ, введите описание продукта в формате 'Заказ: описание продукта'.")

# Обработка описания продукта для заказа
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_order_description(message: Message):
    user_id = message.from_user.id
    user_input = message.text

    # Проверяем, что пользователь начал сообщение с "Заказ:"
    if user_input.startswith('Заказ:'):
        order_description = user_input.replace('Заказ:', '').strip()

        # Отправляем заказ в очередь RabbitMQ
        send_order(f'Заказ: {user_id} {order_description}')

        # Отправляем подтверждение пользователю
        bot.send_message(user_id, f'Ваш заказ "{order_description}" принят!')

        # Очищаем клавиатуру
        markup = types.ReplyKeyboardRemove()
        bot.send_message(user_id, "Чем еще я могу помочь?", reply_markup=markup)
    else:
        # Если описание продукта не начинается с "Заказ:", просим пользователя повторить ввод
        bot.send_message(user_id, "Чтобы оформить заказ, введите описание продукта в формате 'Заказ: описание продукта'.")

# Обработка текстовых команд
@bot.message_handler(func=lambda message: message.text in [section.name for section in Section.select()])
def handle_section(message):
    user_id = message.from_user.id
    section_name = message.text

    products = Product.select().join(Section).where(Section.name == section_name)

    for product in products:
        photo_path = f'photo/{product.photo_filename}'
        with open(photo_path, 'rb') as photo:
            bot.send_photo(user_id, photo, caption=f"{product.name}\n{product.description}")

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
