import logging
import uuid
from enum import Enum

import pika

from utils.general.logger import Logger

logger = logging.getLogger('django')


class RabbitHelper:
    rabbit = None
    connection = None
    channel = None

    class Exchanges(Enum):
        USER_MANAGEMENT = 'user_management'

    def __init__(self):
        self._connect()
        self.create_exchange()

    def _connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_URL))
            self.channel = self.connection.channel()
            Logger.info(logger, 'Successfully connected to rabbit queue', title='rabbit')
        except Exception as e:
            Logger.error(logger, str(e), title='rabbit')

    def create_exchange(self):
        self.channel.exchange_declare(exchange=self.Exchanges.USER_MANAGEMENT.value, exchange_type='fanout')

    def create_queue(self, extension_name) -> str:
        queue_key = f'{extension_name}_{uuid.uuid4()}'
        self.channel.queue_declare(queue=queue_key, durable=True)
        self.bind_queue(queue_key)
        return queue_key

    def bind_queue(self, queue_key=None):
        self.channel.queue_bind(exchange=self.Exchanges.USER_MANAGEMENT.value, queue=queue_key)

    def publish(self, exchange, message):
        try:
            Logger.info(logger, 'publish message to exchange started', title='rabbit')
            self.channel.basic_publish(exchange=exchange, routing_key='', body=message)
        except Exception as e:
            Logger.error(logger, str(e), title='rabbit publish')
            self._connect()
            self.bind_queue()
            self.channel.basic_publish(exchange=exchange, routing_key='', body=message)

    def close(self):
        self.connection.close()


rabbit = RabbitHelper()
