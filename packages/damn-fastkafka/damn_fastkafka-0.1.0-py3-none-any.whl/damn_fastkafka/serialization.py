import json
from abc import ABC, abstractmethod
from typing import Any



class Serializer(ABC):
    """Abstract base class for serialization."""

    @abstractmethod
    def serialize(self, data: Any) -> bytes:
        """Serialize the given data."""
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        """Deserialize the given data."""
        pass


class JsonSerializer(Serializer):
    """JSON serializer."""

    def serialize(self, data: Any) -> bytes:
        return json.dumps(data).encode("utf-8")

    def deserialize(self, data: bytes) -> Any:
        return json.loads(data.decode("utf-8"))
