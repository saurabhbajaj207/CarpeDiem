# Contains all File manipulation functions
import os
from cryptLib import encrypt, decrypt

DIARY_DIR = "MyDiary"


def getFileList(dirName):
    fileList = []
    for path, subdirs, files in os.walk(dirName):
        for filename in files:
            f = os.path.join(path, filename)
            if f.endswith(".txt"):
                fileList.append(f)

    return fileList


def updateFiles(function, password, dirName=DIARY_DIR):
    fileList = getFileList(dirName)
    for fname in fileList:
        f = open(fname, 'r')
        data = f.read()
        f.close()

        f = open(fname, 'w')
        f.write(function(data, password))
        f.close()
