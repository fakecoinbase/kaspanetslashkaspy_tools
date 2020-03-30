import sys
import logging
import logging.handlers

kaspy_tools_file_handler = None
kaspy_tools_stream_handler = None


def get_local_logger(local_logger_name):
    global kaspy_tools_file_handler
    global kaspy_tools_stream_handler
    local_logger = logging.getLogger(local_logger_name)
    local_logger.setLevel(logging.DEBUG)

    # add handlers to logger
    local_logger.addHandler(kaspy_tools_file_handler)
    local_logger.addHandler(kaspy_tools_stream_handler)
    return local_logger


def make_kaspy_tools_log_handlers():
    global kaspy_tools_file_handler
    global kaspy_tools_stream_handler
    kaspy_tools_file_handler = logging.handlers.RotatingFileHandler('./logs/kaspy_tools.log', maxBytes=100000000)
    kaspy_tools_file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    kaspy_tools_file_handler.setFormatter(formatter)
    kaspy_tools_stream_handler = logging.StreamHandler(sys.stderr)
    return kaspy_tools_stream_handler, kaspy_tools_file_handler
