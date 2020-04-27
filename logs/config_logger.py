import sys
import logging
import logging.handlers
from pathlib import Path

automation_file_handler = None
automation_stream_handler = None


def get_testkits_logger():
    global automation_file_handler
    global automation_stream_handler
    local_logger = logging.getLogger('TEST')
    local_logger.setLevel(logging.DEBUG)

    # add handlers to logger
    local_logger.addHandler(automation_file_handler)
    # local_logger.addHandler(automation_stream_handler)
    return local_logger


def get_kaspy_tools_logger():
    global automation_file_handler
    global automation_stream_handler
    local_logger = logging.getLogger('KT')
    local_logger.setLevel(logging.DEBUG)

    # add handlers to logger
    local_logger.addHandler(automation_file_handler)
    # local_logger.addHandler(automation_stream_handler)
    return local_logger


def make_automation_log_handlers():
    global automation_file_handler
    global automation_stream_handler
    logfile_path = Path.home() / "logs" / 'automation.log'
    automation_file_handler = logging.handlers.RotatingFileHandler(logfile_path, maxBytes=100000000)
    automation_file_handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter(fmt='%(levelname)s:%(asctime)s.%(msecs)01d:%(name)-4s:--> %(message)s',
                                  datefmt='%H:%M:%S')
    automation_file_handler.setFormatter(formatter)
    automation_stream_handler = logging.StreamHandler(sys.stderr)
    return automation_stream_handler, automation_file_handler
