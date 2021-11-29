import logging


def config_logging():
    log_formatter = logging.Formatter("%(asctime)s|%(levelname)8s| %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(log_formatter)
    custom_logger = logging.getLogger("")
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(handler)


if __name__ == '__main__':
    config_logging()
    logging.info('SessionParser start')
