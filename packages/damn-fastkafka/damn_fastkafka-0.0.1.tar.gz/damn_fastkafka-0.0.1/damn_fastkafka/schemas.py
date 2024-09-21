from pydantic import BaseModel


class InputSchema(BaseModel):
    message: str


class OutputSchema(BaseModel):
    response: str
