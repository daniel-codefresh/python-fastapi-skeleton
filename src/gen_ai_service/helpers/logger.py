import sys

from loguru import logger


def init_logging() -> None:
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "{extra} - <level>{message}</level>"
    )

    logger.remove(0)
    logger.add(sys.stdout, level="INFO", format=logger_format)
