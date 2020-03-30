from kaspy_tools.kaspa_model.tx_script_codes import op_codes



class TxScript:
    def __init__(self, *, op_list=None, pubHush=None, pubKey=None):
        self._script_stack = b''
        if not op_list:
            self._op_list = []
        else:
            self._op_list = op_list
        self._pubHush = pubHush
        self._pubHush_bytes = None
        self._pubKey = pubKey

    def script_push(self, value):
        self._script_stack += value

    def script_pop(self):
        ret_byte = self._script_stack[-1]
        self._script_stack = self._script_stack[:-1]

    def get_pubhash(self):
        return self._pubHush

    def get_pubhash_bytes(self):
        if self._pubHush_bytes is None:
            self._pubHush_bytes = bytes.fromhex(self._pubHush)
        return self._pubHush_bytes

    def set_pubhash_bytes(self, pub_hash_bytes):
        self._pubHush_bytes = pub_hash_bytes

    def __bytes__(self):
        ret_bytes = b''
        for token in self._op_list:
            if token in op_codes:
                ret_bytes += op_codes[token]
            else:
                token_bytes = bytes.fromhex(token)
                ret_bytes += (len(token_bytes)).to_bytes(1, byteorder='little')
                ret_bytes += token_bytes

        return ret_bytes

    def __add__(self,other):
        sum = TxScript(self._op_list + other._op_list)
        return sum




