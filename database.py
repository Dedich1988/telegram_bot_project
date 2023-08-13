from peewee import *

db = SqliteDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class Section(BaseModel):
    name = CharField(unique=True)
    photo_filename = CharField()  # Добавляем поле для хранения имени файла с фотографией

class Product(BaseModel):
    section = ForeignKeyField(Section, backref='products')
    name = CharField()
    description = TextField()
    photo_filename = CharField()

class Order(BaseModel):
    user_id = CharField()
    description = TextField()

db.connect()
# db.create_tables([Section, Product, Order])

# Создаем тестовые разделы с фотографиями в базе данных
# Добавляем разделы в базу данных
# def create_test_data():
#     with db.atomic():
#         section1 = Section.create(name='Мед и продукты пчеловодства', photo_filename='menu/photo/honey.jpg')
#         section2 = Section.create(name='Гусеводство', photo_filename='menu/photo/geese.jpg')
#         section3 = Section.create(name='Виноградарство', photo_filename='menu/photo/grapes.jpg')
#         section4 = Section.create(name='Разные товары', photo_filename='menu/photo/miscellaneous.jpg')
#
#
# # Вызываем функцию для создания тестовых данных
# create_test_data()
