"""
CoinbaseInfo class is used to record data needed when creating and validating a coinbase transaction.
"""

class CoinbaseInfo:
    pass


class PaidBlockInfo:
    def __init__(self, pub_key_hash):
        self.pub_key_hash = pub_key_hash