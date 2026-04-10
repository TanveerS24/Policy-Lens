from loguru import logger


def configure_logging() -> None:
    logger.remove()
    logger.add("/tmp/policylens.log", rotation="10 MB", retention="7 days", enqueue=True, backtrace=True, diagnose=True)
    logger.add("stdout", enqueue=True)
