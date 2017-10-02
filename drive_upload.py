from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import hashlib
import time
from fileLib import DIARY_DIR


def createDriveDirectory(name, parentId, retryCount=3):
    try:
        files = drive.ListFile(
            {'q': u"'%s' in parents and title = '%s'and trashed = false" % (
                parentId, name.replace("'", "\\'"))}).GetList()
        if len(files) > 0:  # checking whether folder was already present
            return files[0]['id']

        folder = drive.CreateFile({'title': name, 'mimeType': 'application/vnd.google-apps.folder',
                                   'parents': [{"kind": "drive#fileLink", "id": parentId}]})
        folder.Upload()
        return folder['id']

    except:
        retryCount -= 1
        if retryCount == 0:
            print "Too many errors. Aborting..."
            raise
        else:
            print "Error communicating with Drive. Retrying in 30s..."
            time.sleep(30)
            createDriveDirectory(name, parentId, retryCount)


def createDriveFile(filepath, parentId, retryCount=3):
    try:
        name = os.path.basename(filepath)
        print "Uploading.... " + name
        files = drive.ListFile(
            {'q': u"'%s' in parents and title = '%s' and trashed = false" % (
                parentId, name.replace("'", "\\'"))}).GetList()
        if len(files) > 0:  # checking whether file was already present
            file = files[0]
            if file['md5Checksum'] == md5(filepath):  # checking for changes in file
                return file['id']
        else:
            file = drive.CreateFile({'title': name,
                                     'parents': [{"kind": "drive#fileLink", "id": parentId}]})
        file.SetContentFile(filepath)
        file.Upload()
        return file['id']

    except:
        retryCount -= 1
        if retryCount == 0:
            print "Too many errors. Aborting..."
            raise
        else:
            print "Error communicating with Drive. Retrying in 30s..."
            time.sleep(30)
            createDriveFile(filepath, parentId, retryCount)


def md5(filepath):
    with open(filepath) as file:
        return hashlib.md5(file.read()).hexdigest()


gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)
print "Uploading...."
backupFolder = drive.ListFile({'q': "'root' in parents and title = '__BACKUP__'"}).GetList()
if len(backupFolder) > 0:
    backupFolder = backupFolder[0]
else:
    print "Can't find backup folder. Please create '__BACKUP__' folder on google drive"
    exit(1)

folderToBackup = DIARY_DIR

# so same name as returned by os.walk
folderToBackup = os.path.abspath(folderToBackup)

driveIds = {}
name = os.path.basename(folderToBackup)
folderToBackupId = createDriveDirectory(name, backupFolder["id"])
driveIds[folderToBackup] = folderToBackupId

for root, dirs, files in os.walk(folderToBackup):
    if root in driveIds:
        rootDirId = driveIds[root]
    else:
        print "Unexpected: Cannot find Id. Abort"
        exit(1)

    for _dir in dirs:
        dirId = createDriveDirectory(_dir, rootDirId)
        driveIds[os.path.join(root, _dir)] = dirId

    for file in files:
        filepath = os.path.join(root, file)
        filepath = filepath.decode('utf8')
        fileId = createDriveFile(filepath, rootDirId)
