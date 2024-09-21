from typing import Callable, List

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


class KafkaBase:
    def __init__(self, kafka_servers: str):
        self._kafka_servers = kafka_servers


class KafkaProducer(KafkaBase):
    def __init__(self, kafka_servers: str):
        super().__init__(kafka_servers)
        self._producer = AIOKafkaProducer(bootstrap_servers=self._kafka_servers)

    async def start(self):
        await self._producer.start()

    async def send_message(self, topic: str, value: bytes):
        await self._producer.send_and_wait(topic, value)

    async def stop(self):
        await self._producer.stop()


class KafkaConsumer(KafkaBase):
    def __init__(self, kafka_servers: str, topics: List[str]):
        super().__init__(kafka_servers)
        self._consumer = AIOKafkaConsumer(
            *topics, bootstrap_servers=self._kafka_servers
        )
        self._handlers = {}

    def register_handler(self, topic: str, handler: Callable):
        self._handlers[topic] = handler

    async def start(self):
        await self._consumer.start()
        async for message in self._consumer:
            topic = message.topic
            if topic in self._handlers:
                await self._handlers[topic](message)

    async def stop(self):
        await self._consumer.stop()
