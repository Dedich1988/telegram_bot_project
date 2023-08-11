from peewee import *

db = SqliteDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class Section(BaseModel):
    name = CharField(unique=True)

class Product(BaseModel):
    section = ForeignKeyField(Section, backref='products')
    name = CharField()
    description = TextField()
    photo_filename = CharField()


class Order(BaseModel):  # Добавляем определение класса Order
    user_id = CharField()
    description = TextField()



#Создаем тестовые продукты в базе данных
# def create_test_data():
#     with db.atomic():
#         section1 = Section.create(name='Торты и пирожные')
#         section2 = Section.create(name='Печенье и выпечка')
#
#         product1 = Product.create(section=section1, name='Торт "Шоколадное наслаждение"', description='Вкусный шоколадный торт', photo_filename='chocolate_cake.jpg')
#         product2 = Product.create(section=section1, name='Пирожное "Тирамису"', description='Нежное пирожное с кофейным вкусом', photo_filename='tiramisu.jpg')
#         product3 = Product.create(section=section2, name='Печенье "Овсянка"', description='Печенье с овсянкой и изюмом', photo_filename='oatmeal_cookies.jpg')

db.connect()
db.create_tables([Section, Product])
