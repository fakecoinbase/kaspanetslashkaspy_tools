import secp256k1
import utils.base58


class KaspaAddress:
    """
    Class that handles private/public keys and Kaspa addresses
    """
    def __init__(self, *, base58_private_key=None, hex_private_key=None):
        """
        Instantiate a KaspaAddress, either using your own private key, or letting it make a new one.
        :param base_private_key: Wif (walet input format) representation of a private key.
        """
        if base58_private_key:
            hex_key = utils.base58.b58decode(base58_private_key).hex()
            self._private_key = secp256k1.PrivateKey(privkey=bytes.fromhex(hex_key))
        elif hex_private_key:
            self._private_key = secp256k1.PrivateKey(privkey=bytes.fromhex(hex_private_key))
        else:
            self._private_key = secp256k1.PrivateKey()

        self._public_key = self._private_key.pubkey


    def get_private_key(self):
        """
        Returns a hex representation of the private address
        :return:
        """
        return self._private_key.serialize()

    def get_public_key(self):
        """
        Returns a hex representation of the private address
        :return:
        """
        return self._public_key.serialize().hex()

    def get_public_base58(self):
        pub_key = self._public_key.serialize()
        return utils.base58.b58encode(pub_key)

    @staticmethod
    def decode_wif(private_key_WIF):
        """
        Accepts a wif (walet encoded format) encoded key.
        Returns that key encoded in hex.
        :param private_key_WIF: Wif encoded private key
        :return:
        """
        first_decode = utils.base58.b58decode(private_key_WIF)
        private_key_full = first_decode.hex()
        private_key = private_key_full[2:-8]
        return private_key


if __name__ == "__main__":
    # see how to use. Private key in base58 is taken from docker_compose file.
    add = KaspaAddress(base58_private_key='J2XvsEoCPpJFx4bhJMXUszGpATvGs9zvPtJAjBrVcChh')
    print(add.get_private_key())
    print(add.get_public_key())

