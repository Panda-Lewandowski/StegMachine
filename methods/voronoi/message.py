from bitstring import BitArray

class InvaligBlockLength(Exception):
    """This exception is raised when the length 
    of the message block is greater than 10.
    """
    pass


def split_message_to_bits(msg, length=8):
    """The function splits the message into blocks.
    
    :param msg: message to split 
    :type msg: bytes
    :param length: length of blocks, defaults to 8
    :type length: int, optional
    :raises InvaligBlockLength: is raised when the length is greater than 10
    :return: list of blocks
    :rtype: list
    """
    if length > 10:
        raise InvaligBlockLength("Length of block must be less than 10!")
    msg = BitArray(bytes=msg).bin
    return [msg[i:i+length] for i in range(0, len(msg), length)]


if __name__ == "__main__":
    msg = b'\xb2\x1a\xe7\x04z\xce\x82i\xdc}\xf3\x08\xea\xba\xe1\xf70i4c\xda'
    split_str = split_message_to_bits(msg)
    print(f"Splited message: {split_str}")
    