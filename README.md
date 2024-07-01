# microct-data-auto
These scripts are part of a project work done for the certificate course "Data Steward" at the University of Vienna. It focuses on data management of microCT data.

# move_and_rename.py
This script is based to work on the directory structure and metadata files created by the YXLON software Cera, after reconstructing microCT data.

The script will
- create a list of paths for subfolders withing a specified directory ("basepath") that contain a certain phrase ("phrase")
- move specified files in the move_recon_xml function two directories up
- rename specified files to include the name of the folder they are stored in.

how to use:

Open terminal and change directory to the one containing the script

python move_and_rename.py --basepath /path/to/directory --phrase "phrase"

# zipping.py
This script will archive folders containing a certain phrase and rename them to contain the name of the folder they are located in.

how to use:

Open terminal and change directory to the one containing the script

python zipping.py --basepath /path/to/directory --phrase "phrase" --limit optional, maximum number of folders that should be archived --archive_name optional, new name of archive

concerning --archive_name:

This is the name of the archive before the initiation of the renaming the .zip folder to contain the name of the folder it is located in.

