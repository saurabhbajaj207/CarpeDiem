# Contains all crytography related functions

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util import Counter

ENCODED_HEADER = '=*=EnC0d3dH3Ad3R==*'


def generateChecksum(password):
    return getKey(getKey(password))


def getKey(password):
    return SHA256.new(password).digest()


def encrypt(plainText, password):
    if plainText.startswith(ENCODED_HEADER):
        return plainText

    key = getKey(password)
    ctr = Counter.new(128)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return ENCODED_HEADER + cipher.encrypt(plainText)


def decrypt(cipherText, password):
    if not cipherText.startswith(ENCODED_HEADER):
        return cipherText

    cipherText = cipherText[len(ENCODED_HEADER):]
    key = getKey(password)
    ctr = Counter.new(128)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.decrypt(cipherText)
