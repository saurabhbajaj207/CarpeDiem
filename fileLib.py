# Contains all File manipulation functions
import os

for path, subdirs, files in os.walk('.\MyDiary'):
   for filename in files:
     f = os.path.join(path, filename)
