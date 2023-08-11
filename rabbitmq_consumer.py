import pika
from database import Order

def callback(ch, method, properties, body):
    # Получение описания заказа из тела сообщения
    order_description = body.decode()

    # Разделение ид пользователя и описания заказа
    user_id, description = order_description.split(' ', 1)

    # Сохранение заказа в базе данных
    Order.create(user_id=user_id, description=description)

    print(f"Received order from user {user_id}: {description}")

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue_name = 'order_queue'
channel.queue_declare(queue=queue_name)

# Установка функции обратного вызова для обработки заказов
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Waiting for orders...')
channel.start_consuming()
