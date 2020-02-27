import sys
import logging
import logging.handlers

kosmos_file_handler = None
kosmos_stream_handler = None


def get_local_logger(local_logger_name):
    global kosmos_file_handler
    global kosmos_stream_handler
    local_logger = logging.getLogger(local_logger_name)
    local_logger.setLevel(logging.DEBUG)

    # add handlers to logger
    local_logger.addHandler(kosmos_file_handler)
    local_logger.addHandler(kosmos_stream_handler)
    return local_logger

def make_kosmos_log_handlers():
    global kosmos_file_handler
    global kosmos_stream_handler
    kosmos_file_handler = logging.handlers.RotatingFileHandler('./logs/kaspy_tools.log', maxBytes=100000000)
    kosmos_file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    kosmos_file_handler.setFormatter(formatter)
    kosmos_stream_handler = logging.StreamHandler(sys.stderr)
    return kosmos_stream_handler, kosmos_file_handler
