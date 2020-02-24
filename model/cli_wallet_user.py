from utils import general_utils


class CliWalletUser:
    """
    This objects holds all the required methods to handle a CLI wallet user's data.
    """
    def __init__(self, private_key, mainnet_address, testnet_address, devnet_address):
        self._private_key = private_key
        self._mainnet_address = mainnet_address
        self._testnet_address = testnet_address
        self._devnet_address = devnet_address

    # ========== Set Block Methods ========== #

    def set_private_key(self, private_key):
        """ Sets variable "private_key" to the received value"""
        self._private_key = private_key

    def set_mainnet_addr(self, mainnet_address):
        """ Sets variable "mainnet_address" to the received value"""
        self._mainnet_address = mainnet_address

    def set_testnet_addr(self, testnet_address):
        """ Sets variable "testnet_address" to the received value"""
        self._testnet_address = testnet_address

    def set_devnet_addr(self, devnet_address):
        """ Sets variable "devnet_address" to the received value"""
        self._devnet_address = devnet_address

    # ========== Get Methods ========== #

    def get_private_key(self):
        """
        :return: private_key
        """
        return self._private_key

    def get_mainnet_addr(self):
        """
        :return: mainnet_address
        """
        return self._mainnet_address

    def get_testnet_addr(self):
        """
        :return: testnet_address
        """
        return self._testnet_address

    def get_devnet_addr(self):
        """
        :return: devnet_address
        """
        return self._devnet_address

    def get_private_key_as_bytes(self):
        """
        :return: private_key as bytes
        """
        return general_utils.convert_hex_to_bytes(self._private_key)

    def get_mainnet_addr_as_bytes(self):
        """
        :return: mainnet_address as bytes
        """
        return general_utils.convert_hex_to_bytes(self._mainnet_address)

    def get_testnet_addr_as_bytes(self):
        """
        :return: testnet_address as bytes
        """
        return general_utils.convert_hex_to_bytes(self._testnet_address)

    def get_devnet_addr_as_bytes(self):
        """
        :return: devnet_address as bytes
        """
        return general_utils.convert_hex_to_bytes(self._devnet_address)
