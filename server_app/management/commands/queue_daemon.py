import django
from django.conf import settings
from django.core.management.base import BaseCommand
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

django.setup()

from server_app.events import OnCharacterEvent


class MessageConsumer(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=self.queues,
                callbacks=[self.on_message],
                on_decode_error=self.on_decode_error,
                accept=['msgpack'],
                tag_prefix='dev_server',
                prefetch_count=10
            )
        ]

    def on_message(self, body, message):
        # TODO validate event_type

        OnCharacterEvent.char_event(params={
            'event_type': body['event_type'],
            'data': body
        })

        message.ack()


class Command(BaseCommand):

    def handle(self, *args, **options):

        # TODO hide values in env vars and retrieve from settings module
        exchange = Exchange(settings.EXCHANGE_NAME, settings.EXCHANGE_TYPE)
        queue = settings.QUEUE
        binding_keys = [settings.ROUTING_KEY]
        queue = Queue(
            queue,
            exchange=exchange,
            bindings=binding_keys,
            no_declare=True
        )

        with Connection(**settings.AMQP) as conn:
            print('Initializing message consumption with the following config:')
            print('\nQueue: ', queue)
            print('RKs: ', binding_keys)
            print('host: ', settings.AMQP.get('hostname'))
            print('user: ', settings.AMQP.get('userid'))

            consumer = MessageConsumer(conn, queue)
            consumer.run()
