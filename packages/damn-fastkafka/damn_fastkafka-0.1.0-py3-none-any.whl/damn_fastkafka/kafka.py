import asyncio
from typing import Any, Dict, Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError
from aiologger import Logger

from .exceptions import KafkaConnectionError, KafkaProcessingError
from .serialization import Serializer


class KafkaClient:
    """Kafka client to manage producer and consumer lifecycle."""

    def __init__(
        self,
        kafka_broker: str,
        logger: Logger,
        serializer: Serializer,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        """
        Initialize Kafka client with broker, logger, and serializer.

        :param kafka_broker: Kafka broker address (e.g., localhost:9092).
        :param logger: Asynchronous logger instance.
        :param serializer: Serializer instance (e.g., JsonSerializer, AvroSerializer).
        :param max_retries: Maximum number of retries for sending a message.
        :param retry_delay: Delay between retries in seconds.
        """
        self.kafka_broker = kafka_broker
        self.producer = None
        self.logger = logger
        self.serializer = serializer
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.consumers = []

    async def start(self):
        """Start the Kafka producer and registered consumers."""
        try:
            self.producer = AIOKafkaProducer(bootstrap_servers=self.kafka_broker)
            await self.producer.start()
            await self.logger.info("Kafka producer started")
            for consumer in self.consumers:
                asyncio.create_task(consumer())
        except Exception as e:
            await self.logger.error(f"Failed to start Kafka producer or consumers: {e}")
            raise KafkaConnectionError("Failed to connect to Kafka broker")

    async def stop(self):
        """Stop the Kafka producer."""
        if self.producer:
            await self.producer.stop()
            await self.logger.info("Kafka producer stopped")

    async def send_message(
        self, topic: str, message: dict, headers: Optional[Dict[str, Any]] = None
    ):
        """
        Serialize and send a message to the specified Kafka topic with optional headers.

        :param topic: The Kafka topic to send the message to.
        :param message: The message to be sent as a dictionary.
        :param headers: Optional dictionary of message headers.
        """
        serialized_message = self.serializer.serialize(message)
        try:
            await self.producer.send_and_wait(
                topic, serialized_message, headers=headers
            )
            await self.logger.info(f"Message successfully sent to topic {topic}")
        except KafkaError as e:
            await self.logger.error(f"Error sending message to {topic}: {e}")
            raise KafkaConnectionError(f"Failed to send message to topic {topic}")

    async def send_message_with_retries(
        self, topic: str, message: dict, headers: Optional[Dict[str, Any]] = None
    ):
        """
        Send a message to Kafka with retries in case of failure.

        :param topic: The Kafka topic to send the message to.
        :param message: The message to be sent as a dictionary.
        :param headers: Optional dictionary of message headers.
        """
        attempt = 0
        while attempt < self.max_retries:
            try:
                await self.send_message(topic, message, headers)
                return  # Success, exit the loop
            except KafkaConnectionError as e:
                attempt += 1
                if attempt < self.max_retries:
                    await self.logger.warning(
                        f"Retrying to send message to {topic}. Attempt {attempt}/{self.max_retries}"
                    )
                    await asyncio.sleep(self.retry_delay)
                else:
                    await self.logger.error(
                        f"Failed to send message after {self.max_retries} attempts"
                    )
                    raise e
