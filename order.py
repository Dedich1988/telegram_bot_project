import pika
import atexit
from telebot import types

# Создаем одно соединение при старте приложения
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
queue_name = 'order_queue'
channel.queue_declare(queue=queue_name)

def send_order(user_id, order_description):
    try:
        # Отправка заказа в очередь
        channel.basic_publish(exchange='', routing_key=queue_name, body=f'Заказ: {user_id} {order_description}')
    except Exception as e:
        # Обработка ошибок при отправке заказа
        print(f"Error sending order: {e}")

def handle_order_description(bot, message, rs, in_order_process):
    user_id = message.from_user.id
    user_input = message.text

    if user_id not in in_order_process or not in_order_process[user_id]:
        # Если пользователь не в процессе оформления заказа
        if user_input == 'заказ':
            in_order_process[user_id] = True
            bot.send_message(user_id, "Чтобы оформить заказ, введите описание продукта в формате 'Заказ: описание продукта'.")
        else:
            rs_reply = rs.reply(str(user_id), user_input)
            bot.send_message(user_id, rs_reply)
    else:
        # Если пользователь в процессе оформления заказа
        if user_input.startswith('Заказ:'):
            order_description = user_input.replace('Заказ:', '').strip()
            send_order(user_id, order_description)
            in_order_process[user_id] = False
            bot.send_message(user_id, f'Ваш заказ "{order_description}" принят!')
            markup = types.ReplyKeyboardRemove()
            bot.send_message(user_id, "Чем еще я могу помочь?", reply_markup=markup)
        else:
            bot.send_message(user_id, "Чтобы оформить заказ, введите описание продукта в формате 'Заказ: описание продукта'.")

# Дополнительный код

# Закрываем соединение при завершении приложения
atexit.register(lambda: connection.close())
