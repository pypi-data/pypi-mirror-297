class KafkaConnectionError(Exception):
    """Exception raised for Kafka connection-related errors."""

    pass


class KafkaProcessingError(Exception):
    """Exception raised during Kafka message processing."""

    pass
