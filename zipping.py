import os
import shutil
import click

# function to create a list of folder paths within a basepath that contain a specific phrase
def list_folderpaths_phrase(basepath, phrase):
    folderpaths_phrase_list = []
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_dir():
                if phrase in entry.name:
                    folderpaths_phrase_list.append(entry.path)
                folderpaths_phrase_list.extend(
                    list_folderpaths_phrase(entry.path, phrase))  # Recursively search subfolders
    return folderpaths_phrase_list


# function to zip folders specified in folderpaths_phrase_list
def zip(folderpaths_phrase_list, phrase, archive_name=None):
    created_archives = []  # List to store created archive filenames

    for folder_path in folderpaths_phrase_list:
        if not os.path.isdir(folder_path):
            print(f"Folder path '{folder_path}' does not exist.")
            continue

        # Define name of archive
        if archive_name is None:
            archive_name = phrase + ".zip"
        else:
            if not archive_name.endswith(".zip"):
                archive_name += ".zip"

        # parent directory of the current folder
        parent_dir = os.path.dirname(folder_path)

        archive_path = os.path.join(parent_dir, archive_name)

        # create the archive
        shutil.make_archive(os.path.splitext(archive_path)[0], 'zip', folder_path)

        created_archives.append(os.path.basename(archive_path))  # Store created archive filename

        print(f"Created archive '{archive_path}'")

    return archive_name, created_archives  # Return archive_name and list of created archive filenames

# Function to list all folder paths within a basepath
def list_folderpaths(basepath):
    folderpaths_list = []
    for item in os.listdir(basepath):
        item_path = os.path.join(basepath, item)
        if os.path.isdir(item_path):
            folderpaths_list.append(item_path)
    return folderpaths_list


# Function to rename .zip files within specified folder paths
def rename(folderpaths_list, created_archives, archive_name):
    for folder_path in folderpaths_list:
        # Check if the folder path exists and is a directory
        if not os.path.isdir(folder_path):
            print(f"Folder path '{folder_path}' does not exist.")
            continue

        # Ensure archive_name is not None
        if archive_name is None:
            print("Error: archive_name cannot be None.")
            return

        # Check and rename .zip file
        for created_archive in created_archives:
            arch_file = os.path.join(folder_path, created_archive)
            if os.path.isfile(arch_file):
                # Construct new filename based on folder name and archive_name
                folder_name = os.path.basename(folder_path)
                new_arch_filename = folder_name + "_" + archive_name
                # Rename the archive file
                os.rename(arch_file, os.path.join(folder_path, new_arch_filename))
                print(f"Renamed '{created_archive}' to '{new_arch_filename}' in folder '{folder_path}'")


@click.command()
@click.option('--basepath', help="directory that contains folders of interest", required=True)
@click.option('--phrase', help="phrase that the name of the folders have to contain to be zipped", required=True)
@click.option('--limit', type=int, help="maximum number of folders to zip")
@click.option('--archive_name', help="name of the archive file", default=None)
def zip_phrase(basepath, phrase, limit, archive_name):
    print(f"Basepath: {basepath}, Phrase: {phrase}")
    folderpaths_phrase_list = list_folderpaths_phrase(basepath, phrase)

    # Apply limit to the list of folders
    if limit is not None:
        folderpaths_phrase_list = folderpaths_phrase_list[:limit]

    print(f"Folders to be zipped: {folderpaths_phrase_list}")

    # Call zip function with updated folderpaths_phrase_list and archive_name
    archive_name, created_archives = zip(folderpaths_phrase_list, phrase, archive_name=archive_name)

    # After zipping, list all folders (not filtered by phrase) to rename .zip files
    folderpaths_list = list_folderpaths(basepath)

    # Call rename function with folderpaths_list, created_archives, and archive_name
    rename(folderpaths_list, created_archives, archive_name)


if __name__ == '__main__':
    zip_phrase()
