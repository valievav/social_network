import logging


def create_logger(level=logging.DEBUG) -> logging.Logger:
    """
    Displays logs in the console.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = create_logger()
