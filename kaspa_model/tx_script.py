from io import BytesIO
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspa_model.tx_script_codes import op_codes_to_bytes, bytes_to_op_codes
from kaspy_tools.utils import general_utils

KT_logger = config_logger.get_kaspy_tools_logger()


SIG_HASH_ALL = b'\x01'
SIGHASH_NONE = b'\x02'
SIGHASH_SINGLE = b'\x03'
SIGHASH_ANYONECANPAY = b'\x04'

class TxScript:
    def __init__(self, script_stack_op=None, script_stack_bytes=None):

        self._script_stack_op = script_stack_op or []
        self._script_stack_bytes = script_stack_bytes or []


    @classmethod
    def parse_tx_script(cls, *, raw_script='', length=0):
        if type(raw_script) is str:     # i.e:  hex string
            script_bytes = bytes.fromhex(raw_script)
        elif type(raw_script) is BytesIO:
            script_bytes = raw_script.read(length)
        else:               # type(raw_script) is bytes
            script_bytes = raw_script
        new_script = cls()
        last_op = None
        while script_bytes:
            op_pair, script_bytes, pub_hash_bytes = cls.get_token(script_bytes, last_op)
            last_op = op_pair[0]
            new_script.script_push(op_pair[0], op_pair[1])
            if pub_hash_bytes:
                new_script.set_pub_hash(pub_hash_bytes)
        return new_script

    @classmethod
    def get_token(cls, script_bytes, last_op=None):
        """
        This is a tokenizer, part of the parsing of script given in bytes.
        Call it with script bytes, and it will return the next token + rest of scripts.
        If the last token was OP_HASH160, this means that the current data is the has, so it
        returns this also.
        :param script_bytes: A bytes object with raw rest-of-script
        :param last_op: The string name of the last token seen in this script (e.g: 'OP_HASH160')
        :return: (opcode, value), rest-of-script, pub-hash
                example 1:
                ('OP_EQUAL', b'\x87'),b'', None

                Example 2:
                ('data', b'\xda\x17E\xe9\xb5I\xbd\x0b\xfa\x1aV\x99q\xc7~\xba0\xcdZK'),
                b'\x14\xda\x17E\xe9\xb5I\xbd\x0b\xfa\x1aV\x99q\xc7~\xba0\xcdZK\x87',
                b'\xda\x17E\xe9\xb5I\xbd\x0b\xfa\x1aV\x99q\xc7~\xba0\xcdZK'
        """
        pub_hash_bytes = None
        if script_bytes[:1] in bytes_to_op_codes:
            checked_byte = script_bytes[0:1]
            op_pair = (bytes_to_op_codes[checked_byte], checked_byte)
            return op_pair, script_bytes[1:], pub_hash_bytes
        else:   # data
            data_len = script_bytes[0]
            just_data = script_bytes[1:data_len+1]
            op_pair = ('data', just_data)
            if last_op == 'OP_HASH160':
                pub_hash_bytes = just_data
            return op_pair, script_bytes[data_len+1:], pub_hash_bytes


    @classmethod
    def empty_script(cls):
        script_sig = cls()
        return script_sig


    @classmethod
    def script_sig_factory(cls, sig, public_key, hash_type):
        script_sig = cls()
        script_sig.script_push('<sig>',  sig + hash_type)  # empty sig with length 0
        pub_key_data = public_key
        script_sig.script_push('<pub_key>', pub_key_data)
        return script_sig

    @classmethod
    def script_pub_hush_factory(cls, public_key_hash):
        script_op_list = ['OP_DUP', 'OP_HASH160', public_key_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
        new_script = cls()
        for token in script_op_list:
            if token in op_codes_to_bytes:
                new_script.script_push(token, op_codes_to_bytes[token])
            else:
                new_script.script_push('<pub_hash>', token)
                new_script.set_pub_hash(token)

        return new_script

    def set_pub_hash(self,pub_hash_bytes):
        self._pub_hash_bytes = pub_hash_bytes

    def script_sig_set_sig(self, sig):
        # mesure just the length of sig, without the extra byte.
        # len_sig = len(sig[:-1]).to_bytes(1, byteorder='little')
        len_sig = len(sig).to_bytes(1, byteorder='little')
        self._script_stack_bytes.append(len_sig + sig)
        self._script_stack_op.append('<sig>')

    def script_push(self, op_name, op_value):
        self._script_stack_op.append(op_name)
        self._script_stack_bytes.append(op_value)

    def script_pop(self):
        op_name = self._script_stack_op.pop()
        op_value = self._script_stack_bytes.pop()
        return op_name, op_value

    #****************    get methods  *************************

    def get_pubhash_bytes(self):
        # get it without the length byte
        return self._pub_hash_bytes

    def __bytes__(self):
        ret_bytes = b''
        for token in self._script_stack_bytes:
            if token in bytes_to_op_codes:
                ret_bytes += token
            else:
                ret_bytes += (len(token)).to_bytes(1, byteorder='little')
                ret_bytes += token
        return ret_bytes

    # def __add__(self,other):
    #     new_stack_bytes = self._script_stack_bytes + other._script_stack_bytes
    #     new_stack_op = self._script_stack_op + other._script_stack_op
    #     sum_script = TxScript(script_stack_bytes=new_stack_bytes, )
    #     return sum_script




