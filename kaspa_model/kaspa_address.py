"""
Use this file to create private keys -> public keys -> addresses
"""

from kaspy_tools.kaspa_crypto.kaspa_keys import KaspaKeys
from kaspy_tools.kaspa_crypto import format_conversions

prefixes = ["kaspa", "kaspadev", "kaspareg", "kaspatest", "kaspasim"]


class KaspaAddress:
    def __init__(self, wif=None):
        """
        Create a new KaspaAddress object.
        If a private key is supplied, base address on this private key.
        self._address will keep a kaspa address such as:
        kaspadev:qq8ycyv5rd4azxwtkp6vlxgcutpgfrf4zu336j4mpe
        Otherwise, create a new private key.
        :param wif: A private key, encoded as a wif (Wallet Import Format).
        """
        self._address = None    # ...built lazily, only when asked for
        if wif is None:
            self._key = KaspaKeys()
        else:
            self._key = KaspaKeys(wif=wif)

    def get_address(self, prefix='kaspa'):
        """
        Lazily creates and returns the address.
        This is a Bech32 encoded address built based on a public key hash.
        This is the public address you share with others to receive funds.
        :param prefix: Specify the prefix for the required address.
        :return: The address computed (or already stored).
        """
        if self._address is None:
            self._address = format_conversions.public_key_to_address(self._key.public_key, prefix)

        return self._address

    @property
    def private_key(self):
        """
        Returns the bytes representation of the private key stored.
        :return: the bytes representation of the private key stored.
        """
        return self._key.private_key

    @property
    def private_key_hex(self):
        """
        Returns the hex version of the private key stored.
        :return:
        """
        return self._key.public_key_hex

    @property
    def public_key(self):
        return self._key.public_key

    @property
    def public_key_hex(self):
        return self._key.public_key.hex()

    def get_public_key_hash(self):
        pub_key = self.public_key
        return format_conversions.address_to_public_key_hash(pub_key)

    def get_wif(self):
        return self._key.to_wif()


if __name__ == "__main__":
    # see how to use.
    k1 = KaspaAddress()
    print('public key(hex)             : ', k1.public_key_hex)
    print('Address Bech32 with prefix) : ', k1.get_address("kaspadev"))
    print('private key(hex)            : ', k1.private_key)
    print('WIF(base58check)            : ', k1.get_wif())