import json
from mongoengine import *
from datetime import datetime

import pika



credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

exchange_name = 'My_Exchange'

channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange=exchange_name, queue='email_queue')


def create_tasks(nums: int):
    for i in range(nums):
        message = {
            'id': i,
            'payload': f"Date: {datetime.now().isoformat()}",
            'processed': False  
        }

        channel.basic_publish(exchange=exchange_name, routing_key='email_queue', body=json.dumps(message))

    connection.close()


if __name__ == '__main__':
    create_tasks(30)