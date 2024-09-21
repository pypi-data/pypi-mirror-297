from aiologger import Logger


async def setup_logger():
    """Set up the asynchronous logger using aiologger."""
    logger = Logger.with_default_handlers(name="kafka_client")
    return logger
