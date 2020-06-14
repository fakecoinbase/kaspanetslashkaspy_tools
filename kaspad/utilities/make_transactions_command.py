"""
This module creates kaspanet transactions.
"""
import random
# from hashlib import sha256
from kaspy_tools import kaspa_model
# import kaspy_tools.utils.general_utils
# import kaspy_tools.utils.base58
from kaspy_tools import kaspy_tools_constants
import kaspy_tools.kaspa_model.tx
from kaspy_tools.kaspa_model import tx_in
import kaspy_tools.kaspa_model.tx_out
from kaspy_tools.kaspa_model import tx_script
from kaspy_tools.kaspa_model import kaspa_address
from kaspy_tools.kaspa_crypto.kaspa_keys import KaspaKeys
from kaspy_tools.kaspa_crypto import format_conversions
from kaspy_tools.kaspa_crypto.schnorr_sing_key import ECKey



def make_new_transactions(*, count, utxo_list, addresses, in_count=1, out_count=1 ):
    """
    Create a list of TXs by calling
    :param count:
    :param utxo_list:
    :param addresses:
    :param in_count:
    :param out_count:
    :return:
    """
    tx_list = []
    fees= kaspy_tools_constants.DEFAULT_FEE
    for tx_num in range(count):
        tx = make_a_single_transaction(in_count=in_count, out_count=out_count, utxo_list=utxo_list, addresses=addresses, fees=fees)
        tx_list.append(tx)

    return tx_list


def make_a_single_transaction(*, in_count, out_count, utxo_list, addresses, fees):
    """
    Make a transaction object, and return it.
    :param in_count:   Number of inputs
    :param out_count:  Number of outputs
    :utxo_list:        A list of utxo to use
    :keys:             A dictionary with private and public keys to use
    :return: a new transaction
    """
    utoxs_with_known_private_keys, total_value = find_utoxs_with_known_private_keys(in_count, utxo_list, addresses)
    if len(utoxs_with_known_private_keys) < in_count:
        raise RuntimeError('Could not find enough UTXOs to make the required transaction.')
    out_list = make_p2pkh_output_list(out_count, total_value - fees, addresses)
    in_list = make_p2pkh_input_list(in_count, utoxs_with_known_private_keys,  addresses)

    new_tx =  kaspa_model.tx.Tx.tx_factory(version_bytes=kaspa_model.tx.VERSION_1,
                                           tx_in_list=in_list, tx_out_list=out_list,
                                           subnetwork_id_bytes=kaspa_model.tx.NATIVE_SUBNETWORK, locktime_int=0,
                                           gas_bytes=None, payload_hash=None, payload=None)

    sign_tx_inputs(in_list, new_tx)
    # local_logger.info('new tx: ' + str(bytes(final_tx)))
    return new_tx



def sign_tx_inputs(in_list, new_tx):
    """
    Schnorr signs a list of inputs that belong to a single transaction.
    Parameters
    ----------
    in_list      A list of tx inputs
    tx_bytes     The transaction that the inputs belong to, encoded in bytes.

    Returns      None
    -------

    """
    for tx_in in in_list:
        private_key = tx_in.private_key
        sign_key = ECKey()
        sign_key.set(private_key, compressed=True)
        public_key = sign_key.get_pubkey().get_bytes()
        tx_in.sig_script = tx_in.script_pub_key
        msg = bytes(new_tx) + (1).to_bytes(4, byteorder='little')   # TODO why??
        dbl_hash = KaspaKeys.double_sha256(msg)
        sig = sign_key.sign_schnorr(dbl_hash)
        new_script = tx_script.TxScript.script_sig_factory(sig, public_key, tx_script.SIG_HASH_ALL)
        tx_in.signed_script = new_script
        tx_in.sig_script = tx_in.empty_script
    restore_tx_scripts(new_tx)
    return None

def restore_tx_scripts(new_tx):
    input_list = new_tx.tx_input_list
    for input in input_list:
        input.sig_script = input.signed_script





