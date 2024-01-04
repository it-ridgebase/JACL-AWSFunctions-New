import logging

def setup_logging():
    # Create a logger
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler that logs debug messages
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)

    # Create a console handler that also logs debug messages
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

def main():
    setup_logging()
    logger = logging.getLogger('test_logger')

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

if __name__ == "__main__":
    main()
