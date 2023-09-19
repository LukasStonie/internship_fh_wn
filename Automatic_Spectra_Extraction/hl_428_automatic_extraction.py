import os
import shutil


def copy_file_and_rename(file):
    # get information from path
    properties = file.split("/")
    group = properties[0]
    batch = properties[1]
    time = properties[2]
    file_name = properties[3]

    source_file = SOURCE_DIR + "/" + file
    file_exists = os.path.isfile(source_file)
    destination_folder = TARGET_DIR + "/" + group
    destination_file = destination_folder + "/" + batch + "_" + time + "_" + file_name

    try:
        # print(destination_file)
        os.makedirs(destination_folder, exist_ok=True)
        shutil.copyfile(source_file, destination_file)
    except Exception as e:
        print(e)
    return


SOURCE_DIR = "/Users/Praktikum/Documents/HL428/Roiss_L-428"
SOURCE_SUB_DIRS = ["Both", "Control", "Etoposide", "Resveratrol"]
TARGET_DIR = "/Users/Praktikum/Documents/HL428/Roiss_L-428_aggregated"

for subdir in SOURCE_SUB_DIRS:
    # create empty list for file paths
    file_paths = []
    # iterate over all files in all subdirectories
    for root, dirs, files in os.walk(SOURCE_DIR + "/" + subdir):
        for file in files:
            file_paths.append(os.path.join(root.lstrip(SOURCE_DIR), file))

    # copy file from filepath to new directory
    for file_path in file_paths:
        if "veratrol" in file_path:
            file_path = file_path.replace("veratrol", "Resveratrol")
        # print(file_path)
        copy_file_and_rename(file_path)
    print("file_cnt", len(file_paths))
