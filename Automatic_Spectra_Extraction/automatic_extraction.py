import pandas as pd
import shutil
import os


# parse date into format YY_MM_DD
def parse_date(date):
    date = date.strftime("%y_%m_%d")
    return date

def copy_file_and_rename(file):
    #get information from path
    properties = file.split("/")
    substrate = properties[0]
    state = properties[1]
    time = properties[2]
    date = properties[3]
    directory = properties[4]
    file_name = properties[5]

    source_file = SOURCE_DIR + "/" + file
    file_exists = os.path.isfile(source_file)
    destination_folder = TARGET_DIR + "/" + substrate + "/" + state + "/" + time
    destination_file = destination_folder + "/" + date + "_" + directory + "_" + file_name

    try:
        os.makedirs(destination_folder, exist_ok=True)
        shutil.copyfile(source_file, destination_file)
    except Exception as e:
        print(e)
    return


EXCEL_FILE = "/Users/Praktikum/Desktop/Quality_Spectra.xlsx"

SUBSTRATES = ["Ag1", "Ag2", "Au", "In_Situ"]
TIME = ["Start", "End"]
STATE = ["Induced", "Non_Induced"]

SOURCE_DIR = "/Users/Praktikum/Documents/E_Coli/Steininger_E_Coli_Messung"
TARGET_DIR = "/Users/Praktikum/Documents/E_Coli/Steininger_E_Coli_By_Substrate_State_Time"

for substrate in SUBSTRATES:
    df = pd.read_excel(EXCEL_FILE, substrate)  # read sheet
    df_filtered = df[df['Type'].isna()]  # filter out rows with type
    # create emmpty list for file paths
    file_paths = []
    # fill list with file paths
    for index, row in df_filtered.iterrows():
        file_paths.append(substrate + "/" + row["State"] +"/"+ row["Time"] + "/" + parse_date(row["Date"]) + "/" + str(
            row["Directory"]) + "/" + row["File"])
    #copy file from filepath to new directory
    for file_path in file_paths:
        copy_file_and_rename(file_path)
