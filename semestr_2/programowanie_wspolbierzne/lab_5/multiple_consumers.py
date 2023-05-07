import pika
from time import sleep
from random import randint
from sys import argv


def send(channel):
    channel.queue_declare(queue='letterbox')
    id = 1
    while True:
        msg = f'Message {id}'
        id += 1
        sleep(randint(1, 4))
        channel.basic_publish(exchange='', routing_key='letterbox', body=msg)
        print(f'Message {msg} published')


def receive(channel):
    def consume(channel, method, props, body):
        print(f'Consumer {argv[2]} received {body}')
        sleep(randint(1, 6))
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print(f'Consumer {argv[2]} finished processing {body}')

    channel.queue_declare(queue='letterbox')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='letterbox', on_message_callback=consume)
    print('Start consuming')
    channel.start_consuming()


conn_pars = pika.ConnectionParameters('localhost')
with pika.BlockingConnection(conn_pars) as conn:
    channel = conn.channel()
    if argv[1] == 'send':
        send(channel)
    else:
        receive(channel)
