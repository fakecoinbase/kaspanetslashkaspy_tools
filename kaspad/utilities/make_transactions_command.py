"""
This module creates kaspanet transactions.
"""
import random
from kaspy_tools import kaspa_model
import kaspy_tools.utils.general_utils
import kaspy_tools.utils.base58
import kaspy_tools.kaspa_model.tx
from kaspy_tools.kaspa_model import tx_in
import kaspy_tools.kaspa_model.tx_out
import kaspy_tools.kaspa_model.tx_script
import kaspy_tools.utils.elliptic_curve
from kaspy_tools.kaspa_model import kaspa_address
from kaspy_tools.kaspa_crypto.kaspa_keys import KaspaKeys
from kaspy_tools.kaspa_crypto import format_conversions



def make_new_transactions(count, utxo_list, addresses):
    """
    Main function that creates transactions.
    Parameters
    ----------
    count       The number of transactions to create
    utxo_list   A list of utxo to use
    keys        A dictionary with private and public keys to use

    Returns
    -------

    """
    tx_list = []
    for tx_num in range(count):
        tx = make_a_single_transaction(in_count=2, out_count=3, utxo_list=utxo_list, addresses=addresses)
        tx_list.append(tx)

    return tx_list


def make_a_single_transaction(*, in_count, out_count, utxo_list, addresses):
    """
    Make a transaction object, and return it.
    :param in_count:   Number of inputs
    :param out_count:  Number of outputs
    :utxo_list:        A list of utxo to use
    :keys:             A dictionary with private and public keys to use
    :return: a new transaction
    """
    utoxs_with_known_private_keys, total_value = find_utoxs_with_known_private_keys(in_count, utxo_list, addresses)
    out_list = make_p2pkh_output_list(out_count, total_value, addresses)
    in_list = make_p2pkh_input_list(utoxs_with_known_private_keys, addresses)

    new_tx =  kaspa_model.tx.Tx.tx_factory(version_bytes=kaspa_model.tx.VERSION_1,
                                           tx_in_list=in_list, tx_out_list=out_list,
                                           subnetwork_id=kaspa_model.tx.NATIVE_SUBNETWORK, locktime=0,
                                           gas=None, payload_hash=None, payload=None)

    tx_bytes = bytes(new_tx)  # inputs contain no signatures yet
    sign_tx_inputs(in_list, tx_bytes)
    # local_logger.info('new tx: ' + str(bytes(final_tx)))
    return new_tx


def sign_tx_inputs(in_list, tx_bytes):
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
        # new_pubhash = kaspy_tools.utils.elliptic_curve.schnorr_sign(tx_bytes, tx_in.get_private_key())
        private_key = tx_in.get_private_key()
        wif_key = format_conversions.bytes_to_wif(bytes.fromhex(private_key))
        sign_key = KaspaKeys(wif_key)
        new_pubhash = sign_key.sign(tx_bytes)
        tx_in.get_script().set_pubhash_bytes(new_pubhash)
    return None


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
    chosen_addresses = random.sample(addresses.items(), min(out_count,len(addresses)))  # choose count elements
    for i in range(out_count):
        public_key_hash = chosen_addresses[min(i, len(chosen_addresses))][1].get_public_key_hash(prefix='kaspadev')
        tx_script = make_script_pub_key(public_key_hash.hex())
        if out_count - i == 1:  # last output
            new_out = kaspa_model.tx_out.TxOut.tx_out_factory(value=last_out_value, script_pub_key=tx_script)
            #new_out = kaspa_model.tx_out.TxOut(last_out_value, tx_script)
        else:
            new_out = kaspa_model.tx_out.TxOut.tx_out_factory(value=each_out_value, script_pub_key=tx_script)
            #new_out = kaspa_model.tx_out.TxOut(each_out_value, tx_script)
        output_list.append(new_out)

    return output_list


def make_p2pkh_input_list(utxo_list, addresses):
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
    emtpy_sig = ''  # This is an empty hex string
    keys = {addr.get_public_key_hash() : addr for addr in addresses.values()}
    # make_sig_script
    for utxo in utxo_list:
        prev_tx = utxo[0][0]
        prev_tx_out_index = utxo[0][1]
        pub_hash_bytes = utxo[1]['output'].get_script_pub_key().get_pubhash_bytes()
        matched_address = keys[pub_hash_bytes]
        private_key, public_key = matched_address.get_private_key(), matched_address.get_public_key()
        script_sig = make_sig_script(emtpy_sig, public_key)  # empty bytes as <sig>
        sequence = 0
        new_tx_in = tx_in.TxIn.tx_in_factory(previous_tx_id=prev_tx, previous_tx_out_index=prev_tx_out_index,
                                 script=script_sig, sequence=sequence, private_key=private_key)
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
    for utxo_key, utxo_val in utxo_list.items():
        pub_hash_bytes = utxo_val['output'].get_script_pub_key().get_pubhash_bytes()
        if pub_hash_bytes not in hashed_public_keys:  # I don't know the private key for this public key
            continue
        if utxo_val['used'] == False:  # utxo is not used
            utxo_list_with_known_keys.append((utxo_key, utxo_val))
            utxo_val['used'] = True  # set to used
            total_value += utxo_val['output'].get_value()
            if len(utxo_list_with_known_keys) == in_count:
                break  # fount enough utxos
    if len(utxo_list_with_known_keys) < in_count:
        pass
        # local_logger.warning('Found only %d unused utxo, out of %d requested.', len(unused_utxo_list), in_count)
    return utxo_list_with_known_keys, total_value


def make_sig_script(sig, public_key):
    """
    Create an 'unlocking' script for an input.
    :param sig:    A signature to be used
    :public_key:   A public key that should be used to verify the signature
    :return:       A TxScript object describing the script
    """
    script_op_list = [sig, public_key]
    tx_scr = kaspa_model.tx_script.TxScript(op_list=script_op_list)
    return tx_scr


def make_script_pub_key(public_key_hash):
    """
    Create a 'puzzle' script object to be included in a tx out.
    :param public_key_hash: A 20 bytes hash of a public key.
    :return: a TxScript object
    """
    script_op_list = ['OP_DUP', 'OP_HASH160', public_key_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']

    tx_script = kaspa_model.tx_script.TxScript(op_list=script_op_list, pubHush=public_key_hash)
    return tx_script
