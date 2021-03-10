import os
import csv
import arcpy as ap
from arcgis.gis import GIS
from dotenv import load_dotenv

##### CONFIG #####
from config import local_config, portal_config, config_options

##### HELPERS #####
from gis_lib.helpers import * 

##### LOCAL #####
from gis_lib.routes import routesCreation, routeBuffers
from gis_lib.stops import stopsCreation, ghosttopsCreation
from gis_lib.eam import eamStopCreation
from gis_lib.ada import adaCreation
from gis_lib.local import csv_locs, add_columns, update_current
from gis_lib.portal import updatePortalLayers

##### DATA #####
from features import features 
 

# TODO: add in portal ids for feature classes on each portal and cut out project specific bloat
# TODO: update date to be that monday's date to avoid confusion
# TODO: update_current needs to list the ones in the working dir and determine the matching 
# feature that is is associated with and then update that

def run():
    # GET THE LOCAL PROJECT ENV VARIABLES
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)    # Function chaining all of the processing of feature classes into one 
    
    #  change cwd
    os.chdir(os.environ['SQL_EXPORTS'])

    # turn local variables into object
    local = local_config()
    ap.env.workspace = os.path.join(local['Automation_Exports'], local['ds_gdb'])
    
    # get feature class names by feeding in date
    feature_classes = features(local['sched_date'])

    # build agol and enterprise profiles
    agol_config = portal_config(feature_classes, 'agol')
    enterprise_config = portal_config(feature_classes, 'enterprise')
    
    # get the location of all of the csv's ---> to be depricated with airflow
    csvs = csv_locs(local['sched_date'])

    printList(csvs, "org_csv")

    # delete the working gdb if it has already been run this week
    # clearDataStore(local['Automation_Exports'], local['sched_date'])

    # add headers to dba csv exports
    csv_dir = add_columns(local['Sql_Exports'], csvs, local['sched_date'])
    
    # define config object
    config = config_options(csvs, csv_dir, local)

    # run the model with all of the specified variable objects and profiles

    # function that finishes by updating the current gdb
    def createLocalFiles(config, csvs):
        print(' ')
        print('-------------------------------------')
        print('Start of Local GIS file Creation')
        print('-------------------------------------')
        print(' ')
        # itterate through csvs to only run processes that have been updated
        # for file in csvs:
        #     if file['type'] == 'stopsbyline':
        #         stopsCreation(config)
        #     elif file['type'] == 'patterns':
        #         routesCreation(config)
        #         routeBuffers(config)
        #         adaCreation(config)
        #     elif file['type'] == 'eamstops':
        #         eamStopCreation(config)
        #     elif file['type'] == 'ghoststops':
        #         ghosttopsCreation(config)
        eamStopCreation(config)
        # update_current(config)

    createLocalFiles(config, csvs)
    # updatePortalLayers(agol_config)
    # updatePortalLayers(enterprise_config)

run()

# DEFAULT DIRECTORIES

# def __init__():
#     title_vi = r"\\metroas08\arcgisdatastore\Open Data Admin\TitleVI\Final_17.gdb" # \\metroas08\arcgisdatastore\Open Data Admin\TitleVI\Final_17.gdb  or r'A:\Open Data Admin\TitleVI\Final_17.gdb
#     AutomationExports = r'\\metroas08\arcgisdatastore\Open Data Admin\AutomationExports' # \\metroas08\arcgisdatastore\Open Data Admin\AutomationExports or r'A:\Open Data Admin\AutomationExports
#     sql_exports = r'\\metroas08\arcgisdatastore\Open Data Admin\SQL_Exports' # r'W:\Transfer\wkjenkins' or r'A:\Open Data Admin\SQL_Exports\SQL_Exports'

#     exports_dir = input(rf"Where are the data files? (Defaults to default {sql_exports}) ") or sql_exports
#     title_vi_gdb = input(rf'Where is the the TitleVI Geodatabase (Defalults to {title_vi} : ') or title_vi

