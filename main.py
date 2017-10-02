import os
from getpass import getpass
import atexit
from fileLib import updateFiles, DIARY_DIR, createNewEntry
from cryptLib import encrypt, decrypt, generateChecksum

# **IMPORTANT**:Flag.txt contains checksum to verify the password
# so that user accidentally does not use wrong password to decrypt and encrypt
FLAG = DIARY_DIR+"\\Flag.txt"


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


# sets environment for New user by creating MyDiary and Flag.txt
def setEnv(password):
    if not os.path.exists(DIARY_DIR):
        os.makedirs(DIARY_DIR)
        file = open(FLAG, 'w')
        file.write(generateChecksum(password))
        file.close()


if __name__ == '__main__':
    # First time User
    if not os.path.exists(DIARY_DIR):
        print "First time User. Please enter the password"
        password1 = getpass(">")
        password2 = getpass("Re-Enter >")
        if (password1 != password2):
            print "Passwords don't match.Please Retry"
            exit(1)

        atexit.register(exit_handler)
        setEnv(password2)

    # User had already set the password
    else:
        atexit.register(exit_handler)
        print "Welcome to CarpeDiem!!"
        password = getPassword()
        validatePassword(password)
        updateFiles(decrypt, password)

        while True:
            print "Enter yor choice"
            print "'n':Create new Entry <space> [optional argument- dd/mm/yyyy]"
            print "'q':quit application "
            input = raw_input("\>>>")
            choice = input.split(" ")
            if choice[0] == 'n':
                if len(choice) == 1:
                    createNewEntry()
                else:
                    createNewEntry(choice[1])

            elif choice[0] == 'q':
                updateFiles(encrypt, password)
                exit(0)
