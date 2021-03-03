import arcpy as ap
import os
import shutil
import glob
import shutil
import csv


def date(text):
    for file in glob.glob(text):
        dates = []
        dates.append(int(file[-10:-4]))
    date = str(max(dates))
    print(f'{text[:-1]} Date: {date}')
    return date

def current_sign(stops_input_loc):
    with open(stops_input_loc, 'r') as file:
        reader = csv.reader(file)  # pass the file to our csv reader
        i = next(reader)  # second row (first row of data)
        s = i[0]  # first column in second row (first row of data)
    print(f'SIGN: {s}')
    return s

def deleteFeatureClass(file, loc):
    org_loc = ap.env.workspace
    ap.env.workspace = loc
    if ap.Exists(file):
        ap.Delete_management(file)
        print(f'Deleted {file} from {loc}')
    else:
        print("Nothing to Delete!!! Moving on with script.")
    ap.env.workspace = org_loc

def deleteFolder(loc):
    if os.path.exists(loc) and os.path.isdir(loc):
        shutil.rmtree(loc)
        print(f"{loc} DELETED!!!")

def clipCalc(table, fields):
    for field in fields:
        ap.CalculateField_management(table, f"!{field}! * !sqmiles_coverage!", "PYTHON3")
        print(f"Recalculated {field}!!!")
    print("-------------------------------------------")
    print(" ")
    print(f"Finished Calculating Fields for {table}!!!")

def replaceGDB(root_dir, gdb):
    if os.path.exists(os.path.join(root_dir, gdb)):
        ap.ClearWorkspaceCache_management(os.path.join(root_dir, gdb))
        deleteFolder(os.path.join(root_dir,gdb))
    ap.CreateFileGDB_management(root_dir, gdb)
    print("GEODATABASE CREATED!!!")

def calcSqMiles(fc, field):
    ap.CalculateField_management(fc, field, '!shape.area@squaremiles!', 'PYTHON3')


def clipPolygons(census_gdb, census_file, boundary_file, output_gdb, output_file):
    init_file = f'{census_file}_init'

    # copy files to new gdb
    ap.env.workspace = census_gdb
    ap.FeatureClassToFeatureClass_conversion(census_file, output_gdb, init_file)

    # switch to ouput gdb
    ap.env.workspace = output_gdb

    # rename fields
    ap.AddFields_management(init_file,[
        ['SqMiles','DOUBLE'],
        ['SqMiles_Clip','DOUBLE'],
        ['Coverage','DOUBLE']])

    # calculate the initial sq miles for the unclipped census polygons
    calcSqMiles(init_file, 'SqMiles')

    # clip and recalculate sq miles in SqMIiles_clip field
    ap.Clip_analysis(init_file, boundary_file, output_file)
    calcSqMiles(output_file, 'SqMiles_clip')

    # calculate percent coverage of clip
    ap.CalculateField_management(output_file, 'coverage', '!SqMiles_clip! / !SqMiles!', 'PYTHON3')

    # recalculate all of the fields bases on the coverage field


def joinAndCalcFields(fc, census_gdb, output_gdb, key, table, table_key, fields_list):
    #add field
    org_loc = ap.env.workspace
    ap.env.workspace = census_gdb
    ap.TableToTable_conversion(table, output_gdb, table)
    ap.env.workspace = output_gdb
    ap.JoinField_management(fc, key, table, table_key, fields_list)

    #calculate field
    for field in fields_list:
        ap.CalculateField_management(fc, field, f"!{field}! * !coverage!")
        print(f"{field} calculated")
    ap.env.workspace = org_loc

def cleanUp(working_file, gdb, final_file, final_gdb_loc, delete_fields):
    org_loc = ap.env.workspace
    ap.env.workspace = gdb
    
    deleteFeatureClass(final_file, final_gdb_loc)

    ap.FeatureClassToFeatureClass_conversion(working_file, ap.env.workspace, final_file)

    for field in delete_fields:
        ap.DeleteField_management(final_file, field)
        print("---------------------------")
        print(field + " DELETED")
        print("---------------------------")

    print("Minority_Final feature class created - Script Complete!!!")

    ap.ClearWorkspaceCache_management()

    deleteFeatureClass(final_file, final_gdb_loc)

    # CREATE FINAL FEATURE CLASS
    ap.FeatureClassToFeatureClass_conversion(final_file, final_gdb_loc, final_file)
    print("---------------------------")

    ap.env.workspace = org_loc


def checkforfield(fc, field, type):
    if field not in ap.ListFields(fc, field):
        return
    else:
        ap.DeleteField_management(fc, field)
        ap.AddField_management(fc, field, type)

def clearDataStore(dir, date):
    replaceGDB(dir, f"DataStore_{date}.gdb")