# coincurve:
#     https://github.com/ofek/coincurve

import hashlib
from coincurve import PrivateKey as ECPrivateKey
from kaspy_tools.kaspa_crypto import format_conversions



class KaspaKeys:
    """
    This class uses the python coincurve (that is based on secp256k1) to
    provides necessary cryptographic functionality.

    :param wif: A private key serialized to the Wallet Import Format. If the
                argument is not supplied, a new private key will be created.
                The WIF compression flag will be adhered to, but the version
                byte is disregarded. Compression will be used by all new keys.
    :type wif: ``str``
    :raises TypeError: If ``wif`` is not a ``str``.
    """
    def __init__(self, wif=None):
        self._address=None
        if wif:
            if isinstance(wif, str):
                private_key_bytes, compressed, version = format_conversions.wif_to_bytes(wif)
                self._pk = ECPrivateKey(private_key_bytes)
            elif isinstance(wif, ECPrivateKey):
                self._pk = wif
                compressed = True
            else:
                raise TypeError('Wallet Import Format must be a string.')
        else:
            self._pk = ECPrivateKey()
            compressed = True

        self._public_point = None
        self._public_key = self._pk.public_key.format(compressed=compressed)

    @property
    def public_key(self):
        """The public point serialized to bytes."""
        return self._public_key

    @property
    def public_key_hex(self):
        """The public point serialized to bytes."""
        return self._public_key.hex()


    @property
    def private_key_hex(self):
        return self._pk.to_hex()

    @property
    def private_key(self):
        """:rtype: ``bytes``"""
        return self._pk.secret

    def to_wif(self):
        return format_conversions.bytes_to_wif(
            self._pk.secret,
            version='main',
            compressed=self.is_compressed()
        )



    def is_compressed(self):
        """Returns whether or not this private key corresponds to a compressed
        public key.

        :rtype: ``bool``
        """
        return True if len(self.public_key) == 33 else False

    @staticmethod
    def double_sha256(data):
        if type(data) is str:
            bytes_data = bytes.fromhex(data)
        else:
            bytes_data = data

        msg_hash1 = hashlib.new('sha256',bytes_data ).digest()
        msg_hash2 = hashlib.new('sha256',msg_hash1 ).digest()
        return msg_hash2

