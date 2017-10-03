import unittest
from cryptLib import encrypt, decrypt
from fileLib import getFileList, updateFiles
import os
import shutil


class TestMethods(unittest.TestCase):
    def test_encrypt_decrypt(self):
        plaintext = "hello world"
        password = "pass"
        ciphertext = encrypt(plaintext, password)
        self.assertEqual(plaintext, decrypt(ciphertext, password))

        # trying to encrypt already encrypted file
        ciphertext = encrypt(plaintext, password)
        self.assertEqual(plaintext, decrypt(ciphertext, password))

        # trying to decrypt already decrypted text
        self.assertEqual(plaintext, decrypt(plaintext, password))

    def test_getFileList(self):
        self.makeFileStructure()
        fileList = ['Folder1\\Folder2\\hello1.txt', 'Folder1\\Folder3\\hello2.txt']
        self.assertEqual(getFileList("Folder1"), fileList)
        shutil.rmtree("Folder1")

    def makeFileStructure(self):
        os.makedirs("Folder1")
        os.makedirs(".\\Folder1\\Folder2")
        os.makedirs(".\\Folder1\\Folder3")
        f = open(".\\Folder1\\" +"\\hello.txt", 'w')
        f.close()
        for path, subdirs, files in os.walk("Folder1"):
            i = 1
            for dir in subdirs:
                f = open(".\\Folder1\\" + str(dir) + "\\hello" + str(i) + ".txt", 'w')
                f.write("hello world");
                f.close()
                i += 1


if __name__ == '__main__':
    unittest.main()
