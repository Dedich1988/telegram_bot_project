from telebot import TeleBot, types
from database import Section, Product

from peewee import CharField, ForeignKeyField, TextField, Model
from playhouse.db_url import connect

# Подключение к базе данных
db = connect('sqlite:///my_database.db')


def show_menu(user_id, bot):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    sections = Section.select()
    section_buttons = [section.name for section in sections]
    markup.add(*[types.KeyboardButton(text) for text in section_buttons])
    bot.send_message(user_id, "Выберите раздел:", reply_markup=markup)


def get_section_list():
    sections = Section.select()
    section_list = " ".join([section.name for section in sections])
    return "У нас есть следующие разделы: " + section_list


def get_products_list(user_id, section_name):
    products = Product.select().join(Section).where(Section.name == section_name)
    product_list = []
    for product in products:
        photo_path = f'photo/{product.photo_filename}'
        with open(photo_path, 'rb') as photo:
            bot.send_photo(user_id, photo, caption=f"{product.name}\n{product.description}")
        product_list.append(product.name)
    return "В разделе " + section_name + " у нас есть следующие продукты: " + ", ".join(product_list)