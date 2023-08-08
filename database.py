from peewee import *

# Создание подключения к базе данных (подставьте свои настройки)
db = SqliteDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

# Модель для разделов
class Section(BaseModel):
    name = CharField(unique=True)

# Модель для товаров
class Product(BaseModel):
    section = ForeignKeyField(Section, backref='products')
    name = CharField()
    description = TextField()
    photo_filename = CharField()  # Здесь будет храниться имя файла фотографии

# Создание таблиц в базе данных (вызывается один раз при инициализации)
db.connect()
db.create_tables([Section, Product])
db.close()
