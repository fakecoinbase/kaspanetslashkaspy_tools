import requests
import json
from automation_testing import constants_devnet, constants_testnet, constants_mainnet
from kaspy_tools.kasparov.kasparov_rest_objects import KasparovGet, KasparovPost

urls = {0: constants_devnet.OPEN_DEVNET_KASPAROV_URL, 1: constants_testnet.KASPAROV_URL,
        2: constants_mainnet.KASPAROV_URL}


def api_get_requests(request, network, test_args, positional_parameters=None):
    """
    Manages all the API GET requests.

    :param request: The path the request that is to be tested, passed as a string (/example/exp)
    :type request: str
    :param network: The network on which the test is to be conducted (0 =devnet, 1 = testnet, 2 = mainnet)
    :type network: int
    :param test_args: The setup of the test (if required)
    :type test_args: dict or None
    :param positional_parameters: positional parameters that might be required such as blockHash, Address, txid, txhash
    :type positional_parameters: str
    :return: The response for the request
    """
    url = urls[network]
    api_test = KasparovGet(url + request, test_args)
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