def make_p2pkh_output_list(out_count, total_value, addresses):
    """
    Make a "pay to public key hash" output list for a single transaction.
    Parameters
    ----------
    out_count      The number of requested outputs
    total_value    The total value of the transaction output (sum for all outputs)
    addresses           A dictionary of keys that are used in the creation of the outputs.

    Returns        A list of the outputs
    -------

    """
    output_list = []
    each_out_value = total_value // out_count
    last_out_value = total_value - ((out_count - 1) * each_out_value)

    # choose out_count addresses (or less if I have less addresses)
    chosen_addresses = random.sample(addresses.items(), min(out_count,len(addresses)))  # choose count elements
    # now, use chosen_addresses to create script_pub_key objects and then output objects
    for i in range(len(chosen_addresses)):
        public_key_hash = chosen_addresses[i][1].get_public_key_hash()
        tx_script = kaspa_model.tx_script.TxScript.script_pub_hush_factory(public_key_hash)
        if out_count - i == 1:  # last output
            new_out = kaspa_model.tx_out.TxOut.tx_out_factory(value=last_out_value, script_pub_key=tx_script)
        else:
            new_out = kaspa_model.tx_out.TxOut.tx_out_factory(value=each_out_value, script_pub_key=tx_script)
        output_list.append(new_out)

    return output_list


def make_p2pkh_input_list(in_count, utxo_list, addresses):
    """
    Make a list of inputs (for a single tx) that can utilize utxos
    Parameters
    ----------
    utxo_list    A specific list of utxos' that was chosen for a transaction
    keys         A dictionary with private and public keys

    Returns      A list with the required inputs
    -------

    """
    in_list = []
    value = 0
    emtpy_sig = b''  # This is an empty bytes object
    keys = {addr.get_public_key_hash() : addr for addr in addresses.values()}
    # make_sig_script
    for utxo in utxo_list:
        prev_tx_bytes = bytes.fromhex(utxo['output'].get_tx_id())[::-1]
        prev_tx_out_index = utxo['output'].get_out_index()
        pub_hash_bytes = utxo['output'].get_script_pub_key().get_pubhash_bytes()
        matched_address = keys[pub_hash_bytes]
        private_key, public_key = matched_address.private_key, matched_address.public_key
        sig_script = tx_script.TxScript.empty_script()
        sequence_bytes = (0).to_bytes(8,byteorder='little')
        script_pub_key = utxo['output'].get_script_pub_key()
        new_tx_in = tx_in.TxIn.tx_in_factory(previous_tx_id_bytes=prev_tx_bytes, previous_tx_out_index=prev_tx_out_index,
                                 sig_script=sig_script, script_pub_key=script_pub_key, empty_script=sig_script,
                                 sequence_bytes=sequence_bytes, private_key=private_key)
        in_list.append(new_tx_in)
    return in_list


def find_utoxs_with_known_private_keys(in_count, utxo_list, addresses):
    """
    Search for in_count unused utxo to be used as inputs, and mark them as used.
    :param in_count:     Count of utxo to look for
    :param utxo_list:    A dictionary with all utxo
    :return:             chosem unused_utxos, total_value (for theswe utxo)
    """
    utxo_list_with_known_keys = []
    total_value = 0
    hashed_public_keys = [addr.get_public_key_hash() for addr in addresses.values()]
    #for utxo_key, utxo_val in utxo_list.items():
    for utxo_val in utxo_list:
        pub_hash_bytes = utxo_val['output'].get_script_pub_key().get_pubhash_bytes()
        if pub_hash_bytes not in hashed_public_keys:  # I don't know the private key for this public key
            continue
        if utxo_val['used'] == False:  # utxo is not used
            utxo_list_with_known_keys.append(utxo_val)
            utxo_val['used'] = True  # set to used
            total_value += utxo_val['output'].get_value()
            if len(utxo_list_with_known_keys) == in_count:
                break  # fount enough utxos
    if len(utxo_list_with_known_keys) < in_count:
        pass
        # local_logger.warning('Found only %d unused utxo, out of %d requested.', len(unused_utxo_list), in_count)
    return utxo_list_with_known_keys, total_value


