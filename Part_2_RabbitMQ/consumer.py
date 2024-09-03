import json
import os
import sys
import time
from models import Contact

import pika


def send_email(contact_id):
    contact = Contact.objects.with_id(contact_id)
    if contact:
        print(f"Email has been sent to: {contact.fullname}")
        contact.message_sent = True
        contact.save()

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue', durable=True)

    def callback(ch, method, properties, body):
        contact_id = json.loads(body.decode())
        print(f" [x] Received {contact_id}")
        send_email(contact_id)
        print(f" [x] Completed {method.delivery_tag} task")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)