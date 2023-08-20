import telebot
import datetime
from telebot import types
from decouple import config
import rivescript
from order import handle_order_description
import menu
from database import Section, Product, User, UserSession

# Создание экземпляра Rivescript
rs = rivescript.RiveScript(utf8=True)
rs.load_directory('rivescripts')
rs.sort_replies()

# Получение токена бота из .env файла
BOT_TOKEN = config('BOT_TOKEN')

# Настройка бота
bot = telebot.TeleBot(BOT_TOKEN)




# В этой функции обработки команды /start или первого взаимодействия пользователя с ботом
def handle_start(message):
    user_id = str(message.from_user.id)
    time_entered = datetime.datetime.now()

    # Сохраняем данные пользователя в базе данных
    User.create(user_id=user_id, created_at=datetime.datetime.now())  # Используйте created_at вместо time_entered





# Обработка команд /start, /menu и /help
@bot.message_handler(commands=['start', 'menu', 'help'])
def handle_commands(message):
    help_text = """
    Ваш бот поддерживает следующие команды и фразы:

    /start: Приветствие и начало работы с ботом.
    /menu: Отображение меню товаров.
    /help: Отображение справочной информации о боте.
    заказ или оформить заказ: Начало процесса оформления заказа.
    покажи ассортимент, просмотреть продукцию, открыть меню товаров или показать что есть в магазине: Отображение списка товаров.
    кто тебя создал: Информация о создателе бота.
    """

    if message.text == '/start':
        bot.send_message(message.chat.id, "Приветствую вас в фермерском магазине 'Натуральное изобилие'! Чтобы посмотреть наши товары, вам достаточно написать одну из следующих фраз:\n\n- 'Покажи ассортимент'\n- 'Просмотреть продукцию'\n- 'Открыть меню товаров'\n- 'Показать что есть в магазине'\n\nВыберите удобный вариант, и я с удовольствием покажу вам наш богатый выбор натуральных продуктов!")
        menu.show_start(bot, message)
    elif message.text == '/menu':
        menu.show_menu(bot, message)
    elif message.text == '/help':
        bot.send_message(message.chat.id, help_text)

in_order_process = {}  # Initialize the in_order_process dictionary

# ...

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message: telebot.types.Message):
    user_id = message.from_user.id
    user_input = message.text

    # Загружаем или создаем сессию
    user, created = User.get_or_create(user_id=user_id)
    session, _ = UserSession.get_or_create(user=user)

    # Получаем контекст сессии
    context = session.context

    if user_id in in_order_process and in_order_process[user_id]:
        handle_order_description(bot, message, rs, in_order_process)
    else:
        # Обработка текстовых команд через RiveScript
        rs_reply = rs.reply(str(user_id), user_input)

        if "{request_order_description}" in rs_reply:
            in_order_process[user_id] = True
            handle_order_description(bot, message, rs, in_order_process)
        elif "{show_menu}" in rs_reply:
            # Вызов функции для отображения меню
            menu.show_menu(bot, message)
        elif rs_reply.startswith("{show_products}"):
            section_name = rs_reply.split()[1]
            menu.show_products(bot, message, section_name)
        elif Section.select().where(Section.name == user_input).exists():
            menu.show_products(bot, message, user_input)  # Вызов функции для отображения продуктов данной секции
        else:
            # Отправка ответа RiveScript пользователю
            bot.send_message(user_id, rs_reply)

        # Сохраняем значение текста сообщения пользователя в качестве контекста
        if context:
            session.context = context + '\n' + user_input
        else:
            session.context = user_input
        session.save()

# Запуск бота
bot.polling(none_stop=True)

