import csv
import json
import re
import string
import time
import datetime
from datetime import datetime, timezone
from os import listdir
from os.path import isfile, join
import os

#get current date and time
#This will be used to label the directory scan with a timestamp
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H-%M")
print("date and time =", dt_string)
print(now)
directoryPath_output = r"PATH TO DIRECTORY SCAN LEDGERS"
#output ledgers are labeled with "_walker" because the script is based on os.walk
write_dataOut = open("%s%s%s" % (directoryPath_output,dt_string,"_walker.csv"), 'w',newline='')
writer_dataOut = csv.writer(write_dataOut)
#write headers into the output csv
writer_dataOut.writerow([
	"rootDirKey","rootDir_path","subdir_path","subdir","now","has_projectTag","projectTag","sdFile","ext_ext",
	"f_created","f_modified","f_created_mdy","f_created_hms",
	"f_modified_mdy","f_modified_hms","fMod_period",
	"atime","lastAccess_mdy","f_size","st_mode","st_dev","st_nlink","st_uid","st_gid"])
#specify root directories to start the scan
dirs2search = {
	"directory_to_scan": r"PATH TO PARENT DIRECTORY TO SCAN",
	}
for rootDir_key,rootDir_path in dirs2search.items():
	for rootdir, dirs, files in os.walk(rootDir_path):
		for subdir in dirs:
			subdir_path = (os.path.join(rootdir, subdir))
			subDir_files = [f for f in listdir(subdir_path) if isfile(join(subdir_path, f))]
			fCount = 0
			for f in range(len(subDir_files)):
				try:
					fCount += 1
					sdFile = subDir_files[f]
					fileName_full = str(subdir_path)+"%s%s" % ("/",sdFile)
					split_fileName_atExt = sdFile.split(".")
					fileName = split_fileName_atExt[0]

					'''this section parses the file name and looks for project tag patterns
					the project tag pattern is a label which indicates the project the file belongs to
					if the file name does not match a project tag, a boolean of False will be designated to the row
					if the file does have a project tag, the row will be tagged with the respective project tag
					this is used for filtering projects by project'''
					
					split_fileName = fileName.split("_")
					projectTag = "-"
					has_projectTag = False
					if len(split_fileName) >3:
						fPatterns_  = [
							str(len(split_fileName[0])),
							str(len(split_fileName[1])),
							str(len(split_fileName[2]))
							]
						if str("_".join(fPatterns_)) in ["8_2_3","8_2_4","8_2_5"]:
							projectTag = split_fileName[2]
							has_projectTag = True
					#collect file stats and from the file
					ext_ext = split_fileName_atExt[-1]
					fileStats = os.stat(fileName_full)
					f_created = fileStats.st_ctime
					f_modified = fileStats.st_mtime
					f_cretaed_formated = datetime.fromtimestamp(fileStats.st_ctime, tz=timezone.utc)
					f_created_mdy = f_cretaed_formated.strftime("%m/%d/%Y")
					f_created_hms = f_cretaed_formated.strftime("%H:%M:%S")
					f_modified_formated = datetime.fromtimestamp(fileStats.st_mtime, tz=timezone.utc)
					f_modified_mdy = f_modified_formated.strftime("%m/%d/%Y")
					split_fMod_mdy = f_modified_mdy.split("/")
					f_lastAccess_formated = datetime.fromtimestamp(fileStats.st_atime, tz=timezone.utc)
					f_lastAccess_mdy = f_lastAccess_formated.strftime("%m/%d/%Y")
					#this section determines which billing period the file was last updated in
					fMod_d = int(split_fMod_mdy[1])
					fMod_m = int(split_fMod_mdy[0])
					fMod_y = int(split_fMod_mdy[2])
					fMod_period_d = 0
					if fMod_m <= 14:
						fMod_period_d = 1
					else:
						fMod_period_d = 2
					fMod_period = "%s%s%s%s%s" % (fMod_period_d,"_",fMod_m,"_",fMod_y)
					f_modified_hms = f_modified_formated.strftime("%H:%M:%S")
					f_size = fileStats.st_size
					#write the file to csv output
					writer_dataOut.writerow([
						rootDir_key,rootDir_path,subdir_path,subdir,now,has_projectTag,projectTag,sdFile,ext_ext,
						f_created,f_modified,f_created_mdy,f_created_hms,f_modified_mdy,
						f_modified_hms,fMod_period,fileStats.st_atime,f_lastAccess_mdy,
						f_size,fileStats.st_mode,fileStats.st_dev,fileStats.st_nlink,
						fileStats.st_uid,fileStats.st_gid
						])
				except:
					pass
write_dataOut.close()
print("done")