#     # WORKING DIRECTORIES
#     ds_gdb = os.path.join(AutomationExports, f"DataStore_{pattern_file_date}.gdb")
#     cf_gdb = os.path.join(AutomationExports, "CurrentFiles.gdb")

#     os.chdir(sql_exports)

#     pattern_date = date('METRO_PATTERNS*')

#     return {
#         "date": pattern_date,
#         "date_formatted": f'{pattern_date[2:4]}/{pattern_date[4:7]}/{pattern_date[:2]}',
#         "sign": currentSign(os.path.join(sql_exports, f'METROBUS-STOP-EXTRACTION{pattern_date}.csv')),
#         "acs_year": title_vi_gdb[-6:-4]

#     }




# PATTERN VARIABLES
# patterns_name = f'METRO_PATTERNS{pattern_file_date}'
# patterns_csv = os.path.join(sql_exports, f'METRO_PATTERNS{pattern_file_date}.csv')
# patterns_table = os.path.join(sql_exports, f'h_{patterns_name}.csv')


# STOPS VARIABLES
# stops_input = f'METROBUS-STOP-EXTRACTION{stops_date}'
# stops_input_loc = os.path.join(sql_exports, f'{stops_input}.csv')
# stops_table = os.path.join(sql_exports, f'h_{stops_input}.csv')


# STOPS BY LINE VARIABLES
# stopsbyline_input = f'METROBUS-STOPBYLINE_EXTRACTION-WITH-DISTANCE{stops_by_line_date}'
# stopsbyline_input_loc = os.path.join(sql_exports, f'{stopsbyline_input}.csv')
# stopsbyline_table = os.path.join(sql_exports, f'h_{stopsbyline_input}.csv')



# acs_year = title_vi_gdb[-6:-4]



# PATTERNS POINTS VARIABLES
# patterns_xy = os.path.join(, f'{patterns_name}_XY_{pattern_file_date}')
# patterns_xy_loc = os.path.join(ds_gdb, patterns_xy)

# PATTERNS LINE VARIABLES
# patterns_line = f'{patterns_name}_{sign}'
# patterns_line_loc = os.path.join(ds_gdb, patterns_line)

# PATTERNS ATTRIBUTE TABLES
# patterns_group = f'{patterns_name}_group_{sign}_{pattern_file_date}'

# STOPS VARIABLES
# stops_output = f'MetroBusStops_{sign}_{stops_date}'
# stops_output_loc = os.path.join(ds_gdb, stops_output)

# STOPS VARIABLES
# stopsbyline_input = f'METROBUS-STOPBYLINE_EXTRACTION-WITH-DISTANCE{stops_by_line_date}'
# stopsbyline_input_loc = os.path.join(sql_exports, f'{stopsbyline_input}.csv')

# STOPS BY LINE VARIABLES
# stopsbyline_output = f'MetroBusStopsByLine_{sign}_{stops_by_line_date}'
# stopsbyline_output_loc = os.path.join(ds_gdb, stopsbyline_output)

# GHOST STOPS VARIABLES
# ghoststops_input = f'METROBUS-GHOSTSTOPS{stops_by_line_date}'
# ghoststops_input_loc = os.path.join(sql_exports, f'{ghoststops_input}.csv')

# GHOST STOPS BY LINE VARIABLES
# ghoststops_output = f'MetroBusGhostStops_{sign}_{stops_by_line_date}'
# ghoststops_output_loc = os.path.join(ds_gdb, ghoststops_output)
# ghoststops_table = os.path.join(sql_exports, f'h_{ghoststops_input}.csv')


# ROUTES VARIABLES
# routes_dir_line = f'MetroBusRoutes_dir_{sign}_{pattern_file_date}'
# routes_dir_loc = os.path.join(ds_gdb, routes_dir_line)
# routes_line = f'MetroBusRoutes_{sign}_{pattern_file_date}'
# routes_loc = os.path.join(ds_gdb, routes_line)
# routes_csv = f'Routes_{pattern_file_date}.csv'
# routes_csv_loc = os.path.join(AutomationExports, f'exports\{routes_csv}')

