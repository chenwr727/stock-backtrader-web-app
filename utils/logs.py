from loguru import logger

logger.add(
    "./logs/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="7 days",
    level="INFO",
    encoding="utf-8",
)
