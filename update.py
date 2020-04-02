import arcpy as ap
import os
import pandas as pd
import glob
import csv
import shutil
import sys
from arcgis.gis import GIS


# ************ VARIABLES ************


def date(text):
    for file in glob.glob(text):
        dates = []
        dates.append(int(file[-10:-4]))
    date = str(max(dates))
    print(f'{text[:-1]} Date: {date}')
    return date


def currentSign():
    with open(stops_input_loc, 'r') as file:
        reader = csv.reader(file)  # pass the file to our csv reader
        i = next(reader)  # second row (first row of data)
        s = i[0]  # first column in second row (first row of data)
    print(f'SIGN: {s}')
    return s


# DEFAULT DIRECTORIES
title_vi = r"\\metroas08\arcgisdatastore\Open Data Admin\TitleVI\Final_17.gdb" # \\metroas08\arcgisdatastore\Open Data Admin\TitleVI\Final_17.gdb  or r'A:\Open Data Admin\TitleVI\Final_17.gdb
AutomationExports = r'\\metroas08\arcgisdatastore\Open Data Admin\AutomationExports' # \\metroas08\arcgisdatastore\Open Data Admin\AutomationExports or r'A:\Open Data Admin\AutomationExports
sql_exports = r'\\metroas08\arcgisdatastore\Open Data Admin\SQL_Exports' # r'W:\Transfer\wkjenkins' or r'A:\Open Data Admin\SQL_Exports\SQL_Exports'

exports_dir = input(rf"Where are the data files? ")
title_vi_gdb = input(rf'Where is the the TitleVI Geodatabase: ')


os.chdir(sql_exports)

pattern_file_date = date('METRO_PATTERNS*')
date_formatted = f'{pattern_file_date[2:4]}/{pattern_file_date[4:7]}/{pattern_file_date[:2]}'
stops_date = date('METROBUS-STOP-EXTRACTION*')
stops_by_line_date = stops_date

# PATTERN VARIABLES
patterns_name = f'METRO_PATTERNS{pattern_file_date}'
patterns_csv = os.path.join(sql_exports, f'{patterns_name}.csv')
patterns_table = os.path.join(sql_exports, f'h_{patterns_name}.csv')


# STOPS VARIABLES
stops_input = f'METROBUS-STOP-EXTRACTION{stops_date}'
stops_input_loc = os.path.join(sql_exports, f'{stops_input}.csv')
stops_table = os.path.join(sql_exports, f'h_{stops_input}.csv')


# STOPS BY LINE VARIABLES
stopsbyline_input = f'METROBUS-STOPBYLINE_EXTRACTION-WITH-DISTANCE{stops_by_line_date}'
stopsbyline_input_loc = os.path.join(sql_exports, f'{stopsbyline_input}.csv')
stopsbyline_table = os.path.join(sql_exports, f'h_{stopsbyline_input}.csv')

sign = currentSign()

# WORKING DIRECTORIES
ds_gdb = os.path.join(AutomationExports, f"DataStore_{pattern_file_date}.gdb")
cf_gdb = os.path.join(AutomationExports, "CurrentFiles.gdb")


acs_year = title_vi_gdb[-6:-4]
ap.env.workspace = os.path.join(AutomationExports, ds_gdb)

# PATTERNS POINTS VARIABLES
patterns_xy = f'{ap.env.workspace}\{patterns_name}_XY_{pattern_file_date}'
patterns_xy_loc = os.path.join(ds_gdb, patterns_xy)

# PATTERNS LINE VARIABLES
patterns_line = f'{patterns_name}_{sign}'
patterns_line_loc = os.path.join(ds_gdb, patterns_line)

# PATTERNS ATTRIBUTE TABLES
patterns_group = f'{patterns_name}_group_{sign}_{pattern_file_date}'

# STOPS VARIABLES
stops_output = f'MetroBusStops_{sign}_{stops_date}'
stops_output_loc = os.path.join(ds_gdb, stops_output)

# STOPS VARIABLES
stopsbyline_input = f'METROBUS-STOPBYLINE_EXTRACTION-WITH-DISTANCE{stops_by_line_date}'
stopsbyline_input_loc = os.path.join(sql_exports, f'{stopsbyline_input}.csv')

# STOPS BY LINE VARIABLES
stopsbyline_output = f'MetroBusStopsByLine_{sign}_{stops_by_line_date}'
stopsbyline_output_loc = os.path.join(ds_gdb, stopsbyline_output)

# ROUTES VARIABLES
routes_dir_line = f'MetroBusRoutes_dir_{sign}_{pattern_file_date}'
routes_dir_loc = os.path.join(ds_gdb, routes_dir_line)
routes_line = f'MetroBusRoutes_{sign}_{pattern_file_date}'
routes_loc = os.path.join(ds_gdb, routes_line)
routes_csv = f'Routes_{pattern_file_date}.csv'
routes_csv_loc = os.path.join(AutomationExports, f'exports\{routes_csv}')

ada_csv_loc = os.path.join(AutomationExports, f"ADA-ROUTES-LIST.csv") #
# PATTERN VARIABLES
ada_name = f'ADA-ROUTES-LIST'
ada_csv_loc = os.path.join(sql_exports, f"{ada_name}.csv")
ada_table = os.path.join(sql_exports, f'h_{ada_name}.csv')


