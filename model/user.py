
from utils import general_utils


class User:
    """
    This objects holds all the required methods to handle a user's data used for JSON-RPC tests.
    """
    def __init__(self, private_key, private_key_wif, address, public_key_hash):
        self.private_key = private_key
        self.private_key_wif = private_key_wif
        self.address = address
        self.public_key_hash = public_key_hash

    # ========== Set Block Methods ========== #

    def set_private_key(self, private_key):
        """ Sets variable "private_key" to the received value"""
        self.private_key = private_key

    def set_private_key_wif(self, private_key_wif):
        """ Sets variable "private_key_wif" to the received value"""
        self.private_key_wif = private_key_wif

    def set_address(self, address):
        """ Sets variable "address" to the received value"""
        self.address = address

    def set_public_key_hash(self, public_key_hash):
        """ Sets variable "public_key_hash" to the received value"""
        self.public_key_hash = public_key_hash

    # ========== Get Methods ========== #

    def get_private_key(self):
        """
        :return: private_key as bytes
        """
        return general_utils.convert_hex_to_bytes(self.private_key)

    def get_private_key_wif(self):
        """
        :return: private_key_wif as bytes
        """
        return general_utils.convert_hex_to_bytes(self.private_key_wif)

    def get_address(self):
        """
        :return: address as bytes
        """
        return general_utils.convert_hex_to_bytes(self.address)

    def get_public_key_hash(self):
        """
        :return: public_key_hash as bytes
        """
        return general_utils.convert_hex_to_bytes(self.public_key_hash)
