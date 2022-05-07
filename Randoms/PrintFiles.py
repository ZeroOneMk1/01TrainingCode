# !/usr/bin/python

import os

EXT = (".txt", ".py", ".json") # CHANGE ME into all the file extensions that you want THAT ARE TEXT FILETYPES
ROOT_DIR = "/Users/yusufsimsek/Desktop/Code/01TrainingCode/Party Wizard" #CHANGE ME to the root directory of files

for (root, dirs, files) in os.walk(ROOT_DIR, topdown=True):
    for name in files:
        path = os.path.join(root, name)
        if path.endswith(EXT):
            print(f"--------------------")
            print(f"## File {path}:\n")
            with open(path, 'r') as f:
                print(f.read())