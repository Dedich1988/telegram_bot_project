from telebot import types
from database import Section, Product

def show_menu(bot, message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=2)
    sections = Section.select()
    section_buttons = [section.name for section in sections]
    markup.add(*[types.KeyboardButton(text) for text in section_buttons])
    bot.send_message(user_id, "Выберите раздел:", reply_markup=markup)

def show_products(bot, message, section_name):
    user_id = message.from_user.id
    products = Product.select().join(Section).where(Section.name == section_name)
    if products:
        for product in products:
            photo_path = f'photo/{product.photo_filename}'
            with open(photo_path, 'rb') as photo:
                bot.send_photo(user_id, photo, caption=f"{product.name}\n{product.description}")
    else:
        bot.send_message(user_id, "В этом разделе нет продуктов")
