"""
CoinbaseInfo class is used to record data needed when creating and validating a coinbase transaction.
"""
from io import BytesIO
from kaspy_tools.kaspa_model.tx import Tx
from kaspy_tools.kaspa_model.tx_script import TxScript
from kaspy_tools.kaspad.json_rpc import json_rpc_requests

class CoinbaseInfo:
    def __init__(self, *, paying_block_hash_bytes, coinbase_tx_bytes, conn=None):
        self.paying_block_hash_bytes = paying_block_hash_bytes
        self._paid_blocks = None   # a dictionary with block hash as ids, PaidBlockInfo instance as values
        self.coinbase_tx_bytes = coinbase_tx_bytes
        self.conn = conn

    @property
    def paid_blocks(self):
        if self._paid_blocks is None:
            self._paid_blocks = {}
            my_hash = self.paying_block_hash_bytes.hex()
            my_block = json_rpc_requests.get_block_request(block_hash=my_hash, conn=self.conn)['result']
            self.parent_hash = my_block['selectedParentHash']
            chain_response = json_rpc_requests.get_chain_from_block(start_hash=self.parent_hash,
                                                                    conn=self.conn)['result']
            for accepted_block in chain_response['addedChainBlocks'][0]['acceptedBlocks']:
                self._paid_blocks[accepted_block['hash']] = PaidBlockInfo(accepted_block['hash'],
                                                accepted_tx_hash_list=accepted_block['acceptedTxIds'],
                                                conn=self.conn)
        return self._paid_blocks

    @paid_blocks.setter
    def paid_blocks(self, paid_blocks):
        self._paid_blocks = paid_blocks

    @property
    def paying_block_script_pub_key_obj(self):
        coinbase_tx = Tx.parse_tx(BytesIO(self.coinbase_tx_bytes))
        script_obj = TxScript.parse_tx_script(raw_script=coinbase_tx.payload_obj.script_pub_key)
        return script_obj



class PaidBlockInfo:
    def __init__(self, block_hash, accepted_tx_hash_list, conn=None):
        self.block_hash = block_hash
        self.accepted_tx_hash_list = accepted_tx_hash_list
        self._accepted_transactions = None
        self.conn = conn

    @property
    def accepted_transactions(self):
        if self._accepted_transactions is None:
            self._accepted_transactions = self.update_fields()

        return self._accepted_transactions

    @accepted_transactions.setter
    def accepted_transactions(self, accepted_transactions):
        self._accepted_transactions = accepted_transactions

    def update_fields(self):
        my_block = json_rpc_requests.get_block_request(block_hash=self.block_hash, conn=self.conn,
                                                       verbose_tx=True)['result']
        self._accepted_transactions = {}
        for tx in my_block['rawRx']:
            if tx['hex'] not in self._accepted_transactions:
                self._accepted_transactions[tx['hex']] = tx

        
