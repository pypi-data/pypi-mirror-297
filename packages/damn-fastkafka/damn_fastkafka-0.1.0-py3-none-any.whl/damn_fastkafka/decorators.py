import logging
from typing import Callable, Type

from aiokafka import AIOKafkaConsumer
from exceptions import KafkaProcessingError
from models import BaseKafkaModel
from pydantic import ValidationError

logger = logging.getLogger(__name__)


def kafka_listener(
    incoming_topic: str,
    outgoing_topic: str,
    incoming_schema: Type[
        BaseKafkaModel
    ],  # Обязательно наследоваться от BaseKafkaModel
    outgoing_schema: Type[BaseKafkaModel],
):
    """
    Decorator to register a function that listens to a Kafka topic and processes messages.

    :param incoming_topic: Kafka topic to consume messages from.
    :param outgoing_topic: Kafka topic to send processed messages to.
    :param incoming_schema: Pydantic schema for validating incoming data, inheriting from BaseKafkaModel.
    :param outgoing_schema: Pydantic schema for validating outgoing data, inheriting from BaseKafkaModel.
    """

    def decorator(func: Callable):
        async def wrapper(self: "KafkaClient"):
            consumer = AIOKafkaConsumer(
                incoming_topic,
                bootstrap_servers=self.kafka_broker,
                group_id=f"{incoming_topic}_group",
            )
            await consumer.start()
            await self.logger.info(f"Consumer started for topic {incoming_topic}")

            try:
                async for msg in consumer:
                    try:
                        # Validate incoming data
                        data = incoming_schema.parse_raw(msg.value)
                        await self.logger.debug(
                            f"Message received from {incoming_topic}: {data}"
                        )

                        # Process the message with the decorated function
                        result = await func(data)

                        # Validate outgoing data
                        validated_result = outgoing_schema(**result)

                        # Send the result to the outgoing topic
                        await self.send_message(outgoing_topic, validated_result.dict())

                    except ValidationError as ve:
                        await self.logger.error(f"Validation error: {ve}")
                        raise KafkaProcessingError(f"Validation error: {ve}")
            finally:
                await consumer.stop()
                await self.logger.info(f"Consumer stopped for topic {incoming_topic}")

        return wrapper

    return decorator
