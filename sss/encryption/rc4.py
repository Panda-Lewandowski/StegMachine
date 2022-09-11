from Crypto.Cipher import ARC4
from Crypto.Hash import SHA256
from Crypto import Random

def rc4_encrypt(key, msg):
	return ARC4.new(key).encrypt(msg)

def rc4_decrypt(key, msg):
	return ARC4.new(key).decrypt(msg)

		
if __name__=='__main__':
    key = input('Введите ключ: ').encode('utf-8')
    msg = input('Введите сообщение: ').encode('utf-8')
    nonce = Random.new().read(16)
    key += nonce
    key = SHA256.new(key).digest() 
    print(f"Соль: {nonce}")
    print(f"Просоленный ключ: {key}")
    encr_msg = rc4_encrypt(key, msg)
    print(f"Зашифрованное сообщение: {encr_msg}")
    decr_msg = rc4_decrypt(key, encr_msg).decode('utf-8')
    print(f"Расшифрованное сообщение: {decr_msg}")
