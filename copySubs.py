import os
import shutil
import sys

#Copies all files with a specific ending from a folder to another folder.
def copy(fromfolder,tofolder,file_ending):
    files = os.listdir(fromfolder)
    for file in files:
        splitup = os.path.splitext(file)
        if splitup[1] == file_ending:
            shutil.copy(os.path.join(fromfolder,file),tofolder)
                
    
#Gets all subfolders of a folder.
def getSubfolders(path):
    return [os.path.join(path, file) for file in os.listdir(path)]

if len(sys.argv) < 4:
    print("Usage: python copy.py <file_ending> <path> <tofolder>")
else:
    file_ending = sys.argv[1]
    dirpath = sys.argv[2]
    tofolder = sys.argv[3]
    subs = getSubfolders(dirpath)
    for sub in subs:
        copy(sub,tofolder,file_ending)