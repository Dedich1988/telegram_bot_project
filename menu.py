from telebot import types
from database import Section, Product
import os
def show_start(bot, message):
    sections = Section.select()

    for section in sections:
        photo_path = f'photo/{section.photo_filename}'
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=section.name)

def show_menu(bot, message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    sections = Section.select()

    for section in sections:
        markup.add(types.KeyboardButton(section.name))

    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=markup)
import os

# ...

def show_products(bot, message, section_name):
    user_id = message.from_user.id
    products = Product.select().join(Section).where(Section.name == section_name)

    if products:
        for product in products:
            photo_path = os.path.join('photo', product.photo_filename.replace('/', os.sep))
            print("Attempting to open:", photo_path)  # Debug line
            try:
                with open(photo_path, 'rb') as photo:
                    bot.send_photo(user_id, photo, caption=f"{product.name}\n{product.description}")
            except FileNotFoundError as e:
                print("File not found:", e)
    else:
        bot.send_message(user_id, "В этом разделе нет продуктов")


