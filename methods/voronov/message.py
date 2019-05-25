from bitstring import BitArray

def split_message(msg, length=8):
    msg = BitArray(bytes=msg).bin
    return [msg[i:i+length] for i in range(0, len(msg), length)]


if __name__ == "__main__":
    msg = b'\xb2\x1a\xe7\x04z\xce\x82i\xdc}\xf3\x08\xea\xba\xe1\xf70i4c\xda'
    split_str = split_message(msg)
    print(f"Splited message: {split_str}")
    