'''This script is meant to be run in a Python node in Grasshopper with Rhino7.
   The script will reference the most recent directory ledger and patch broken
   file paths. If the directory location or folder name(s) of a file have changed,
   the script will patch the file path as long as the file name has not changed.'''
import rhinoscriptsyntax as rs
import csv
import re
import string
import time
import datetime
from datetime import datetime
from os import listdir
from os.path import isfile, join
import os

now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d-%m-%Y_%H-%M")
print("date and time =", dt_string)
print(now)
f2f = x
directoryPath_ledgers = r"PATH TO DIRECTORY LEDGERS (CSVs)"
files_ = [f for f in listdir(directoryPath_ledgers) if isfile(join(directoryPath_ledgers, f))]
store_fCTimes = []
store_fPaths = []
for f in files_:
    split_f = f.split("_")
    if split_f[2] == "walker.csv":
        filePath = str(directoryPath_ledgers)+"%s" % (f)
        fileStats = os.stat(filePath)
        store_fCTimes.append(float(fileStats.st_ctime))
        store_fPaths.append(filePath)
f_read = store_fPaths[store_fCTimes.index(max(store_fCTimes))]
file = open(f_read, 'r')
lines_ = file.readlines()
file.close()
fPathOut_ = []
dirPath_ = None
for i in range(len(lines_)):
    line = lines_[i]
    line = line.strip("\n")
    csvInfo = line.split(',')
    if csvInfo[7] == f2f:
        dirPath_ = csvInfo[2]
        f2f_path = str("%s%s%s" % (dirPath_,"\\",f2f))
        a = f2f_path
        fPathOut_.append(f2f_path)
        break
