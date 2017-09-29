# Contains all File manipulation functions
import os
from datetime import datetime

DIARY_DIR = ".\\MyDiary"


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


def createNewEntry(date= ""):
    if date == "":
        now = datetime.now()
        yearPath = DIARY_DIR + "\\" + str(now.year)
        monthPath = yearPath + "\\" + str(now.month)
        dayPath = monthPath + "\\" + str(now.day) + ".txt"
    else:
        date = date.split("/")
        yearPath = DIARY_DIR + "\\" + str(date[2])
        monthPath = yearPath + "\\" + str(date[1])
        dayPath = monthPath + "\\" + str(date[0]) + ".txt"

    if not os.path.exists(yearPath):
        os.makedirs(yearPath)
    if not os.path.exists(monthPath):
        os.makedirs(monthPath)

    f = open(dayPath, 'a')
    f.close()
    os.system("notepad.exe " + dayPath)
