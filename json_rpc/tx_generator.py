"""
This module holds the methods that handle the process of generating valid and invalid txs for the automation project.
"""

from model.tx import Tx
from utils import general_utils
from io import BytesIO


# ========== Tx generator methods ========== #

def generate_valid_tx(previous_tx):
    """
    Generates a valid Tx with valid data.

    :return: Valid tx
    """
    prev_tx_bytes = general_utils.convert_hex_to_bytes(previous_tx)
    tx_stream = BytesIO(prev_tx_bytes)
    prev_tx_instance = Tx.parse_tx(tx_stream)