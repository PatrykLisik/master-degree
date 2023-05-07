import pika
from sys import argv
from uuid import uuid4


def client(channel):
    def consume_reply(channel, method, props, body):
        print(f'Reply: {body}, Correlation: {props.correlation_id}')
        channel.stop_consuming()

    msg = argv[2]
    reply_queue = channel.queue_declare(queue='', exclusive=True)
    channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True,
                          on_message_callback=consume_reply)
    corr_id = str(uuid4())
    props = pika.BasicProperties(reply_to=reply_queue.method.queue,
                                 correlation_id=corr_id)
    channel.basic_publish(exchange='', routing_key='request-queue',
                          body=msg, properties=props)
    print(f'Message {msg} published, with correlation {corr_id} waiting for reply')
    channel.start_consuming()


def server(channel):
    def consume_request(channel, method, props, body):
        print(f'Request: {body}, Correlation: {props.correlation_id}')
        props1 = pika.BasicProperties(correlation_id=props.correlation_id)
        channel.basic_publish(exchange='', routing_key=props.reply_to,
                              body='Reply to request', properties=props1)

    channel.basic_consume(queue='request-queue', auto_ack=True,
                          on_message_callback=consume_request)
    print('Waiting for messages ...')
    channel.start_consuming()


conn_pars = pika.ConnectionParameters('localhost')
with pika.BlockingConnection(conn_pars) as conn:
    channel = conn.channel()
    channel.queue_declare(queue='request-queue')
    if argv[1] == 'client':
        client(channel)
    else:
        server(channel)
