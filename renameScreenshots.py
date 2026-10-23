import os
import sys

#Renames screenshots in a folder to be sequentially numbered starting from i, and only renames screenshots that have the number j in their name.
def renameScreenshots(path, i, j):
    iold = i-1
    files = os.listdir(path)
    while not iold == i:
        iold = i
        for file in files:
            splitup = os.path.splitext(file)
            if splitup[1] == ".png":
                if splitup[0].startswith("Download ("):
                    #print(splitup[0][10] + splitup[0][11])
                    if splitup[0][10] + splitup[0][11] == f"{j}" or (splitup[0][10] == f"{j}" and splitup[0][11] == ")"): #splitup[0][10] is first digit after (
                        os.rename(os.path.abspath(os.path.join(path,file)), 
                          os.path.abspath(os.path.join(path)) + f"\\Download ({i}).png")
                        i+=1
                        j+=1                    

if len(sys.argv) < 3:
    print("Usage: python renameScreenshots.py <path> <start_i> <start_j>")
else:
    path = sys.argv[2]
    i = int(sys.argv[3])
    j = int(sys.argv[4])
    renameScreenshots(path,i,j)