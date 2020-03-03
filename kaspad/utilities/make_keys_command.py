"""
This module creates private/pulic key-pairs, and store them in the commands storage.
"""
import hashlib
from kosmos.k_agent.logs import config_logger
from kaspy_tools.utils import elliptic_curve
from kaspy_tools.utils import base58

local_logger = config_logger.get_local_logger(__name__)


def create_public_and_private_keys(count):
    """
    Create private and public keys, to be used in outputs of transactions
    :return: the keys dictionary
    """
    keys = {}
    for i in range(count):
        private, public = elliptic_curve.make_new_key_pair()
        hash_pub = hash_public_key(public)
        keys[hash_pub] = private, public

    add_mining_address(keys, '5y3R29c7Xzf4gj6BihFCrfvY86cQEX2s17uhCySKnC1j')
    add_mining_address(keys, 'AbhCRoR8X9C7wvBeUWiQWiyP81ZmprCyBVharQH4Bhwz')
    local_logger.info('%d key-pairs created.', len(keys))
    return keys


def add_mining_address(keys, base58_private_key):
    """
    manually add single private and public key from dev-net
    :param keys:                 A dictionary with current keys
    :param base58_private_key:   A base58 encoded private address to add
    :return: None
    """
    private_mining_address = base58.b58decode(base58_private_key, base58.BITCOIN_ALPHABET)
    public_mining_address = elliptic_curve.make_public_key(private_mining_address, compressed=True).hex()
    public_hash = elliptic_curve.make_address_hash(public_mining_address, compressed=True)
    keys[public_hash] = (private_mining_address, public_mining_address)
    return None


def hash_public_key(public_key):
    """
    Make a kaspa hash of a public key
    Parameters
    ----------
    public_key   Hex encoded public key

    Returns      The hashed public address
    -------

    """
    hasher_256 = hashlib.sha256()
    hasher_256.update(bytes.fromhex(public_key))
    pub_hash_1 = hasher_256.digest()
    hasher_160 = hashlib.new('ripemd160')
    hasher_160.update(pub_hash_1)
    pub_hash_2 = hasher_160.digest()
    return pub_hash_2
