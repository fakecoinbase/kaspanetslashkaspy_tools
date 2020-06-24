"""
This module holds the methods that handle all the kaspa-d tx utils for the automation project.
"""
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspad.json_rpc import json_rpc_requests

KT_logger = config_logger.get_kaspy_tools_logger()

RPC_INTERNAL_ERROR = -32603


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


def submit_valid_raw_tx(tx_hex, options=None, conn=None):
    """
    Submits a raw tx to the DAG-block network.
    Returns the action's response.

    :param tx_hex: The tx as hex
    :param options: Enter specific options that are required else leave as None
    :return: The original response of the submit request, response_json
    """
    response, response_json = json_rpc_requests.submit_raw_tx(tx_hex, options, conn=conn)
    return response, response_json


def check_if_in_mempool(tx_id, conn):
    """
    Checks if the txID is in the mempool.
    Returns the tx json if it's in, and the error if not.
    Will raise if the tx is conflicting or invalid.

    :param tx_id: the txID as hex.
    :param conn: the RPC connection.
    :return: response_json or None
    """
    in_mempool = json_rpc_requests.get_mempool_entry_request(tx_id, conn)
    if in_mempool['result']:
        if in_mempool['error']:
            raise ValueError(f'Got both result and error in the response: {in_mempool}')
        return in_mempool['result']
    else:
        error_code = in_mempool['error']['code']
        if error_code != RPC_INTERNAL_ERROR:
            raise ValueError(
                f'Missing tx in mempool, expected error code: {RPC_INTERNAL_ERROR}, found: {error_code}')

        expected_error_message = 'transaction is not in the pool'
        error_message = in_mempool['error']['message']
        if error_message != expected_error_message:
            raise ValueError(
                f'Missing tx in mempool, expected error message: "{expected_error_message}", found: "{error_message}"')

        return None
