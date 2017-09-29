import os
from getpass import getpass
import atexit
from fileLib import updateFiles, DIARY_DIR
from cryptLib import encrypt, decrypt, generateChecksum

FLAG = "Flag.txt"


def getPassword():
    password = ''
    while password == '':
        password = getpass('Enter password> ')
    return password


def exit_handler():
    print 'Seize the Day!'


def validatePassword(password):
    file = open(FLAG, "r")
    checksum = file.read()
    file.close()
    temp = generateChecksum(password)
    if checksum != temp:
        print "password is incorrect. Please Retry"
        exit(1)


def createFlagFile(password):
    file = open(FLAG, 'w')
    file.write(generateChecksum(password))
    file.close()
    if not os.path.exists(DIARY_DIR):
        os.makedirs(DIARY_DIR)


if __name__ == '__main__':
    if not os.path.exists(FLAG):
        print "First time User. Please enter the password"
        password1 = getpass(">")
        password2 = getpass("Re-Enter >")
        if (password1 != password2):
            print "Passwords don't match.Please Retry"
            exit(1)

        atexit.register(exit_handler)
        updateFiles(encrypt, password2)
        createFlagFile(password2)

    else:
        atexit.register(exit_handler)
        print "Welcome to CarpeDiem!!"
        password = getPassword()
        validatePassword(password)
        updateFiles(decrypt, password)

        tag = ''
        while tag != 'e':
            tag = raw_input("press 'e' to exit")
            updateFiles(encrypt, password)
            exit(0)
