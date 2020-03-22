"""
This module holds the methods that handle all the kaspa-d tx utils for the automation project.
"""
from kaspy_tools.kaspad import json_rpc_client
from kaspy_tools.logs import config_logger
from kaspy_tools.utils import general_utils


local_logger = config_logger.get_local_logger('kaspy_tools')


def error_handler(response_error):
    """
    Verify if an error was received in the block action that was conducted.

    :param response_error: The "error" dictionary that is part of the block cmd response formatted as: response["error"]
    :return: String, in case error was received, the code and message in one string, else "No error" string
    """
    if response_error is not None:
        error = "Error Code: " + str(response_error["code"]) + ", Error Message: " + str(response_error["message"])
        return error
    else:
        message = "No error"
        return message


def submit_valid_raw_tx(tx_hex, options=None):
    """
    Submits a raw tx to the DAG-block network.
    Returns the action's response.

    :param tx_hex: The tx as hex
    :param options: Enter specific options that are required else leave as None
    :return: The original response of the submit request, response_json
    """
    response, response_json = json_rpc_client.submit_block_request(tx_hex, options)
    return response, response_json
