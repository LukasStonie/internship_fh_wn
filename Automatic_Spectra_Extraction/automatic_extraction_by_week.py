import numpy as np
import pandas as pd
import shutil
import os
from datetime import datetime, timedelta


# parse date into format YY_MM_DD
def parse_date(date):
    tmp = date.strftime("%y_%m_%d")
    return tmp

def copy_file_and_rename(file, week_number):
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
    destination_folder = TARGET_DIR + "/" + substrate + "/" + state + "/" + time+"/"+week_number
    destination_file = destination_folder + "/" + date + "_" + directory + "_" + file_name

    try:
        os.makedirs(destination_folder, exist_ok=True)
        shutil.copyfile(source_file, destination_file)
    except Exception as e:
        print(e)
    return


def get_creation_date(file_path):
    # Extract the date portion from the file path
    # sample file path  Au/Non_Induced/Start/22_10_06/2/EXTRACT.1
    date_str = file_path.split("/")[3]
    return datetime.strptime(date_str, '%y_%m_%d')

def get_calendar_week(date):
    # get calendar week from date
    return date.strftime('%W')

EXCEL_FILE = "/Users/Praktikum/Desktop/Quality_Spectra.xlsx"

SUBSTRATES = ["Ag1", "Ag2", "Au", "In_Situ"]
TIME = ["Start", "End"]
STATE = ["Induced", "Non_Induced"]

SOURCE_DIR = "/Users/Praktikum/Documents/E_Coli/Steininger_E_Coli_Messung"
TARGET_DIR = "/Users/Praktikum/Documents/E_Coli/Steininger_E_Coli_By_Substrate_State_Week"

for substrate in SUBSTRATES:
    df = pd.read_excel(EXCEL_FILE, substrate)  # read sheet
    df_filtered = df[df['Type'].isna()]  # filter out rows with type
    # create empty list for file paths
    file_paths = []



    # fill list with file paths
    for index, row in df_filtered.iterrows():
        file_paths.append(substrate + "/" + row["State"] +"/"+ row["Time"] + "/" + parse_date(row["Date"]) + "/" + str(
            row["Directory"]) + "/" + row["File"])

    # group files by week
    grouped_files = {}
    for file_path in file_paths:
        creation_date = get_creation_date(file_path) # parse the date from the file name
        week_start = get_calendar_week(creation_date)  # get the calendar week from the date
        if week_start in grouped_files:
            grouped_files[week_start].append(file_path)
        else:
            grouped_files[week_start] = [file_path]
    print(grouped_files.keys())
    for week, files in grouped_files.items():
        for file in files:
            e = 0
           # copy_file_and_rename(file, week)

