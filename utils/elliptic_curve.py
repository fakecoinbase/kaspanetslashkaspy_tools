import hashlib
from kaspy_tools.utils import new_ecdsa
from kaspy_tools.utils import base58

# import utils.segwit_addr

"""
secp256k1 is taken from here:
    https://www.google.com/search?client=ubuntu&channel=fs&q=secp256k1+python&ie=utf-8&oe=utf-8
    
The base58 module was taken from:
    https://github.com/keis/base58
    
Is this page valid?
    https://gobittest.appspot.com/Address
    
"""


def make_private_key(base_private_key=None, compressed=True):
    """
    Make a private key object randomly, or using an existing one.
    :param base_private_key: None (for a new key) or hex representation of a private key (64 digits)
    :param compressed: True if a compressed key is requested
    :return: The private key object.
    """
    private_key = new_ecdsa.ECKey()

    if base_private_key and type(base_private_key) is bytes:  # got bytes
        private_key = private_key.set(base_private_key, compressed)
    elif base_private_key and type(base_private_key) is str:  # got hex
        private_key = private_key.set(bytes.fromhex(base_private_key), compressed)

    else:  # got nothing
        private_key.generate()

    return private_key


def make_public_key(private_key, compressed=True):
    """
    Convert private key to public key
    :param private_key:
    :param compressed:
    :return:
    """
    if type(private_key) is bytes:  # got bytes
        private_key_obj = utils.new_ecdsa.ECKey()
        private_key_obj.set(private_key, compressed)
    elif type(private_key) is str:  # got hex
        private_key_obj = utils.new_ecdsa.ECKey()
        private_key.set(private_key)
    else:  # got nothing
        private_key_obj = private_key  # private_key is already an object

    pubkey = private_key_obj.get_pubkey()
    pubkey_bytes = pubkey.get_bytes()
    return pubkey_bytes


def make_new_key_pair(compressed=False):
    private_key = utils.new_ecdsa.ECKey()
    private_key.generate()
    private_key_bytes = private_key.get_bytes()
    pubkey = private_key.get_pubkey()
    pubkey_hex = pubkey.get_bytes().hex()
    return private_key_bytes, pubkey_hex


def make_address_hash(public_key, compressed=False):
    # First hash256
    digester = hashlib.sha256()
    if type(public_key) is utils.new_ecdsa.ECKey:
        public_key.get_bytes()
    elif type(public_key) is str:
        public_key = bytes.fromhex(public_key)

    digester.update(public_key)
    sha_256_digest = digester.digest()
    print('\tsha256:', len(sha_256_digest), '\t', bytes.hex(sha_256_digest))
    # now ripemd160 hash
    ripemd160_digester = hashlib.new('ripemd160')
    ripemd160_digester.update(sha_256_digest)
    ripemd160_hash_hex = ripemd160_digester.hexdigest()
    ripemd160_hash = bytes.fromhex(ripemd160_hash_hex)
    print('\tripemd160', len(ripemd160_hash), '\t', ripemd160_hash_hex)
    return ripemd160_hash


def to_base58check(pubkey):
    pubkey = b'\x00' + pubkey
    print('Base 58')
    base58_pubkey = utils.base58.base58.b58encode(pubkey)
    print('\tbase58', len(base58_pubkey), base58_pubkey)
    base58check_pubkey = utils.base58.base58.b58encode_check(pubkey)
    print('\tbase58check', len(base58check_pubkey), base58check_pubkey)
    return base58check_pubkey


def schnorr_sign(msg, priv_key):
    digester = hashlib.sha256()
    digester.update(msg)
    hashed_msg = digester.digest()
    priv_key_obj = make_private_key(priv_key)
    sig = priv_key_obj.sign_schnorr(hashed_msg)
    return sig

#
# def demo_secp256k1():
#     private_key = make_private_key('18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725')
#     public_key = make_public_key(private_key)
#     compressed_public_key = make_public_key(private_key, compressed=True)
#     address_hash = make_address_hash(public_key, compressed=True)
#     # utils.base58.base58check_address = to_base58check(address_hash)
#     bech32_addr = utils.segwit_addr.bech32_encode('abc', list(address_hash))
#     print(bech32_addr)

#
# if __name__ == "__main__":
#     demo_secp256k1()