# CLEAR OUT THE LOG FILE (FOR IF YOU ARE RUNNING MULITPLE TIMES A DAY)
if os.path.exists(os.path.join(os.getcwd(), rf'log_{pattern_file_date}.txt')):
    os.remove(os.path.join(os.getcwd(), rf'log_{pattern_file_date}.txt'))


def log(statement):
    file = os.path.join(AutomationExports, rf'log_{pattern_file_date}.txt')
    if not os.path.exists(file):
        open(file, 'a').close()

    print_log = open(file, 'a+')  # append statement to the end of the file
    print_log.write(f'\n{statement}')
    print_log.close()
    print(statement)



log('')
log('******************************************************************************************************************')
log(f"Waiting for ArcGIS online credentials...")
agol_user = input(f"USERNAME: ")
agol_password = input("PASSWORD: ")
agol_url = 'https://www.arcgis.com/'
agolProj = input('Where is the AGOL local project? ')  # A:\ is the data store folder on \\metroas08\


log('')
log('******************************************************************************************************************')
log(f"Waiting for Enterprise credentials...")
enterprise_user = input(f"USERNAME: ")
enterprise_password = input("PASSWORD: ")
enterprise_url = input('ArcGIS Server URL: ')
enterpriseProj = input('Where is the enterprise server project? ')
log(' ')

print(f'os.getcwd():{os.getcwd()}')


