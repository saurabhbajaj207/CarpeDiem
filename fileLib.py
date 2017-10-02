# Contains all File manipulation functions
import os
from datetime import datetime

DIARY_DIR = ".\\MyDiary"


def getFileList(dirName):
    fileList = []
    for path, subdirs, files in os.walk(dirName, topdown=True):
        for filename in files:
            f = os.path.join(path, filename)
            if f.endswith(".txt"):
                fileList.append(f)
    # fileList[1:] is used to exclude Flag.txt from encryption
    return fileList[1:]


def updateFiles(function, password, dirName=DIARY_DIR):
    fileList = getFileList(dirName)
    for fname in fileList:
        f = open(fname, 'r')
        data = f.read()
        f.close()

        f = open(fname, 'w')
        text = function(data, password)
        if text == None:
            print "Incorrect Decryption key"
            print "Contents of Flag.txt were either changed or deleted"
            f.write(data)
            f.close()
            exit(1)

        f.write(text)
        f.close()


def createNewEntry(date=""):
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']

    if date == "":
        now = datetime.now()
        yearPath = DIARY_DIR + "\\" + str(now.year)
        monthPath = yearPath + "\\" + str(month_list[now.month - 1])
        dayPath = monthPath + "\\" + str(int(now.day)) + ".txt"
    else:
        date = date.split("/")
        yearPath = DIARY_DIR + "\\" + str(date[2])
        monthPath = yearPath + "\\" + str(month_list[date[1] - 1])
        dayPath = monthPath + "\\" + str(int(date[0])) + ".txt"

    if not os.path.exists(yearPath):
        os.makedirs(yearPath)
    if not os.path.exists(monthPath):
        os.makedirs(monthPath)

    f = open(dayPath, 'a')
    f.close()
    os.system("notepad.exe " + dayPath)
