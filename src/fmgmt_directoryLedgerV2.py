'''this code will walk through each sub-directory/folder in whatever parent directory you specify
   and catalogue the any files in the folders. The output is stored as a dictionary and written as json.
   The purpose of this program is to work in tandem with a fille path patching program I wrote that
   fixes file paths if the file location has changed.'''

import os
import json
#specofy the parent directory where to start
directory_path = r"PATH TO PARENT DIRECTORY"
# Create a dictionary to store the directory structure
directory_structure = {}
def structure(path, structure_dict):
    # Get all the items in the directory
    items = os.listdir(path)
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            sub_structure = {"dirpath":item_path}
            structure_dict[item] = sub_structure
            structure(item_path, sub_structure)
        else:
            structure_dict[item] = None
structure(directory_path, directory_structure)
#specify the directory where you want to write the directory ledger
dirPath_output = r"PATH TO WHERE YOU WANT TO WRITE THE OUTPUT"
#write the directory ledger as json
with open(str("%s%s%s" % (dirPath_output,"\\","directoryLedger.json")), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(directory_structure, indent=4, ensure_ascii=False))
