import arcpy as ap
import os
import shutil
import glob
import shutil
import csv
from dotenv import load_dotenv


# get the max date from all of the files with the prefix of text
# the date is everything that happens after text 
# the greatest date is found and should be that monday's date
def date(text):
    for file in glob.glob(text):
        dates = []
        dates.append(int(file[-10:-4]))
    date = str(max(dates))
    print(f'{text[:-1]} Date: {date}')
    return date

# get the current sign from the stops csv export by reading off the first row's signid column
def current_sign(stops_input_loc):
    with open(stops_input_loc, 'r') as file:
        reader = csv.reader(file)  # pass the file to our csv reader
        i = next(reader)  # second row (first row of data)
        s = i[0]  # first column in second row (first row of data)
    print(f'SIGN: {s}')
    return s

# helper function to delete a feature class IF it exists, 
# will change directories to loc during the function
def deleteFeatureClass(file, loc):
    org_loc = ap.env.workspace
    ap.env.workspace = loc
    if ap.Exists(file):
        ap.Delete_management(file)
        print(f'Deleted {file} from {loc}')
    else:
        print("Nothing to Delete!!! Moving on with script.")
    ap.env.workspace = org_loc

# deletes folder if it exists
def deleteFolder(loc):
    if os.path.exists(loc) and os.path.isdir(loc):
        shutil.rmtree(loc)
        print(f"{loc} DELETED!!!")

# helper function to recalculate list of fields with coverage field
def clipCalc(table, fields):
    for field in fields:
        ap.CalculateField_management(table, f"!{field}! * !sqmiles_coverage!", "PYTHON3")
        print(f"Recalculated {field}!!!")
    print("-------------------------------------------")
    print(" ")
    print(f"Finished Calculating Fields for {table}!!!")

# delete gdb and replace with a fresh gdb
def replaceGDB(root_dir, gdb):
    if os.path.exists(os.path.join(root_dir, gdb)):
        ap.ClearWorkspaceCache_management(os.path.join(root_dir, gdb))
        deleteFolder(os.path.join(root_dir,gdb))
    ap.CreateFileGDB_management(root_dir, gdb)
    print("GEODATABASE CREATED!!!")

# easy helper to recalc sq miles using field calculator
def calcSqMiles(fc, field):
    ap.CalculateField_management(fc, field, '!shape.area@squaremiles!', 'PYTHON3')

# check to see if field exists in data table for feature class
def checkforfield(fc, field, type):
    if field not in ap.ListFields(fc, field):
        return
    else:
        ap.DeleteField_management(fc, field)
        ap.AddField_management(fc, field, type)

# delete the weekly datastore gdb
def clearDataStore(dir, date):
    replaceGDB(dir, f"DataStore_{date}.gdb")

# print all of the fields
def printList(list, key=None):
    print(" ")
    print("----------------------------")
    print("creating csv's")
    if key is None:
        for item in list:
            print(f'  - {item}')
    else:
        for item in list:
            print(f'  - {item[key]}')
