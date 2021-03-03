import os
import arcpy as ap
import csv
from .helpers import deleteFolder

def csv_locs(date):
    csvs = [
        {'org_csv': f'METROBUS-STOPBYLINE_EXTRACTION-WITH-DISTANCE{date}.csv', 
        'type': 'stopsbyline', 
        'columns': ['Seq', 'SignID', 'StopID', 'StopAbbr', 'StopName', 'OnSt', 'AtSt', 'StopPos', 'PrefTrans', 'Bench', 'Shelter', 'Transfer', 'ADA', 'PubWay', 'Node', 'LineName', 'RouteCode', 'Dir', 'CountyCode', 'Juris', 'GPS_Lon', 'GPS_Lat', 'Dist', '']},
        {'org_csv': f'METROBUS-STOP-EXTRACTION{date}.csv', 
        'type': 'stops', 
        'columns': ['SignID', 'StopID', 'StopAbbr', 'StopName', 'OnSt', 'AtSt', 'Lines', 'Routes', 'StopPos', 'PrefTrans', 'Bench', 'Shelter', 'Transfer', 'ADA', 'PubWay', 'CountyCode', 'Juris','GPS_Lon', 'GPS_Lat', '']},
        {'org_csv': f'METRO_PATTERNS{date}.csv', 
        'type': 'patterns', 
        'columns': ['SignID', 'ShapeID', 'RouteAbbr', 'DirName', 'LineName','PubNum', 'LineNum', 'shape_lat', 'shape_lon', 'shape_pt_sequence', '']},
        {'org_csv': f"ADA-ROUTES-LIST.csv", 
        'type': 'ada', 
        'columns': ['type', 'ADAAbbr', '']},
        {'org_csv': f'METROBUS-GHOSTSTOPS{date}.csv', 
        'type': 'ghoststops', 
        'columns': ['SignID','StopID','StopAbbr','StopName','OnSt','AtSt','StopPos','PrefTrans','Bench','Shelter','Transfer','ADA','PubWay','CountyCode','Juris','GPS_Lon','GPS_Lat','']}
        ]
       
    new_csvs = []

    for item in csvs:    
        if os.path.exists(os.path.join(os.environ['SQL_EXPORTS']), item['org_csv']):
            new_csvs.append(item)
    return new_csvs

def add_columns(sql_exports, csvs, folder_name):
    # add in missing columns from
    for item in csvs:
        org_csv_loc = os.path.join(sql_exports, item['org_csv'])
        new_csv_loc = os.path.join(sql_exports, rf'{folder_name}\{item["org_csv"]}')

        # check for, delete, and make folder with folder_name (date)
        deleteFolder(os.path.join(sql_exports, folder_name))
        os.mkdir(os.path.join(sql_exports, folder_name))

        all_rows = [item['columns']]
        # Read the entire file into memory:
        with open(org_csv_loc, 'r') as f:
            reader = csv.reader(f)  # pass the file to our csv reader
            for row in reader:     # iterate over the rows in the file
                all_rows.append(row)

        # Do not modify original file - we will make a copy:
        # deleteFeatureClass(item['org_csv'], sql_exports)

        with open(new_csv_loc, 'w', newline='') as f:
            # Overwrite the old file with the modified rows
            writer = csv.writer(f)
            writer.writerows(all_rows)

    # returns the full path of the new csv directory
    return {"org_dir": sql_exports, "processed_dir": os.path.join(sql_exports, folder_name)}

def update_current(config):
    
    ap.env.overwriteOutput = True

    for item in config['updateList']:
        print('********************************************************************************************************')
        print(f'Start of {item} creation in CurrentFiles.gdb')
        print('********************************************************************************************************')

        working = os.path.join(config.ds_gdb, f"{item}_{config.sign}_{config.pattern_file_date}")
        # deleteFeatureClass(os.path.join(config.cf_gdb, f"{item}_REGISTERED"), config.cf_gdb)
        ap.FeatureClassToFeatureClass_conversion(working, config.cf_gdb, f"{item}_REGISTERED")
        print(f'{item}_REGISTERED replaced in CurrentFile.gdb')
        print(' ')