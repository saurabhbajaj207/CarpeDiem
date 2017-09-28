# Contains all crytography related functions

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util import Counter


def getKey(password):
    return SHA256.new(password).digest()


def encrypt(plainText, password):
    key = getKey(password)
    ctr = Counter.new(128)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(plainText)


def decrypt(cipherText, password):
    key = getKey(password)
    ctr = Counter.new(128)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.decrypt(cipherText)
