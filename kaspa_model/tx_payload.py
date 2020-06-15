"""
TxPayload holds the data saved in the payload part of transactions
v0.4.1 coinbase:
[scriptPubKeyLength] [ScriptPubKey] [extraData]    (varint, bytes, bytes)
v0.5.0 coinbase:
[blueScore] [scriptPubKeyLength] [ScriptPubKey] [extraData]   (uint64, varint, bytes, bytes)

(extraData can be anything the miner wishes to push into the coinbase payload)
"""
from io import BytesIO
from kaspy_tools.utils import general_utils
class TxPayload:
    def __init__(self, *, blue_score=None, script_pub_key_length=None, script_pub_key=None, extra_data=None ):
        self.blue_score=blue_score
        self.script_pub_key_length=script_pub_key_length
        self.script_pub_key=script_pub_key
        self.extra_data=extra_data

    @staticmethod
    def parse_tx_payload(*, payload_bytes, use_blue_score=True):
        if use_blue_score:
            blue_score = int.from_bytes(payload_bytes[:8],byteorder='little')
            rest_of_bytes = BytesIO(payload_bytes[8:])
        else:
            blue_score = None
            rest_of_bytes = BytesIO(payload_bytes)
        script_pub_key_length = general_utils.read_varint(rest_of_bytes)[0]     # get the decimal value
        script_pub_key = rest_of_bytes.read(script_pub_key_length)
        extra_data = rest_of_bytes.read()  # read until the end
        return TxPayload(blue_score=blue_score, script_pub_key_length=script_pub_key_length,
                         script_pub_key=script_pub_key, extra_data=extra_data )


