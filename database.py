from peewee import *
from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    'dd',  # Название вашей PostgreSQL базы данных
    user='postgres',  # Ваше имя пользователя PostgreSQL
    password='admin',  # Ваш пароль пользователя PostgreSQL
    host='localhost'  # Адрес вашей PostgreSQL базы данных
)


class BaseModel(Model):
    class Meta:
        database = db

class Section(BaseModel):
    name = CharField(unique=True)
    photo_filename = CharField()

class Product(BaseModel):
    section = ForeignKeyField(Section, backref='products')
    name = CharField()
    description = TextField()
    photo_filename = CharField()
    quantity = IntegerField(default=0)

class Order(BaseModel):
    user_id = CharField()
    description = TextField()

db.connect()

# Create tables if they don't exist
db.create_tables([Section, Product, Order])

# Function to create test data
# def create_test_data():
#     with db.atomic():
#         section1 = Section.create(name='Мед и продукты пчеловодства', photo_filename='menu/photo/honey.jpg')
#         section2 = Section.create(name='Гусеводство', photo_filename='menu/photo/geese.jpg')
#         section3 = Section.create(name='Виноградарство', photo_filename='menu/photo/grapes.jpg')
#         section4 = Section.create(name='Разные товары', photo_filename='menu/photo/miscellaneous.jpg')
#
#         # Create products using existing section records
#         Product.create(section=section1, name='Мед натуральный', description='Свежий натуральный мед',
#                        photo_filename='honey.jpg', quantity=100)
#         Product.create(section=section1, name='С', description='Полезная пчелиная перга',
#                        photo_filename='perga.jpg', quantity=50)
#
#         Product.create(section=section2, name='Гусиные яйца', description='Свежие яйца гусят',
#                        photo_filename='geese_eggs.jpg', quantity=200)
#         Product.create(section=section2, name='Гусята', description='Суточные гусята', photo_filename='goslings.jpg',
#                        quantity=30)
#
#         Product.create(section=section3, name='Черенки винограда', description='Черенки винограда',
#                        photo_filename='grape_cuttings.jpg', quantity=200)
#
#         Product.create(section=section4, name='Иван-чай (кипрей)', description='Иван-чай - натуральный продукт',
#                        photo_filename='fireweed.jpg', quantity=200)
#
# # Call the function to create test data
# create_test_data()
