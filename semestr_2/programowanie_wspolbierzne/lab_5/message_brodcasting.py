import pika
from pika.exchange_type import ExchangeType
from sys import argv


def send(channel):
    msg = argv[2]
    channel.basic_publish(exchange=exchange, routing_key='', body=msg)
    print(f'Message {msg} published')


def receive(channel):
    name = argv[2]

    def consume(channel, method, props, body):
        print(f'Consumer {name} received message {body}')

    queue = channel.queue_declare(queue='Queue' + name, exclusive=True)
    channel.queue_bind(exchange=exchange, queue=queue.method.queue)
    channel.basic_consume(queue=queue.method.queue, auto_ack=True,
                          on_message_callback=consume)
    print('Start consuming')
    channel.start_consuming()


exchange = 'pubsub'
conn_pars = pika.ConnectionParameters('localhost')
with pika.BlockingConnection(conn_pars) as conn:
    channel = conn.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=ExchangeType.fanout)
    if argv[1] == 'send':
        send(channel)
    else:
        receive(channel)