feature_classes = [{"title": "MetroBusRoutes",
            "view_title": "Metro St. Louis MetroBus Routes",
            "summary": f"Current MetroBus Routes for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes for the Metro Saint Louis Transit system as of {date_formatted}. "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984</div></div>"
                           f"<div><div><br /><b>Field Names and Descriptions:</b>"
                           f"<div><div><br />RouteAbbr: Private Route code (Text)"
                           f"<div><div><br />LineName: Public Route Number and Route Name "
                           f"<div><div><br />PubNum: Public Route Number "
                           f"<div><div><br />LineNum: Private Route code (Integer)"
                           f"<div><div><br />ADA: Does this route have ADA Call-a-ride service (1 = True, 0 = False)",

            "tags": ["routes", "metrobus", "bus"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroBusStops",
            "view_title": "Metro St. Louis MetroBus Stops",
            "summary": f"Current MetroBus Stops for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Stops for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b>"
                           f"<div><div><br />Seq: Stop Sequence"
                           f"<div><div><br />SignID: Sign associated with the schedule release with file"
                           f"<div><div><br />StopID: Id associated with the Stop location"
                           f"<div><div><br />StopAbbr: Stop Abbreviation"
                           f"<div><div><br />StopName: Stop Name"
                           f"<div><div><br />OnSt: Street that the stop is on"
                           f"<div><div><br />AtSt: Cross street that the stop is on"
                           f"<div><div><br />StopPos: Stop Position"
                           f"<div><div><br />PrefTrans: Preferred Transfer location"
                           f"<div><div><br />Bench: Bench located at stop (1 = True, 0 = False)"
                           f"<div><div><br />Shelter: Shelter located at stop (1 = True, 0 = False)"
                           f"<div><div><br />Transfer: Transfer located at stop (1 = True, 0 = False)"
                           f"<div><div><br />PubWay: Stop in public right of way (1 = True, 0 = False)"
                           f"<div><div><br />Node: Id for timepoint"
                           f"<div><div><br />LineName: Public number and route name associated with this iteration of the stop."
                           f"<div><div><br />RouteCode: Private route code associated with this iteration of the stop."
                           f"<div><div><br />Dir: Direction of route"
                           f"<div><div><br />CountyCode: County code where the stop is located"
                           f"<div><div><br />Juris: Jurisdiction code where the stop is located"
                           f"<div><div><br />GPS_Lon: Longitude"
                           f"<div><div><br />GPS_Lat: Latitude",
            "tags": ["stops","metrobus","bus"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroBusStopsByLine",
            "view_title": "Metro St. Louis MetroBus Stops By Line",
            "summary": f"Current MetroBus Stops by Line for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Stops by Line for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />Seq: Stop Sequence"
                           f"<div><div><br />SignID: Sign associated with the schedule release with file"
                           f"<div><div><br />StopID: Id associated with the Stop location"
                           f"<div><div><br />StopAbbr: Stop Abbreviation"
                           f"<div><div><br />StopName: Stop Name"
                           f"<div><div><br />OnSt: Street that the stop is on"
                           f"<div><div><br />AtSt: Cross street that the stop is on"
                           f"<div><div><br />StopPos: Stop Position"
                           f"<div><div><br />PrefTrans: Preferred Transfer location"
                           f"<div><div><br />Bench: Bench located at stop (1 = True, 0 = False)"
                           f"<div><div><br />Shelter: Shelter located at stop (1 = True, 0 = False)"
                           f"<div><div><br />Transfer: Transfer located at stop (1 = True, 0 = False)"
                           f"<div><div><br />PubWay: Stop in public right of way (1 = True, 0 = False)"
                           f"<div><div><br />Node: Id for timepoine"
                           f"<div><div><br />LineName: Public number and route name associated with this iteration of the stop."
                           f"<div><div><br />RouteCode: Private route code associated with this iteration of the stop."
                           f"<div><div><br />Dir: Direction of route"
                           f"<div><div><br />CountyCode: County code where the stop is located"
                           f"<div><div><br />Juris: Jurisdiction code where the stop is located"
                           f"<div><div><br />GPS_Lon: Longitude"
                           f"<div><div><br />GPS_Lat: Latitude"
                           f"<div><div><br />Dist: Distance to next stop",
            "tags": ["stops by line", "stops", "metrobus", "bus"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroFacilities",
            "view_title": "Metro St. Louis Facilities Locations",
            "summary": f"Current Metro Saint Louis Transit Facility Location points as of {date_formatted}.",
            "description": f"Current Metro Saint Louis Transit Facility Locations as of {date_formatted}."
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />NAME: Name of Facility"
                           f"<div><div><br />TYPE: Type of Facility"
                           f"<div><div><br />ADDRESS: Mailing Address"
                           f"<div><div><br />CITY: City"
                           f"<div><div><br />STATE: State"
                           f"<div><div><br />ZIP: Zipcode"
                           f"<div><div><br />POINT_X: Longitude"
                           f"<div><div><br />POINT_Y: Latitude",
            "tags": ["metrolink", "light rail", "metrobus", "bus", "assets"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroFacilitiesPoly",
            "view_title": "Metro St. Louis Facilities Boundaries",
            "summary": f"Current Metro Saint Louis Transit Facility Location polygons as of {date_formatted}.",
            "description": f"Current Metro Saint Louis Transit Facility Location polygons as of {date_formatted}. "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />NAME: Name of Facility"
                           f"<div><div><br />TYPE: Type of Facility",
            "tags": ["metrolink", "light rail", "metrobus", "bus", "assets"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroLinkAlignment",
            "view_title": "MetroLink Alignment",
            "summary": f"Current MetroLink light rail Alignment for the Metro Saint Louis Transit system covering the Blue and Red lines as of {date_formatted}.",
            "description": f"Current MetroLink light rail Alignment for the Metro Saint Louis Transit system covering the Blue and Red lines as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />I_RTE_CO: Internal Route Code"
                           f"<div><div><br />RTE_NAME: Route Name"
                           f"<div><div><br />P_RTE_CO: Private Route Code",
            "tags": ["metrolink", "light rail", "alignment"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroLinkStations",
            "view_title": "MetroLink Stations",
            "summary": f"MetroLink Stations for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"MetroLink Stations for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />SIGNID: Updated Sign ID sign assciated with the service update that is associated with the last update "
                           f"<div><div><br />Stop ID (STP_ID): Official Stop ID code "
                           f"<div><div><br />STP_ABBR: Stop Abbreviation "
                           f"<div><div><br />Stop Name (STP_NAME): The official Public name of the stop "
                           f"<div><div><br />On Street (ON_ST): The On Street that the Station is physically located on. "
                           f"<div><div><br />At Street (AT_ST): The At Street that the Station is located (Adjacent road) "
                           f"<div><div><br />STP_P: Stop Position "
                           f"<div><div><br />P_TRF: If the station is a preferred transfer (1 = True, 0 = False) "
                           f"<div><div><br />BNCH: If the station has a bench (1 = True, 0 = False) "
                           f"<div><div><br />SHLT: If the station has a shelter (1 = True, 0 = False) "
                           f"<div><div><br />TRF: If the station is a transfer location (1 = True, 0 = False) "
                           f"<div><div><br />County: County that the Station is in "
                           f"<div><div><br />Municipality (JURIS): Municipality the Station is in "
                           f"<div><div><br />GPS_LON: Longitude "
                           f"<div><div><br />GPS_LAT: Latitude",
            "tags": ["metrolink", "light rail", "assets"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "ServiceArea",
            "view_title": "MetroBus & MetroLink Service Area",
            "summary": f"Metro Service Area for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Metro Service Area for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />STATEFP: Census State Code"
                           f"<div><div><br />COUNTYFP: Census County Code "
                           f"<div><div><br />AFFGEOID: Full Census GeoID"
                           f"<div><div><br />GEOID: Census State County Code"
                           f"<div><div><br />NAME: Name of County"
                           f"<div><div><br />StCoCode: Census State County Code",
            "tags": ["service area", "polygons", "service area"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroBusRoutes_dir",
            "view_title": "MetroBus & MetroLink St. Louis Route Buffers by Route Direction",
            "summary": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984 "
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />RouteAbbr: Private Route Number (Text) "
                           f"<div><div><br />DirName: Direction name of route feature "
                           f"<div><div><br />LineName: Public Route Number and Name "
                           f"<div><div><br />PubNum: Public Route Name "
                           f"<div><div><br />LineNum:	Private Route Number (Integer)"
                           f"<div><div><br />ADA: Does this route have ADA Call-a-ride service (1 = True, 0 = False)",
            "tags": ["routes","metrobus","bus"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "SystemBuffers",
            "view_title": "MetroBus & MetroLink St. Louis System Buffers",
            "summary": f"Current MetroBus System buffered by 1/4, 1/2, and 3/4 miles for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.  <div><div><br />Date Published: {date_formatted} <div><div><br />Projection: WGS1984 "
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />type: States the buffer type "
                           f"<div><div><br />ClipPop025: Estimated population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipMin025: Estimated Minority population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipLEP025: Estimated Limited English Proficiency population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipPov025: Estimated Poverty population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipSen025: Estimated Senior population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipNoCar025: Estimated population with no cars in household within 0.25 miles of system buffer "
                           f"<div><div><br />ClipLowCar025: Estimated population within a Low Car household within 0.25 miles of system buffer"
                           f"<div><div><br />ClipPop050: Estimated population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipMin050: Estimated Minority population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipLEP050: Estimated Limited English Proficiency population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipPov050: Estimated Poverty population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipSen050: Estimated Senior population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipNoCar050: Estimated population with no cars in household within 0.50 miles of system buffer "
                           f"<div><div><br />ClipLowCar050: Estimated population within a Low Car household within 0.50 miles of system buffer "
                           f"<div><div><br />ClipPop075: Estimated population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipMin075: Estimated Minority population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipLEP075: Estimated Limited English Proficiency population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipPov075: Estimated Poverty population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipSen075: Estimated Senior population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipNoCar075: Estimated population with no cars in household within 0.75 miles of system buffer "
                           f"<div><div><br />ClipLowCar075: Estimated population within a Low Car household within 0.75 miles of system buffer "
                           f"<div><div><br />***ALL POPULATIONS ARE BASED ON THE 2017 US CENSUS. FOR METHODOLOGIES CONTACT METRO SAINT LOUIS RESEARCH & DEVELOPMENT",
            "tags": ["system buffers", "system", "buffers", "transit", "bus"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "RouteBuffers",
            "view_title": "MetroBus & MetroLink St. Louis Route Buffers",
            "summary": f"Current MetroBus Routes buffered by 1/4, 1/2, and 3/4 miles for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.  <div><div><br />Date Published: {date_formatted} <div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />RouteAbbr: Private Route Code (Text)"
                           f"<div><div><br />LineName: Public Route Number and Name"
                           f"<div><div><br />PubNum: Public Route Number"
                           f"<div><div><br />LineNum: Private Route Number (Integer"
                           f"<div><div><br />BUFF_DIST: Distance the Route was Buffered (Miles)",
            "tags": ["route buffers", "route", "buffers", "bus"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroADAServiceArea",
            "view_title": "Metro St. Louis ADA Service Area",
            "summary": f"Current MetroBus Routes buffered by 1/4, 1/2, and 3/4 miles for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted}"
                           f"<div><div><br />Projection: WGS1984 "
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br /><br />Name: Name of the service area",
            "tags": ["system", "route", "buffers", "bus", "ada"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "CurrentSystem",
            "view_title": "Current MetroBus & MetroLink Stops and Routes",
            "summary": f"Current MetroBus and MetroLink system for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus and MetroLink system for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br /><br />Date Published: {date_formatted} "
                           f"<div><div><br /><br />Projection: WGS1984",
            "tags": ["route buffers", "route", "bus", "metrobus", "metrolink"],
            "enterprise": True,
            "agol": True,
            "enterprise_fields": [],
            "agol_fields": [],
            },
            ]


def featureList(fc_list, portal):
    list = []

    log('')
    log("*******************************************************************************************************************")
    log(f'The following have been added to the {portal} Feature Class List')
    log("*******************************************************************************************************************")
    log('')

    for fc in fc_list:
        if fc[portal] is True:
            list.append(fc)
            log(f"- {fc['title']}")

    log('')
    log('--- END OF LIST ---')
    log('')
    return list



agol_fc = featureList(feature_classes, 'agol') # add feature
enterprise_fc = featureList(feature_classes, 'enterprise')

# DELETE AND REPLACE ARCGIS FILES/FEATURE CLASSES LOCALLY
def deleteAndReplace(file, loc):
    if ap.Exists(file):
        ap.Delete_management(file)
        log(f'Deleted {file} from {loc}')
    else:
        log(f'{file} is not present.')
        log("Nothing to Delete!!! Moving on with script.")


# DELETE AND REPLACE FOLDERS LOCALLY
def deleteFolder(loc):
    if os.path.exists(loc) and os.path.isdir(loc):
        shutil.rmtree(loc)
        log(f"{loc} DELETED!!!")


def clearDataStore():
    confirm = input(f"Are you sure you want to delete the datastore?: (y/n)")
    if confirm == 'y':
        deleteFolder(ds_gdb)
        ap.CreateFileGDB_management(AutomationExports, f"DataStore_{pattern_file_date}.gdb")


def addCollumns():
    patterns_columns = ['SignID', 'ShapeID', 'RouteAbbr', 'DirName', 'LineName','PubNum', 'LineNum', 'shape_lat', 'shape_lon', 'shape_pt_sequence', '']
    stops_columns = ['SignID', 'StopID', 'StopAbbr', 'StopName', 'OnSt', 'AtSt', 'Lines', 'Routes', 'StopPos', 'PrefTrans', 'Bench', 'Shelter', 'Transfer', 'ADA', 'PubWay', 'CountyCode', 'Juris','GPS_Lon', 'GPS_Lat', '']
    stops_by_line_columns = ['Seq', 'SignID', 'StopID', 'StopAbbr', 'StopName', 'OnSt', 'AtSt', 'StopPos', 'PrefTrans', 'Bench', 'Shelter', 'Transfer', 'ADA', 'PubWay', 'Node', 'LineName', 'RouteCode', 'Dir', 'CountyCode', 'Juris', 'GPS_Lon', 'GPS_Lat', 'Dist', '']
    ada_columns = ['type', 'ADAAbbr', '']
    files_spec = [{'file': stopsbyline_input_loc, 'table': stopsbyline_table, 'columns': stops_by_line_columns},
                  {'file': stops_input_loc, 'table': stops_table, 'columns': stops_columns},
                  {'file': patterns_csv, 'table': patterns_table, 'columns': patterns_columns},
                  {'file': ada_csv_loc, 'table': ada_table, 'columns': ada_columns}]

    for file in files_spec:
        all_rows = [file['columns']]
        # Read the entire file into memory:
        with open(file['file'], 'r') as f:
            reader = csv.reader(f)  # pass the file to our csv reader
            for row in reader:     # iterate over the rows in the file
                all_rows.append(row)

        # Do not modify original file - we will make a copy:
        deleteAndReplace(file['table'], '')

        with open(file['table'], 'w', newline='') as f:
            # Overwrite the old file with the modified rows
            writer = csv.writer(f)
            writer.writerows(all_rows)


def routesCreation():
    deleteAndReplace(patterns_xy, ds_gdb)
    # TURN CSV TO POINTS FEATURE CLASS
    ap.management.XYTableToPoint(patterns_table, patterns_xy, "shape_lon", "shape_lat", "", ap.SpatialReference(4326))
    log("Created Points file from CSV file")

    # CHECK FOR FILE AND DELETE IF IT EXISTS
    deleteAndReplace(patterns_line, ds_gdb)
    ap.PointsToLine_management(patterns_xy,
                               patterns_line,
                               'ShapeID',
                               'SHAPE_PT_SEQUENCE')

    log("Created Line file from Point file")

    # ADD IN PATTERNS GROUP ATTRIBUTES TO PATTERNS LINE
    ap.JoinField_management(patterns_line_loc, 'ShapeID', patterns_table, 'ShapeID', [
                            'RouteAbbr', 'DirName', 'LineName', 'PubNum', 'PubName', 'LineNum'])
    log("Added fields to Patterns")

    with ap.da.UpdateCursor(patterns_line_loc, ['ROUTEABBR']) as cursor:
        for row in cursor:
            if row[0] == 3599:
                cursor.deleteRow()

    ap.AddField_management(patterns_line_loc, "ADA", "SHORT")
    ap.JoinField_management(patterns_line_loc, 'PubNum', ada_table, 'ADAAbbr', ['ADAAbbr'])
    fields = ap.ListFields(patterns_line_loc)
    for field in fields:
        print(field.name)
        print(field.type)

    adaCalc = """def ada(adaRoute):
        if adaRoute is None:
            return 0
        else:
            return 1"""

    ap.CalculateField_management(patterns_line_loc, 'ADA', 'ada(!ADAAbbr!)', "PYTHON3", adaCalc)
    ap.DeleteField_management(patterns_line_loc, "ADAAbbr")

    #############################################################################################################

    # ROUTES BY DIRECTION CREATION

    #############################################################################################################



    deleteAndReplace(routes_dir_line, ds_gdb)

    # CREATE ROUTE DIR SHAPEFILE
    ap.Dissolve_management(patterns_line, routes_dir_line, ['ROUTEABBR', 'LINENAME', 'PUBNUM', 'LINENUM', 'DIRNAME', 'ADA'])
    log('Created Routes Dir Lines')


    #############################################################################################################

    # ROUTES CREATION

    #############################################################################################################

    deleteAndReplace(routes_line, ds_gdb)

    # CREATE ROUTE SHAPEFILE
    ap.Dissolve_management(patterns_line, routes_line, ['ROUTEABBR', 'LINENAME', 'PUBNUM', 'LINENUM', 'ADA'])
    log('Created Routes Lines')


    # DELETE MetroPatterns_XY
    ap.Delete_management(patterns_xy)


def routeBuffers():
    # MetroBusRoutes_Buffer and MetroBusSystem_Buffer
    buffer_list = [{'dist': '0.75 miles', 'name': '075'},
                   {'dist': '0.5 miles', 'name': '05'},
                   {'dist': '0.25 miles', 'name': '025'}]

    # BUFFERING 0.75, 0.5, 0.25 MILES
    for dist in buffer_list:

        # ROUTE BUFFER
        routes_buffer = f'MetroBusRouteBuffer_{dist["name"]}_{sign}_{pattern_file_date}'
        routes_buffer_loc = os.path.join(ds_gdb, routes_buffer)

        # DELETE DUPLICATE ROUTE FILE
        deleteAndReplace(routes_buffer, ds_gdb)

        ap.Buffer_analysis(routes_line, routes_buffer,
                           dist['dist'], "FULL", "ROUND", "NONE")
        log('Routes Buffered')

        # PATTERNS GROUP
        patterns_pd = pd.read_csv(patterns_table).groupby(
            ['RouteAbbr', 'LineName', 'PubNum', 'LineNum', 'ShapeID', 'DirName']).mean()
        patterns_pd.drop(['shape_lat', 'shape_lon', 'shape_pt_sequence'], axis=1)
        log('Unique Routes table created')

        # SYSTEM BUFFER
        mb_sys_buffer = f'MetroBusSystemBuffer_{dist["name"]}_{sign}_{pattern_file_date}'
        mb_sys_buffer_loc = os.path.join(ds_gdb, mb_sys_buffer)

        ap.Dissolve_management(routes_buffer, mb_sys_buffer)
        log('System Buffered')
        ap.AddField_management(mb_sys_buffer, 'type', 'TEXT')
        ap.CalculateField_management(mb_sys_buffer, 'type', '"system"')



    #############################################################################################################

    # TITLE VI POPULATION ANALYSIS

    #############################################################################################################

        # TITLE VI ANALYSIS FOR STANDARD FILES
        # ACS INPUT, TOTAL POPULATION FIELD, DENSITY POPULATION COUNT
        acs_list = [{'file_name': f'Minority{acs_year}_Final', 'pop': 'TPop', 'field': f'ClipPop{dist["name"]}', 'calc': '(!TPop!/!SqMiles!)'},
                    {'file_name': f'Minority{acs_year}_Final', 'pop': 'TMinority', 'field': f'ClipMin{dist["name"]}', 'calc': '!MinorityDens!'},
                    {'file_name': f'LEP{acs_year}_Final', 'pop': 'TLEP', 'field': f'ClipLEP{dist["name"]}', 'calc': '!LEPDens!'},
                    {'file_name': f'Poverty{acs_year}_Final', 'pop': 'TPov',  'field': f'ClipPov{dist["name"]}', 'calc': '!PovDens!'},
                    {'file_name': f'Senior{acs_year}_Final', 'pop': 'TSenior', 'field': f'ClipSen{dist["name"]}', 'calc': '!SeniorDens!'},
                    {'file_name': f'NoCar{acs_year}_Final', 'pop': 'TNoCar', 'field': f'ClipNoCar{dist["name"]}', 'calc': '!NoCarDens!'},
                    {'file_name': f'NoCar{acs_year}_Final', 'pop': 'TLowCar', 'field': f'ClipLowCar{dist["name"]}', 'calc': '!LowCarDens!'}]

        # LOOP FOR CALCULATING TITLE VI POPULCATION BUFFERS
        for acs in acs_list:
            # CALCULATE OUT FOR SYSTEM AND ROUTES BUFFER POPULATIONS

            acs_in = os.path.join(title_vi_gdb, acs['file_name'])
            acs_out = f'{mb_sys_buffer}_{acs["pop"]}'

            log('')
            log('-------------------------')
            log(f'Start of {acs_out} Creation')
            log('-------------------------')
            log('')

            # DELETE DUPLICATE ROUTE DIRECTION FILE
            deleteAndReplace(acs_out, title_vi_gdb)

            ap.Clip_analysis(acs_in, mb_sys_buffer, acs_out)

            # ap.Split_analysis(acs_in, type[0], type[1], title_vi_gdb)
            ap.AddFields_management(acs_out,
                                    [[acs['field'], 'DOUBLE'],
                                     ['ClipSqMiles', 'DOUBLE']])
            log(f'Added fields to {acs_out} ')
            ap.CalculateFields_management(acs_out, 'PYTHON3', [['ClipSqMiles', "!shape.area@squaremiles!"],
                                                               [acs['field'], f'{acs["calc"]} * !ClipSqMiles!']])
            log(f'Calculated fields for {acs_out}')

            # ap.JoinField_management(type, ,acs_out, )
            acs_out_diss = f'{acs_out}_dissolve'

            ap.Dissolve_management(acs_out, acs_out_diss, '', [[acs['field'], 'SUM']])
            ap.AddField_management(acs_out_diss, 'type', 'TEXT')
            ap.CalculateField_management(acs_out_diss, 'type', '"system"')
            ap.JoinField_management(mb_sys_buffer, 'type',
                                    acs_out_diss, 'type', f'SUM_{acs["field"]}')
            ap.AddField_management(mb_sys_buffer, acs['field'], 'DOUBLE')
            ap.CalculateField_management(mb_sys_buffer, acs["field"], f'!SUM_{acs["field"]}!')
            ap.DeleteField_management(mb_sys_buffer, f'SUM_{acs["field"]}')

            delete_list = [acs_out, acs_out_diss]
            for d in delete_list:
                ap.Delete_management(d)


def stopsCreation():
    deleteAndReplace(stops_output, ds_gdb)
    deleteAndReplace(stopsbyline_output, ds_gdb)

    ap.management.XYTableToPoint(stops_table, stops_output, 'GPS_LON', 'GPS_LAT', '', ap.SpatialReference(4326))
    log('Stops Created')
    ap.management.XYTableToPoint(stopsbyline_table, stopsbyline_output,'GPS_LON', 'GPS_LAT', '', ap.SpatialReference(4326))
    log('Stops By Line Created')

    county = os.path.join(cf_gdb, 'State_County')

    stops_state_county = os.path.join(ds_gdb, 'stopsStateCounty')

    deleteAndReplace(stops_state_county, cf_gdb)


    # STOPS COUNTY SPATIAL JOIN

    ap.SpatialJoin_analysis(stops_output, county, stops_state_county)


    # STOPS COUNTY CALUCLATION

    ap.AddField_management(stops_output, "CountyName", "TEXT")

    ap.JoinField_management(stops_output, "StopID", stops_state_county, "StopID", ["GEOID", "NAME"])

    ap.CalculateField_management(stops_output, f"CountyCode", '!GEOID!', "PYTHON3")
    ap.CalculateField_management(stops_output, f"CountyName", '!NAME!', "PYTHON3")

    ap.DeleteField_management(stops_output, "GEOID")
    ap.DeleteField_management(stops_output, "NAME")


    # STOPS BY LINE COUNTY CALCULATIONS

    ap.AddField_management(stopsbyline_output, "CountyName", "TEXT")

    ap.JoinField_management(stopsbyline_output, "StopID", stops_state_county, "StopID", ["GEOID", "NAME"])

    ap.CalculateField_management(stopsbyline_output, f"CountyCode", '!GEOID!', "PYTHON3")
    ap.CalculateField_management(stopsbyline_output, f"CountyName", '!NAME!', "PYTHON3")

    ap.DeleteField_management(stopsbyline_output, "GEOID")
    ap.DeleteField_management(stopsbyline_output, "NAME")

    log("done")
    log("results located @: " + AutomationExports)


def adaCreation(s):
    log('start of ada creation')
    sign=s
    mb_sys_buffer = f'MetroBusRouteBuffer_075_{sign}_{pattern_file_date}'
    mb_sys_buffer_loc = os.path.join(ds_gdb, mb_sys_buffer)

    # SETTING UP FOR MetroADAServiceArea
    ada_fill = os.path.join(cf_gdb, 'ADA_Fill')
    lightrail_buffer = os.path.join(cf_gdb, 'Lightrail_buffer')
    ada_system_merge = os.path.join(ds_gdb, f'MetroADASysMerge_{sign}_{pattern_file_date}')
    ada_service_area = os.path.join(ds_gdb, f'MetroADAServiceArea_{sign}_{pattern_file_date}')
    ada_route_buffer = f"ADARouteBuffer_{sign}_{pattern_file_date}"
    ada_route_buffer_loc = os.path.join(ds_gdb, ada_route_buffer)


    deleteAndReplace(ada_service_area, ds_gdb)
    deleteAndReplace(ada_system_merge, ds_gdb)
    deleteAndReplace(ada_route_buffer, ds_gdb)


    # MERGE METROBUS SYSTEM BUFFER WITH LIGHTRAIL ALIGNMENT BUFFER AND 270 FILL IN
    ap.FeatureClassToFeatureClass_conversion(mb_sys_buffer_loc, ds_gdb, ada_route_buffer, 'ADA = 1')
    ap.Merge_management([ada_fill, ada_route_buffer, lightrail_buffer], ada_system_merge)
    ap.AddField_management(ada_system_merge, 'Name', 'TEXT')
    ap.CalculateField_management(ada_system_merge, "Name", "'Metro ADA Service Area'", "PYTHON3")

    # DISSOLVE MERGED LAYERS INTO MetroADAServiceArea
    ap.Dissolve_management(ada_system_merge, ada_service_area, "Name")
    deleteAndReplace(ada_system_merge, ds_gdb)
    log('end of ada creation')

def updateCurrentGDB():
    updateList =[
        "MetroBusRoutes",
        "MetroBusStops",
        "MetroBusStopsByLine",
        "MetroBusRouteBuffer_05",
        "MetroBusRouteBuffer_025",
        "MetroBusRouteBuffer_075",
        "MetroBusSystemBuffer_05",
        "MetroBusSystemBuffer_025",
        "MetroBusSystemBuffer_075",
        "MetroBusRoutes_dir",
        "MetroADAServiceArea"
    ]

    for item in updateList:
        log('********************************************************************************************************')
        log(f'Start of {item} creation in CurrentFiles.gdb')
        log('********************************************************************************************************')
        working = os.path.join(ds_gdb, f"{item}_{sign}_{pattern_file_date}")
        # update_loc = os.path.join(cf_gdb, f"{item}")
        deleteAndReplace(os.path.join(cf_gdb, f"{item}_REGISTERED"), cf_gdb)
        ap.FeatureClassToFeatureClass_conversion(working, cf_gdb, f"{item}_REGISTERED")
        log(f'{item}_REGISTERED replaced in CurrentFile.gdb')
        log(' ')


def updateWebLayers(fc_list, user, password, url, project, enterprise=False):
    # Original source:
    # https://www.esri.com/arcgis-blog/products/analytics/analytics/updating-your-hosted-feature-services-with-arcgis-pro-and-the-arcgis-api-for-python/

    # Start setting variables
    # Path to the APRX file of the map with the layer(s) in it:
    # prjPath = r"C:\Users\gavi6895\Documents\ArcGIS\Projects\METRO-STL-2019\METRO-STL-2019.aprx"
    # 201002

    # Update the following variables to match:
    # [feature_class_name, summary, description, tags]
    # THE FOLLOWING LIST IS THE EXISTING FILES THAT ARE CURRENTLY HOSTED VIA AGOL AND IF YOU ARE GOING TO UPDATE THE
    # THE LIST OF FILES TO ADD MORE YOU NEED TO CREATE A NEW MAP WITH A CORRESPONDING FILE IN AUTOMATEDEXPORTS/CURRENTFILE.GDB


    folder = 'REGISTERED_SERVICES'

    # Set sharing options
    shrOrg = False
    shrEveryone = False
    shrGroups = ""

    log('*****************************************************')
    log(f"Connecting to {url}...")

    gis = GIS(url, user, password)  # connect to what portal you are interested in publishing to using variables user and password

    log(' ')
    log(f"Connected!!!")
    log('*****************************************************')
    log(' ')
    log(' ')

    # End setting variables

    for fc in fc_list:
        # Local paths to create temporary content
        log(f"Start of: {fc['title']}")
        log('*****************************************************')
        log(' ')
        relPath = 'A:\Open Data Admin\AutomationExports'
        log(f'relPath = {relPath}')

        sddraft = os.path.join(relPath, "WebUpdate.sddraft")
        sd = os.path.join(relPath, "WebUpdate.sd")

        # Create a new SDDraft and stage to SD
        log("Creating SD file")
        ap.env.overwriteOutput = True # allow overwrite???
        prj = ap.mp.ArcGISProject(project) # define the arcpro project
        mp = prj.listMaps(fc['title'])[0] # get the first map that matches the feature class then get the first object
        lay = mp.listLayers()[0] # get the first layer from the map object
        hosted_file_name = f"{fc['title']}_REGISTERED" # define the hosted_file_name. This is what it is named on AGOL/DataStore
        ap.mp.CreateWebLayerSDDraft(map_or_layers=lay,
                                    out_sddraft=sddraft,
                                    service_name=hosted_file_name,
                                    server_type='HOSTING_SERVER',
                                    service_type='FEATURE_ACCESS',
                                    folder_name=folder,
                                    overwrite_existing_service=True,
                                    copy_data_to_server=True) # define service definition parameters

        ap.StageService_server(sddraft, sd) # put the service definition parameters in staging

        # Find the SD, update it, publish /w overwrite and set sharing and metadata
        log("Search for original SD on portal ...")
        log(f"Query: {hosted_file_name}")

        updateList =["Service Definition",
                     ""]

        for item in updateList:
            log('')
            log(f'Start of {fc["title"]} {item}')
            log("*******************************")
            log('')
            list = gis.content.search(query=hosted_file_name, item_type=item)

            # scan list of items to make sure they are an exact match to hosted_file_name
            # preform update() and publish() to "Service Definition"
            i = 0
            # cycle through the list that search() brought back to make sure that it is an exact match to hosted_file_name
            while list[i].title != hosted_file_name:
                i += 1

            log('MATCH FOUND!!!')
            log(list[i])
            log(f'item[i].title = {list[i].title}, hosted_file_name = {hosted_file_name}')
            item = list[i]  # define item based on above findings


            if item == 'Service Definition':
                item.update(data=sd)  # use sd to update hosted "Service Definition" file
                log("Overwriting existing feature service ...")
                fs = item.publish(overwrite=True)  # publish "Service Definition"

                if shrOrg or shrEveryone or shrGroups:  # update sharing groups
                    log("Setting sharing options ...")
                    fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)

            log("Updating Metadata...")
            item.update(item_properties={'snippet': fc['summary'],
                                         'tags': fc['tags'],
                                         'description': fc['description']})


        # START OF UPDATE TO VIEWS ON PORTAL

        log("")
        log(f"Start of {fc['view_title']} View Update")
        log("*******************************")
        log("")
        log("Search for view portal ...")
        log(f"Query: {fc['view_title']}, folder: 'REGISTERED VIEWS'")

        list = gis.content.search(query=f"title: '{fc['view_title']}'", item_type='')
        log(list)
        # scan list of items to make sure they are an exact match to hosted_file_name
        # preform update() and publish() to "Service Definition"
        i = 0
        # cycle through the list that search() brought back to make sure that it is an exact match to hosted_file_name
        while list[i].title != fc['view_title']:
            i += 1

        log('MATCH FOUND!!!')
        log(list[i])
        log(f'item[i].title = {list[i].title}, hosted_file_name = {fc["view_title"]}')
        item = list[i]  # define item based on above findings

        item.update(data=sd)  # use sd to update hosted "Service Definition" file
        log("Overwriting existing feature service ...")

        if item == 'Service Definition':
            fs = item.publish(overwrite=True)  # publish "Service Definition"

            if shrOrg or shrEveryone or shrGroups:  # update sharing groups
                log("Setting sharing options ...")
                fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)

        log("Updating Metadata...")
        item.update(item_properties={'snippet': fc['summary'],
                                     'tags': fc['tags'],
                                     'description': fc['description']})

        log(f"Finished updating: {list[i].title} – ID: {list[i].id}")
        log('')
        log('*********************************************')
        log('')


def createLocalFiles():
    routesCreation()
    routeBuffers()
    stopsCreation()
    adaCreation(sign)
    updateCurrentGDB()


clearDataStore()
addCollumns()
createLocalFiles()
updateWebLayers(agol_fc, agol_user, agol_password, agol_url, agolProj)
updateWebLayers(enterprise_fc, enterprise_user, enterprise_password, enterprise_url, enterpriseProj)