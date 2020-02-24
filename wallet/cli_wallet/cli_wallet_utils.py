from model.cli_wallet_user import CliWalletUser


def verify_balance_response(received_response, expected_response, expected_value=""):
    """
    Verify received response of the 'Balance' command vs. expected response.

    :param received_response: The received response from the wallet
    :param expected_response: The expected response as stored in cli_wallet_responses.py
    :param expected_value: In cases where value needs to be verified, enter the value as an INT
    :return: Boolean, True or False for equality
    """
    received_response_string = received_response[0][0:13]
    received_response_numerical_value = received_response[0][14:-1]
    if received_response_string == expected_response[0]:
        if expected_value == "":
            if received_response == "":
                print("Incorrect value received!")
                return False
            else:
                print("Valid value received: " + received_response_numerical_value)
                return True
        else:
            if received_response_numerical_value == format(expected_value, "6f"):
                print("\nthe correct value was received: ")
                print("received value: " + str(received_response_numerical_value))
                print("expected value: " + str(expected_value))
                return True
            else:
                print("\nreceived and expected values does not match!")
                print("received value: " + str(received_response_numerical_value))
                print("expected value: " + str(expected_value))
                return False


def verify_invalid_address_response(received_response, expected_response):
    """
    Verify received response vs. expected response in case of an invalid address scenario.

    :param received_response: The received response from the wallet
    :param expected_response: The expected response as stored in cli_wallet_responses.py
    :return: Boolean, True or False for equality
    """
    if received_response == expected_response:
        return True
    else:
        print("Received Response:\n")
        print(received_response)
        print("Expected Response:\n")
        print(expected_response)
        return False


def verify_invalid_kasparov_address_response(received_response, expected_response):
    """
    Verify received response vs. expected response in case of an invalid kasparov address scenario.

    :param received_response: The received response from the wallet
    :param expected_response: The expected response as stored in cli_wallet_responses.py
    :return: Boolean, True or False for equality
    """
    received_response_list = received_response[0].split(":")
    del received_response_list[3]
    if received_response_list == expected_response:
        return True
    else:
        print("Received Response:\n")
        print(received_response)
        print("Expected Response:\n")
        print(expected_response)
        return False


def verify_create_command_response(received_response, expected_response):
    """
    Verify received response of the 'Create' command vs. expected response.

    :param received_response: The received response from the wallet
    :param expected_response: The expected response as stored in cli_wallet_responses.py
    :return: Boolean, True or False for equality
    """
    updated_received_response = []
    updated_received_response.extend([received_response[0], received_response[1][:19], received_response[2], received_response[3]])
    updated_received_response.extend([received_response[4][:19], received_response[5][:19], received_response[6][:18]])
    if updated_received_response == expected_response:
        return True
    else:
        print("Received Response:\n")
        print(updated_received_response)
        print("Expected Response:\n")
        print(expected_response)
        return False


def verify_send_command_response(received_response, expected_response):
    """
    Verify received response of the 'Send' command vs. expected response.

    :param received_response: The received response from the wallet
    :param expected_response: The expected response as stored in cli_wallet_responses.py
    :return: Boolean, True or False for equality
    """
    updated_received_response = []
    updated_received_response.extend([received_response[0], received_response[1][:15]])
    if updated_received_response == expected_response:
        return True
    else:
        print("Received Response:\n")
        print(updated_received_response)
        print("Expected Response:\n")
        print(expected_response)
        return False


def parse_create_response_to_object(received_response):
    """
    Parse received response of the "Create" command and returns a "CliWalletUser" object with the parsed info.

    :param received_response: The received response from the wallet
    :return: A "CliWalletUser" object with the parsed info
    """
    private_key = received_response[1][19:-1]
    mainnet_address = received_response[4][19:-1]
    testnet_address = received_response[5][19:-1]
    devnet_address = received_response[6][18:-1]
    return CliWalletUser(private_key, mainnet_address, testnet_address, devnet_address)
