import requests
import json
from automation_testing import constants_devnet
from kaspy_tools.kasparov.kasparov_rest_objects import KasparovGet, KasparovPost

api_urls = {"blocks": constants_devnet.OPEN_DEVNET_KASPAROV_URL + "/blocks",
             "block": constants_devnet.OPEN_DEVNET_KASPAROV_URL + "/block/",
             "utxos": constants_devnet.OPEN_DEVNET_KASPAROV_URL + "/utxos/address/",
             "transactions": constants_devnet.OPEN_DEVNET_KASPAROV_URL + "/transactions/address/",
             "fee-estimates": constants_devnet.OPEN_DEVNET_KASPAROV_URL + "/fee-estimates",
             "transaction_id": constants_devnet.OPEN_DEVNET_KASPAROV_URL + "/transaction/id/",
             "transaction_hash": constants_devnet.OPEN_DEVNET_KASPAROV_URL + "/transaction/hash/"}


def api_get_requests(request_name, test_args=None, positional_parameters=None):
    """
    Manages all the API GET requests.

    :param request_name: The name of the request that is to be tested, passed as a string
    :param test_args: The setup of the test (if required)
    :param positional_parameters: positional parameters that might be required, such as blockHash, Miner Address, txid, txhash
                                as a string
    :return: The response for the request
    """
    api_test = KasparovGet(api_urls[request_name], test_args)
    if positional_parameters is not None:
        api_test.append_to_url(positional_parameters)
        print(api_test.url)
    response = requests.request("GET", api_test.url, params=api_test.parameters)
    return response


def api_post_requests(raw_transaction):
    """
    Manages all the API POST requests.

    :param raw_transaction: The raw transaction to be submitted
    :return: The response for the request
    """
    api_test = KasparovPost(constants_devnet.OPEN_DEVNET_KASPAROV_URL + "/transaction", raw_transaction)
    payload_json = json.dumps(api_test.payload)
    response = requests.post(api_test.url, payload_json, api_test.headers)
    return response


# api_get_requests("transaction_id", 1, "15b925dd07a1531dbefddf2c3d099254526696a0e3fb606527d7fc45334f730d")
# api_get_blocks(limit=2)
