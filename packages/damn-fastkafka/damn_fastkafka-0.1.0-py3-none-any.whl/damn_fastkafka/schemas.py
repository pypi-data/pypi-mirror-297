from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseKafkaSchema(BaseModel):
    """
    A base Pydantic model with a unique identifier field.

    All models inheriting from this class will have a unique `id` field.
    """

    id: UUID = Field(
        default_factory=uuid4,
        alias="_id",
        description="Unique identifier for the message",
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True
        from_attribute = True
