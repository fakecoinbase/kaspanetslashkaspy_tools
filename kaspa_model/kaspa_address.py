"""
Use this file to create private keys -> public keys -> addresses
"""
from kaspy_tools.utils.addr_libs.bitcash.wallet import Key

prefixes = ["kaspa", "kaspadev", "kaspareg", "kaspatest", "kaspasim"]


class KaspaAddress:
    def __init__(self):
        self._key = Key()

    def get_address(self, prefix):
        addr = self._key.get_address(prefix)
        return addr


    def get_public_key(self, in_hex=False):
        if hex:
            return self._key.public_key.hex()
        else:
            return self._key.public_key


if __name__ == "__main__":
    # see how to use. Private key in base58 is taken from docker_compose file.
    k1 = KaspaAddress()
    print(k1.get_public_key(in_hex=True))
    print(k1.get_address("kaspadev"))




