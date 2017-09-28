import os
from getpass import getpass
import atexit

FLAG = "Flag.txt"


def get_key():
    key = ''
    while key == '':
        key = getpass('Enter password> ')
    return key


def exit_handler():
    print 'My application is ending!'


def createFlagFile():
    file = open(FLAG, 'w')
    file.write('keys Updated')
    file.close()


if __name__ == '__main__':
    if not os.path.exists(FLAG):
        print "Please enter the password"
        key1 = getpass(">")
        key2 = getpass("Re-Enter >")
        if (key1 != key2):
            print "Keys don't match. Please reEnter the password"
            exit(1)

        #updateFile(encrypt, getFileList(), key2)
        createFlagFile()

    else:
        atexit.register(exit_handler)
        print "Enter the Password to DeCrypt"
        key = get_key()

        #updateFile(decrypt, getFileList(), key2)

        tag = ''
        while tag != 'e':
            tag = raw_input("press 'e' to exit")
