from django.conf import settings
from kombu import Connection, Exchange


def publish_message(payload):
    rk = settings.ROUTING_KEY
    ex = Exchange(settings.EXCHANGE_NAME, settings.EXCHANGE_TYPE)

    with Connection(**settings.AMQP) as conn:
        producer = conn.Producer(serializer='msgpack')
        producer.publish(payload, exchange=ex, routing_key=rk)
