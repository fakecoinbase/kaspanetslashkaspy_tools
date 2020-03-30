# coincurve:
#     https://github.com/ofek/coincurve

from coincurve import PrivateKey as ECPrivateKey
from collections import namedtuple
from kaspy_tools.kaspa_crypto import format_conversions

# FIELD_SIZE = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
# GROUP_ORDER = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
# TONELLI_SHANKS_CONSTANT = (FIELD_SIZE + 1) // 4


Point = namedtuple('Point', ('x', 'y'))


# def parity(num):
#     return num & 1
#

# def x_to_y(x, y_parity):
#
#     y = pow(x ** 3 + 7, TONELLI_SHANKS_CONSTANT, FIELD_SIZE)
#
#     if parity(y) != y_parity:
#         y = FIELD_SIZE - y
#
#     return y


class KaspaKeys:
    """This class represents a point on the elliptic curve secp256k1 and
    provides all necessary cryptographic functionality.

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

    def get_address(self, prefix):
        """The public address you share with others to receive funds."""
        if self._address is None:
            self._address = format_conversions.public_key_to_address(self._public_key, prefix)

        return self._address

    # @property
    # def public_point(self):
    #     """The public point (x, y)."""
    #     if self._public_point is None:
    #         self._public_point = Point(*public_key_to_coords(self._public_key))
    #     return self._public_point

    def sign(self, data):
        """Signs some data which can be verified later by others using
        the public key.

        :param data: The message to sign.
        :type data: ``bytes``
        :returns: A signature compliant with BIP-62.
        :rtype: ``bytes``
        """
        return self._pk.sign(data)

    def verify(self, signature, data):
        """Verifies some data was signed by this private key.

        :param signature: The signature to verify.
        :type signature: ``bytes``
        :param data: The data that was supposedly signed.
        :type data: ``bytes``
        :rtype: ``bool``
        """
        return self._pk.public_key.verify(signature, data)

    def to_hex(self):
        """:rtype: ``str``"""
        return self._pk.to_hex()

    def to_bytes(self):
        """:rtype: ``bytes``"""
        return self._pk.secret

    def to_wif(self):
        return format_conversions.bytes_to_wif(
            self._pk.secret,
            version='main',
            compressed=self.is_compressed()
        )

    def to_der(self):
        """:rtype: ``bytes``"""
        return self._pk.to_der()

    def to_pem(self):
        """:rtype: ``bytes``"""
        return self._pk.to_pem()

    def to_int(self):
        """:rtype: ``int``"""
        return self._pk.to_int()

    def is_compressed(self):
        """Returns whether or not this private key corresponds to a compressed
        public key.

        :rtype: ``bool``
        """
        return True if len(self.public_key) == 33 else False

    def __eq__(self, other):
        return self.to_int() == other.to_int()