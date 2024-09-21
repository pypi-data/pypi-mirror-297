from .decorators import kafka_endpoint
from .kafka_base import KafkaConsumer, KafkaProducer


class KafkaService:
    def __init__(self, kafka_servers: str):
        self.producer = KafkaProducer(kafka_servers)
        self.consumer = KafkaConsumer(kafka_servers, [])

    def register_endpoint(self, handler, incoming_topic: str, outgoing_topic: str):
        self.consumer.register_handler(incoming_topic, handler)
        # Сохраняем информацию для дальнейшего использования в отправке ответов

    async def start(self):
        await self.producer.start()
        await self.consumer.start()

    async def stop(self):
        await self.producer.stop()
        await self.consumer.stop()
