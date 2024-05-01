import logging

LOG: logging.Logger = logging.getLogger("firedust")


def configure_logger() -> None:
    LOG.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter(
        "[%(asctime)s - %(name)s - %(levelname)s] - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add the handlers to the LOG
    LOG.addHandler(console_handler)
