from wallet.cli_wallet import cli_wallet_constants as cw_constants
from wallet.cli_wallet import cli_wallet_responses as cw_responses
from wallet.cli_wallet import cli_wallet_utils as cw_utils
import time
import subprocess
import logging


def cli_create_command():
    """
    Creates a new CLI Wallet details (private key and public addresses).

    :return: Response as a list of strings
    """
    current_time = time.time()
    timeout = current_time + 20
    process = ""
    response = ""

    try:
        print("Create command test initiating:")
        process = subprocess.Popen(["{0}wallet create".format(cw_constants.CLI_WALLET_LOCAL_PATH)], shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = retrieve_command_response(process, timeout, True)
        print("Create command completed successfully.")
        return response
    except Exception:
        print("Create command failed...")
        raise SystemExit


def cli_balance_command(kasparov_address, public_address, test_type=True):
    """
    Handles all "Balance" command variations for the CLI Wallet interface tests.

    :param kasparov_address: The Kasparov api-server address to be used
    :param public_address: The Public address to be used for the command
    :param test_type: Boolean, True == Positive test scenario, False == Negative test scenario
    :return: The response of the command as a list of strings
    """
    current_time = time.time()
    timeout = current_time + 20
    process = ""
    response = ""

    try:
        print("Balance command test initiating:")
        process = subprocess.Popen(["{0}wallet balance -a={1} -d={2}".format(cw_constants.CLI_WALLET_LOCAL_PATH,
                                                                             kasparov_address, public_address)],
                                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = retrieve_command_response(process, timeout, test_type)
        print(response)
        print("Balance command completed successfully.")
        return response
    except Exception:
        print("Balance command failed...")
        raise SystemExit


def cli_send_command(kasparov_address, public_address, private_key, send_amount, test_type=True):
    """
    Handles all "Send" command variations for the CLI Wallet interface tests.

    :param kasparov_address: The Kasparov api-server address to be used
    :param public_address: The Public address to be used for the command (the receiver of the funds)
    :param private_key: The private key to be used for the command (the sender of the funds)
    :param send_amount: The amount to be sent using the command
    :param test_type: Boolean, True == Positive test scenario, False == Negative test scenario
    :return: The response of the command as a list of strings
    """
    current_time = time.time()
    timeout = current_time + 20
    process = ""
    response = ""

    try:
        print("Send command test initiating:")
        process = subprocess.Popen(
            ["{0}wallet send -a={1} -t={2} -k={3} -v={4}".format(cw_constants.CLI_WALLET_LOCAL_PATH,
                                                                 kasparov_address, public_address, private_key,
                                                                 send_amount)],
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = retrieve_command_response(process, timeout, test_type)
        print("Send command completed successfully.")
        return response
    except Exception:
        print("Send command failed...")
        raise SystemExit


def retrieve_command_response(process, timeout, test_type):
    """
    Handles the retrieval of the online commands (balance, send) response.

    :param process: The command process variable
    :param timeout: The timeout value
    :param test_type: Boolean, True == Positive test scenario, False == Negative test scenario
    :return: The response of the command as a list of strings
    """
    counter = 0
    response = []

    while counter < 10:
        if test_type:
            output = process.stdout.readline().decode("utf-8")
        else:
            output = process.stderr.readline().decode("utf-8")
        if output != "":
            response.append(str(output))
            counter += 1
        else:
            counter += 1
        if time.time() > timeout:
            print("valid online command timed out!")
            raise SystemExit
    return response


def cli_balance_timer(kasparov_address, public_address, value_sent):
    """
    Handles the response verification for the Send command by iterating over 30 seconds
    looking for the response and comparing the sent value.

    :param kasparov_address: The Kasparov api-server address to be used
    :param public_address: The Public address to be used for the command (the receiver of the funds)
    :param value_sent: The amount that was sent using the command
    :return:
    """
    counter = 30
    received_value = False

    try:
        while counter >= 0 and received_value is False:
            response = cli_balance_command(kasparov_address, public_address)
            received_value = cw_utils.verify_balance_response(response, cw_responses.balance_command_positive_response,
                                                              value_sent)
            time.sleep(1)
            counter -= 1
            if received_value is True:
                return True
            elif counter < 0:
                print("Balance check timed out!")
                return False
    except Exception:
        print("cli balance timer failed...")
        raise SystemExit
