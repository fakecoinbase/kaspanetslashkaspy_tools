"""
Use this file to create private keys -> public keys -> addresses
"""

from kaspy_tools.kaspa_crypto.kaspa_keys import KaspaKeys
from kaspy_tools.kaspa_crypto import format_conversions

prefixes = ["kaspa", "kaspadev", "kaspareg", "kaspatest", "kaspasim"]


class KaspaAddress:
    def __init__(self, wif=None):
        self._address = None
        if wif is None:
            self._key = KaspaKeys()
        else:
            self._key = KaspaKeys(wif=wif)

    def get_address(self, prefix='kaspa'):
        """The public address you share with others to receive funds."""
        if self._address is None:
            self._address = format_conversions.public_key_to_address(self._key.public_key, prefix)

        return self._address

    def get_private_key(self):
        return self._key.to_hex()

    def get_public_key(self, in_hex=False):
        if hex:
            return self._key.public_key.hex()
        else:
            return self._key.public_key

    def get_public_key_hash(self, prefix='kaspa'):
        return format_conversions.address_to_public_key_hash(self._key.get_address(prefix))

    def get_wif(self):
        return self._key.to_wif()


if __name__ == "__main__":
    # see how to use.
    k1 = KaspaAddress()
    print('public key(hex)             : ', k1.get_public_key(in_hex=True))
    print('Address Bech32 with prefix) : ', k1.get_address("kaspadev"))
    print('private key(hex)            : ', k1.get_private_key())
    print('WIF(base58check)            : ', k1.get_wif())