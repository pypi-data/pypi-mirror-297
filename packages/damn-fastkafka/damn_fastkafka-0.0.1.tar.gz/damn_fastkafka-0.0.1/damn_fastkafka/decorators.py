import json
from functools import wraps

from pydantic import BaseModel


def kafka_endpoint(
    incoming_topic: str,
    outgoing_topic: str,
    input_schema: BaseModel,
    output_schema: BaseModel,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(message):
            # Десериализация и валидация входящего сообщения
            decoded_message = json.loads(message.value.decode())
            input_data = input_schema(**decoded_message)

            # Вызов обработчика
            output_data = await func(input_data)

            # Валидация и сериализация выходящего сообщения
            validated_output = output_schema(**output_data.dict())
            return outgoing_topic, validated_output.json().encode("utf-8")

        return wrapper

    return decorator
