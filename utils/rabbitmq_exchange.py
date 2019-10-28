import pika

from common import Singleton


class Reader:
    def __init__(self, uuid: str, host: str = 'localhost', port: int = 5672, credentials=None):
        if credentials is None:
            credentials = ['guest', 'guest']
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(*credentials)
        self.uuid = uuid

    def receive_msg(self):
        res = []
        count = 0
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials))
            channel = connection.channel()
            channel.exchange_declare(exchange='cpu_util', exchange_type='direct', durable=False)

            result = channel.queue_declare(queue=self.uuid, exclusive=False, arguments={'x-expires': 30000})
            queue_name = result.method.queue

            channel.queue_bind(exchange='cpu_util', queue=queue_name, routing_key='cpu')

            for method, properties, body in channel.consume(queue=queue_name, auto_ack=True, inactivity_timeout=5):
                if body is None:
                    channel.cancel()
                    channel.close()
                    break
                if count == 0:
                    count = channel.get_waiting_message_count() + 1

                res.append(body.decode('utf-8'))

                if channel.get_waiting_message_count() == 0:
                    channel.cancel()
                    channel.close()
                    break
        except (pika.exceptions.AMQPConnectionError,
                pika.exceptions.ConnectionClosedByBroker,
                pika.exceptions.AMQPChannelError) as exc:
            print(f'<Reader>: {repr(exc)}')
        finally:
            return res


class Sender(metaclass=Singleton):
    def __init__(self, host: str = 'localhost', port: int = 5672, credentials=None):
        if credentials is None:
            credentials = ['guest', 'guest']
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(*credentials)

    def send_msg(self, msg: str):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials))
            channel = connection.channel()

            channel.exchange_declare(exchange='cpu_util', exchange_type='direct')

            channel.basic_publish(
                exchange='cpu_util', routing_key='cpu', body=msg)
            connection.close()
        except (pika.exceptions.AMQPConnectionError,
                pika.exceptions.ConnectionClosedByBroker,
                pika.exceptions.AMQPChannelError) as exc:
            print(f'<Sender>: {repr(exc)}')
            pass
