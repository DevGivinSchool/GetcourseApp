import sys
import logging


def error_handler(message, do_exit=False):
    error_text = f"ERROR: {message}\n{traceback.format_exc()}"
    logging.error(error_text)
    if do_exit:
        sys.exit(f"Программа завершилась ошибкой\n{error_text}")