# PATTERN VARIABLES
# ada_csv_loc = os.path.join(AutomationExports, f"ADA-ROUTES-LIST.csv") #
# ada_name = f'ADA-ROUTES-LIST'
# ada_csv_loc = os.path.join(sql_exports, f"{ada_name}.csv")
# ada_table = os.path.join(sql_exports, f'h_{ada_name}.csv')

# def clearLog(date):
#     # CLEAR OUT THE LOG FILE (FOR IF YOU ARE RUNNING MULITPLE TIMES A DAY)
#     if os.path.exists(os.path.join(os.getcwd(), rf'log_{date}.txt')):
#         os.remove(os.path.join(os.getcwd(), rf'log_{date}.txt'))

# def log(statement):
#     file = os.path.join(AutomationExports, rf'log_{pattern_file_date}.txt')
#     if not os.path.exists(file):
#         open(file, 'a').close()

#     print_log = open(file, 'a+')  # append statement to the end of the file
#     print_log.write(f'\n{statement}')
#     print_log.close()
#     print(statement)



# d_agol_user = os.getenv('AGOL_USER')
# d_agol_password = os.getenv('AGOL_PASSWORD')

# d_enterprise_user =os.getenv('ENTERP_USER')
# d_enterprise_password = os.getenv('ENTERP_PASSWORD')


# title_vi = r"\\metroas08\arcgisdatastore\Open Data Admin\TitleVI\Final_17.gdb" # \\metroas08\arcgisdatastore\Open Data Admin\TitleVI\Final_17.gdb  or r'A:\Open Data Admin\TitleVI\Final_17.gdb
# AutomationExports = r'\\metroas08\arcgisdatastore\Open Data Admin\AutomationExports' # \\metroas08\arcgisdatastore\Open Data Admin\AutomationExports or r'A:\Open Data Admin\AutomationExports
# sql_exports = r'\\metroas08\arcgisdatastore\Open Data Admin\SQL_Exports' # r'W:\Transfer\wkjenkins' or r'A:\Open Data Admin\SQL_Exports\SQL_Exports'

# exports_dir = input(rf"Where are the data files? (Defaults to default {sql_exports}) ") or sql_exports
# title_vi_gdb = input(rf'Where is the the TitleVI Geodatabase (Defalults to {title_vi} : ') or title_vi

# sched_date = date('METRO_PATTERNS*')

# WORKING DIRECTORIES
# ds_gdb = os.path.join(AutomationExports, f"DataStore_{sched_date}.gdb")
# cf_gdb = os.path.join(AutomationExports, "CurrentFiles.gdb")


# print('')
# print('******************************************************************************************************************')
# print(f"Waiting for ArcGIS online credentials...")
# agol_user = input(f"USERNAME (Default = {d_agol_user}): ") or d_agol_user
# agol_password = input("PASSWORD: ") or d_agol_password
# agol_url = 'https://www.arcgis.com/'
# agolProj = r"\\metroas08\arcgisdatastore\Open Data Admin\Online_Content.aprx"  # A:\ is the data store folder on \\metroas08\


# print(f"Waiting for Enterprise credentials...")
# enterprise_user = input(f"USERNAME (Default = {d_enterprise_user}): ") or d_enterprise_user
# enterprise_password = input("PASSWORD: ") or d_enterprise_password
# enterprise_url = "https://maps.metrostlouis.org/arcgis/home/"
# enterpriseProj = r"A:\Open Data Admin\Enterprise_Content.aprx"  # A:\ is the data store folder on \\metroas08\


# title_vi_gdb = input(rf'Where is the the TitleVI Geodatabase (Defalults to {title_vi} : ') or title_vi


# sched_sign = currentSign(os.path.join(local.Sql_Exports, f'METROBUS-STOP-EXTRACTION{sched_date}.csv'))

# config = config_options(csvs, csv_dir, local.sign, local.sched_date, local.ACS_Year, local.ds_gdb, local.cf_gdb)

# updateWebLayers(agol_fc, agol_user, agol_password, agol_url, agolProj)

# updateWebLayers(enterprise_fc, enterprise_user, enterprise_password, enterprise_url, enterpriseProj)
