from __future__ import annotations
from abc import ABC, abstractmethod
from compression.deflate import deflate_compress, deflate_decompress
from correction.hamming import hamming_encode, hamming_decode
from encryption.rc4 import rc4_encrypt, rc4_decrypt

class ParamError(Exception):
    pass

class SSS:
    def __init__(self, key, compression_type='deflate', 
                            correction_type='hamming', 
                            encryption_type='rc4') -> None:
        if compression_type == 'deflate':
            self._compression = DeflateCompression()
        else:
            raise ParamError("Unavailable compression algorithm")

        if correction_type == 'hamming':
            self._correction = HammingCorrection()
        else:
            raise ParamError("Unavailable correction algorithm")

        if encryption_type == 'rc4':
            self._encryption = RC4Encryption(key)
        else:
            raise ParamError("Unavailable encryption algorithm")

    @property
    def compression(self) -> Compression:
        return self._compression

    @compression.setter
    def compression(self, compression) -> None:
        self._compression = compression

    @property
    def correction(self) -> Correction:
        return self._correction

    @correction.setter
    def correction(self, correction) -> None:
        self._correction = correction

    @property
    def encryption(self) -> Encryption:
        return self._encryption

    @encryption.setter
    def encryption(self, encryption) -> None:
        self._encryption = encryption

    def __compress(self, string):
        return self._compression.compress(string)
    
    def __decompress(self, byte_string):
        return self._compression.decompress(byte_string)

    def __correct(self, byte_string):
        return self._correction.correct(byte_string)
    
    def __decorrect(self, byte_string):
        return self._correction.decorrect(byte_string)

    def __encrypt(self, key, byte_string):
        return self._encryption.encrypt(key, byte_string)

    def __decrypt(self, key, byte_string):
        return self._encryption.decrypt(key, byte_string)

    def encode(self, key, string):
        comp_str = self.__compress(string)
        cor_str = self.__correct(comp_str)
        enc_str = self.__encrypt(key, cor_str)
        return enc_str

    def decode(self, key, byte_string):
        dec_str = self.__decrypt(key, byte_string)
        decor_str = self.__decorrect(dec_str)
        decomp_str = self.__decompress(decor_str)
        return decomp_str


class Compression(ABC):
    @abstractmethod
    def compress(self, string):
        pass

    @abstractmethod
    def decompress(self):
        pass


class Correction(ABC):
    @abstractmethod
    def correct(self, byte_string):
        pass

    @abstractmethod
    def decorrect(self, byte_string):
        pass


class Encryption(ABC):
    def __init__(self, key):
        pass

    @abstractmethod
    def encrypt(self, key, byte_string):
        pass

    @abstractmethod
    def decrypt(self, key, byte_string):
        pass


class DeflateCompression(Compression):
    def compress(self, string):
        return deflate_compress(string.encode('utf-8'))
    
    def decompress(self, byte_string):
        return deflate_decompress(byte_string).decode('utf-8')


class HammingCorrection(Correction):
    def correct(self, byte_string):
        return hamming_encode(byte_string)

    def decorrect(self, string):
        return hamming_decode(string)

    
class RC4Encryption(Encryption):
    def __init__(self, key):
        super().__init__(key)

    def encrypt(self, key, byte_string):
        return rc4_encrypt(key, byte_string)

    def decrypt(self, key, byte_string):
        return rc4_decrypt(key, byte_string)
        

if __name__ == "__main__":
    msg = "qwerty"
    key = "zxcvbnm"
    stack = SSS(key)
    
    ready_str = stack.encode(key, msg)
    print(f"Ready string: {ready_str}")

    received_str = stack.decode(key, ready_str)
    print(f"Received string: {received_str}")