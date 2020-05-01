"""
This module holds what is considered as the "General Utilities" methods for the automation project.
"""
import hashlib
from textwrap import wrap
# from collections import Iterable
from collections.abc import Iterable


# ========== Hash related methods ========== #

def hash_256(element_bytes):
    """
    Runs two iterations of sha256 on a bytes object.

    :param element_bytes: bytes object
    :return: the result of the second iteration
    """
    data = element_bytes
    first_iteration = hashlib.sha256(data)
    second_iteration = hashlib.sha256(first_iteration.digest()).digest()
    return second_iteration


# ========== Data manipulation methods ========== #

def load_binary_file(file_path):
    """
    loads a binary file data.

    :param file_path: The path to the binary file
    :return: Data as bytes array
    """
    with open(file_path, "rb") as file:
        data = file.read()
    file.close()
    return data


def convert_bytes_to_hex(element_bytes):
    """
    Converts a bytes array to an hexadecimal string.

    :param element_bytes: The element bytes array
    :return: The element as hexadecimal string
    """
    hex_data = element_bytes.hex()
    return hex_data


def convert_hex_to_bytes(element_hex):
    """
    Converts an hex string to a bytes array.

    :param element_hex: The element hexadecimal string
    :return: The element as bytes array
    """
    bytes_data = bytes.fromhex(element_hex)
    return bytes_data


def little_endian_from_int(num, length):
    """
    Returns the little-endian byte sequence of length.

    :param num:
    :param length:
    :return: Byte sequence
    """
    new_byte = num.to_bytes(length, "little")
    return new_byte


def int_from_little_endian(bytes_array):
    """
    Returns an integer from a provided byte sequence as a little-endian number.

    :param bytes_array: The provided bytes array
    :return: Integer result
    """
    new_int = int.from_bytes(bytes_array, "little")
    return new_int


# ========== varint methods ========== #


def read_varint(bytes_stream):
    """
    Reads a variable integer from a bytes stream and returns the int value as well as the actual bytes array

    :param bytes_stream: The bytes stream to read
    :return: Returns 2 variables:
            1. int_value = the int value of the bytes that were read
            2. bytes_array = the array of the bytes from which the int was taken
    """
    first_byte = bytes_stream.read(1)[0]
    if first_byte == 0xfd:  # 0xfd means the next 2 bytes are the number
        next_2_bytes = bytes_stream.read(2)
        int_value = int_from_little_endian(next_2_bytes)
        return int_value, bytes(first_byte) + next_2_bytes
    elif first_byte == 0xfe:  # 0xfe means the next 4 bytes are the number
        next_4_bytes = bytes_stream.read(4)
        int_value = int_from_little_endian(next_4_bytes)
        return int_value, bytes(first_byte) + next_4_bytes
    elif first_byte == 0xff:  # 0xff means the next 8 bytes are the number
        next_8_bytes = bytes_stream.read(8)
        int_value = int_from_little_endian(next_8_bytes)
        return int_value, bytes(first_byte) + next_8_bytes
    else:  # everything else is just the integer
        return first_byte, bytes([first_byte])


def write_varint(value):
    """
    write_varint creates a bytes object that encodes a value based on the bitcoin varint.
    :param value: value to encode (int)
    :return: bytes object encoding of value parameter
    """
    if (value < 0xfd):
        return value.to_bytes(1, byteorder='little')
    elif value <= 0xffff:
        return b'\xfd' + value.to_bytes(2, byteorder='little')
    elif value <= 0xffffffff:
        return b'\xfe' + value.to_bytes(4, byteorder='little')
    else:
        return b'\xff' + value.to_bytes(8, byteorder='little')


# ========== Misc element related methods ========== #


# def build_element_from_list(element_list):
#     """
#     Returns an element (for example: block header/block body) as a bytes array from given list.
#
#     :param element_list: The element as a list
#     :return: The block element as bytes
#     """
#     element_list = list(flatten_nested_iterable(element_list))
#     block_element_bytes = b"".join(element_list)
#     return block_element_bytes


def flatten_nested_iterable(nested_iterable):
    """
    Yield items from any nested iterable.

    :param nested_iterable: Nested lists, numbers, strings, or any mixed container types
    :return: A flattened list based on the received data
    """
    for x in nested_iterable:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten_nested_iterable(x):
                yield sub_x
        else:
            yield x


def compare_elements(received_element, expected_element):
    """
    Verify that two provided elements are equal.

    :param received_element: The current tip hash that was received from the node
    :param expected_element: The hash of the latest valid block that was submitted
    :return: Boolean
    """
    if received_element == expected_element:
        return True
    else:
        return False


def confirm_element_in_list(element, list):
    """
    Confirms that an element is in a list.

    :param element: The variable that's supposed to be in the list
    :param list: The list in which we are looking for the element
    :return: Boolean
    """
    if element in list:
        return True
    else:
        return False


# ========== Reverse bytes order methods ========== #


def reverse_parent_hash_hex_to_bytes(parent_hash_list):
    """
    Reverses the order of parent hashes hex strings from a list and returns it as a list of bytes arrays.

    :param parent_hash_list: A list of parent hashes hex strings
    :return: A list of the reversed parent hashes as bytes arrays
    """
    new_parents_list = []
    for p_hash in parent_hash_list:
        reversed_hash = reverse_hex(p_hash)
        reversed_hash_bytes = convert_hex_to_bytes(reversed_hash)
        new_parents_list.append(reversed_hash_bytes)
    return new_parents_list


def reverse_bytes(bytes_array):
    """
    Reverses the bytes of a bytes_array and returns the reversed bytes_array.

    :param bytes_array: The bytes array
    :return: The reversed bytes array
    """
    bytes_list = list(bytes_array)
    bytes_list.reverse()
    return bytes(bytes_list)


def reverse_hex(hex_string):
    """
    Reverses the order of a hex string by interval of 2 characters and returns the reversed hex string.

    :param hex_string: The hex string
    :return: The reversed hex string
    """
    hex_string_list = wrap(hex_string, 2)
    hex_string_list.reverse()
    return "".join(hex_string_list)
