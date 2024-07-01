import os
import shutil
import click

# Function to create a list with folders within a certain path that have a specific phrase in them
def get_folders_phrase(basepath, phrase):
    folders_list = []
    print(f"Scanning directory: {basepath}")
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_dir():
                print(f"Checking folder: {entry.name}")
                if phrase in entry.name:
                    print(f"Folder matches: {entry.path}")
                    folders_list.append(entry.path)
                folders_list.extend(get_folders_phrase(entry.path, phrase))  # Recursively search subfolders
    return folders_list

# Function to list all folder paths within a basepath
def list_folderpaths(basepath):
    folderpaths_list = []
    for item in os.listdir(basepath):
        item_path = os.path.join(basepath, item)
        if os.path.isdir(item_path):
            folderpaths_list.append(item_path)
    return folderpaths_list

# Function to rename XML files within specified folder paths
def rename_XML(folderpaths_list):
    for folder_path in folderpaths_list:
        # Check if the folder path exists and is a directory
        if not os.path.isdir(folder_path):
            print(f"Folder path '{folder_path}' does not exist.")
            continue

        # Define XML files to rename
        xml_files = [
            "file1.xml", "file2.xml", "file3.xml",
            "file4.xml", "file5.xml", "file6.xml"
        ]

        # Rename each XML file if it exists
        for xml_file in xml_files:
            file_path = os.path.join(folder_path, xml_file)
            if os.path.isfile(file_path):
                new_filename = os.path.basename(folder_path) + "_" + xml_file
                os.rename(file_path, os.path.join(folder_path, new_filename))
                print(f"Renamed '{xml_file}' to '{new_filename}' in folder '{folder_path}'")


def move_recon_xml(dir_path):
    print(f"Moving XML files in {dir_path}")
    parent_directory = os.path.abspath(os.path.join(dir_path, "../.."))  # Move up two levels
    file1 = 'file1.xml'
    file2 = 'file2.xml'
    file3 = 'file3.xml'
    file_path1 = os.path.join(dir_path, file1)
    file_path2 = os.path.join(dir_path, file2)
    file_path3 = os.path.join(dir_path, file3)

    if not (os.path.isfile(file_path1) and os.path.isfile(file_path2) and os.path.isfile(file_path3)):
        print(f"XML files not found in {dir_path}")
        return

    try:
        shutil.move(file_path1, parent_directory)
        shutil.move(file_path2, parent_directory)
        shutil.move(file_path3, parent_directory)
        print(f"Moved XML files from {dir_path} to {parent_directory}")
    except Exception as e:
        print(f"Error moving XML files: {e}")


@click.command()
@click.option('--basepath', help="directory that contains folders of interest", required=True)
@click.option('--phrase', help="phrase that the name of the folders have to contain to be added", required=True)
def list_folders_phrase(basepath, phrase):
    print(f"Basepath: {basepath}, Phrase: {phrase}")
    folders = get_folders_phrase(basepath, phrase)
    print(f"Folders found: {folders}")
    for folder in folders:
        move_recon_xml(folder)

    # Additional functionality to list folders and paths, and rename XML files
    folderpaths_list = list_folderpaths(basepath)
    rename_XML(folderpaths_list)


if __name__ == '__main__':
    list_folders_phrase()
