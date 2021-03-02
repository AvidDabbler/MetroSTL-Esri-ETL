import os
import csv
import arcpy as ap
from arcgis.gis import GIS

##### HELPERS ####
from .gis_lib.helpers import * 

#### LOCAL ####
from .gis_lib.routes import routesCreation, routeBuffers
from .gis_lib.stops import stopsCreation, ghosttopsCreation
from .gis_lib.eam import eamStopCreation

#### DATA ####
from .features import features 

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



d_agol_user = os.getenv('AGOL_USER')
d_agol_password = os.getenv('AGOL_PASSWORD')

d_enterprise_user =os.getenv('ENTERP_USER')
d_enterprise_password = os.getenv('ENTERP_PASSWORD')


title_vi = r"\\metroas08\arcgisdatastore\Open Data Admin\TitleVI\Final_17.gdb" # \\metroas08\arcgisdatastore\Open Data Admin\TitleVI\Final_17.gdb  or r'A:\Open Data Admin\TitleVI\Final_17.gdb
AutomationExports = r'\\metroas08\arcgisdatastore\Open Data Admin\AutomationExports' # \\metroas08\arcgisdatastore\Open Data Admin\AutomationExports or r'A:\Open Data Admin\AutomationExports
sql_exports = r'\\metroas08\arcgisdatastore\Open Data Admin\SQL_Exports' # r'W:\Transfer\wkjenkins' or r'A:\Open Data Admin\SQL_Exports\SQL_Exports'

exports_dir = input(rf"Where are the data files? (Defaults to default {sql_exports}) ") or sql_exports
title_vi_gdb = input(rf'Where is the the TitleVI Geodatabase (Defalults to {title_vi} : ') or title_vi

os.chdir(sql_exports)
sched_date = date('METRO_PATTERNS*')

# WORKING DIRECTORIES
ds_gdb = os.path.join(AutomationExports, f"DataStore_{sched_date}.gdb")
cf_gdb = os.path.join(AutomationExports, "CurrentFiles.gdb")

ap.env.workspace = os.path.join(AutomationExports, ds_gdb)

print('')
print('******************************************************************************************************************')
print(f"Waiting for ArcGIS online credentials...")
agol_user = input(f"USERNAME (Default = {d_agol_user}): ") or d_agol_user
agol_password = input("PASSWORD: ") or d_agol_password
agol_url = 'https://www.arcgis.com/'
agolProj = r"\\metroas08\arcgisdatastore\Open Data Admin\Online_Content.aprx"  # A:\ is the data store folder on \\metroas08\


print(f"Waiting for Enterprise credentials...")
enterprise_user = input(f"USERNAME (Default = {d_enterprise_user}): ") or d_enterprise_user
enterprise_password = input("PASSWORD: ") or d_enterprise_password
enterprise_url = "https://maps.metrostlouis.org/arcgis/home/"
enterpriseProj = r"A:\Open Data Admin\Enterprise_Content.aprx"  # A:\ is the data store folder on \\metroas08\


title_vi_gdb = input(rf'Where is the the TitleVI Geodatabase (Defalults to {title_vi} : ') or title_vi

feature_classes = features(sched_date)

def featureList(fc_list, portal):
    features = []

    print('')
    print("*******************************************************************************************************************")
    print(f'The following have been added to the {portal} Feature Class List')
    print("*******************************************************************************************************************")
    print('')

    for fc in fc_list:
        if fc[portal] is True:
            list.append(fc)
            print(f"- {fc['title']}")

    print('')
    print('--- END OF LIST ---')
    print('')


    if portal == 'agol':
        profile = {
            "portal": 'https://www.arcgis.com/',
            "user": os.getenv('AGOL_USER'),
            "password": os.getenv('AGOL_PASSWORD'),
            "project": os.getenv('AGOL_PROJECT'),
        }
    elif portal == 'enterprise':
        profile = {
            "portal": os.getenv('ENTERP_PORTAL'),
            "user": os.getenv('ENTERP_USER'),
            "password": os.getenv('ENTERP_PASSWORD'),
            "project": os.getenv('ENTERP_PROJECT'),
        }
    profile["features"] = features
    return profile



def files_spec(date):
    return [
        {'org_csv': f'METROBUS-STOPBYLINE_EXTRACTION-WITH-DISTANCE{date}.csv', 
        # 'table': stopsbyline_table, 
        'columns': ['Seq', 'SignID', 'StopID', 'StopAbbr', 'StopName', 'OnSt', 'AtSt', 'StopPos', 'PrefTrans', 'Bench', 'Shelter', 'Transfer', 'ADA', 'PubWay', 'Node', 'LineName', 'RouteCode', 'Dir', 'CountyCode', 'Juris', 'GPS_Lon', 'GPS_Lat', 'Dist', '']},
        {'org_csv': f'METROBUS-STOP-EXTRACTION{date}', 
        # 'table': stops_table, 
        'columns': ['SignID', 'StopID', 'StopAbbr', 'StopName', 'OnSt', 'AtSt', 'Lines', 'Routes', 'StopPos', 'PrefTrans', 'Bench', 'Shelter', 'Transfer', 'ADA', 'PubWay', 'CountyCode', 'Juris','GPS_Lon', 'GPS_Lat', '']},
        {'org_csv': f'METRO_PATTERNS{date}', 
        # 'table': patterns_table, 
        'columns': ['SignID', 'ShapeID', 'RouteAbbr', 'DirName', 'LineName','PubNum', 'LineNum', 'shape_lat', 'shape_lon', 'shape_pt_sequence', '']},
        {'org_csv': f"ADA-ROUTES-LIST.csv", 
        # 'table': ada_table, 
        'columns': ['type', 'ADAAbbr', '']},
        {'org_csv': f'METROBUS-GHOSTSTOPS{date}', 
        # 'table': ghoststops_table, 
        'columns': ['SignID','StopID','StopAbbr','StopName','OnSt','AtSt','StopPos','PrefTrans','Bench','Shelter','Transfer','ADA','PubWay','CountyCode','Juris','GPS_Lon','GPS_Lat','']}
        ]
        # will be outdated after AirFlow. Updated SQL Scripts 
        # will allow for us to use specified column headers

def addCollumns(sql_exports, spec, folder_name):
    # add in missing columns from
    for item in spec:
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
        deleteFeatureClass(item['org_csv'], sql_exports)

        with open(new_csv_loc, 'w', newline='') as f:
            # Overwrite the old file with the modified rows
            writer = csv.writer(f)
            writer.writerows(all_rows)
    # returns the full path of the new csv directory
    return {"org_dir": sql_exports, "processed_dir": os.path.join(sql_exports, folder_name)}

def adaCreation(s):
    log('start of ada creation')
    sign = s
    mb_sys_buffer = f'MetroBusRouteBuffer_075_{sign}_{pattern_file_date}'
    mb_sys_buffer_loc = os.path.join(ds_gdb, mb_sys_buffer)

    # SETTING UP FOR MetroADAServiceArea
    ada_fill = os.path.join(cf_gdb, 'ADA_Fill')
    lightrail_buffer = os.path.join(cf_gdb, 'Lightrail_buffer')
    ada_system_merge = os.path.join(ds_gdb, f'MetroADASysMerge_{sign}_{pattern_file_date}')
    ada_service_area = os.path.join(ds_gdb, f'MetroADAServiceArea_{sign}_{pattern_file_date}')
    ada_route_buffer = f"ADARouteBuffer_{sign}_{pattern_file_date}"
    ada_route_buffer_loc = os.path.join(ds_gdb, ada_route_buffer)


    deleteFeatureClass(ada_service_area, ds_gdb)
    deleteFeatureClass(ada_system_merge, ds_gdb)
    deleteFeatureClass(ada_route_buffer, ds_gdb)


    # MERGE METROBUS SYSTEM BUFFER WITH LIGHTRAIL ALIGNMENT BUFFER AND 270 FILL IN
    ap.FeatureClassToFeatureClass_conversion(mb_sys_buffer_loc, ds_gdb, ada_route_buffer, 'ADA = 1')
    ap.Merge_management([ada_fill, ada_route_buffer, lightrail_buffer], ada_system_merge)
    ap.AddField_management(ada_system_merge, 'Name', 'TEXT')
    ap.CalculateField_management(ada_system_merge, "Name", "'Metro ADA Service Area'", "PYTHON3")

    # DISSOLVE MERGED LAYERS INTO MetroADAServiceArea
    ap.Dissolve_management(ada_system_merge, ada_service_area, "Name")
    deleteFeatureClass(ada_system_merge, ds_gdb)
    log('end of ada creation')

def updateCurrentGDB():
    updateList =[
        "MetroBusRoutes",
        "MetroBusStops",
        # "MetroBusGhostStops",
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
        deleteFeatureClass(os.path.join(cf_gdb, f"{item}_REGISTERED"), cf_gdb)
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
            item = list[i] # define item based on above findings

            item.update(data=sd) # use sd to update hosted "Service Definition" file
            log("Overwriting existing feature service ...")


            if item == 'Service Definition':
                fs = item.publish(overwrite=True)  # publish "Service Definition"

                if shrOrg or shrEveryone or shrGroups: # update sharing groups
                    log("Setting sharing options ...")
                    fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)

            log("Updating Metadata...")
            item.update(item_properties={'snippet': fc['summary'],
                                         'tags': fc['tags'],
                                         'description': fc['description']})

            try:
                item.publish(overwrite=True)
                print('Published Service Definition!!!')
            except:
                print('Could Not Publish!!!!')



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
        item = list[i] # define item based on above findings

        item.update(data=sd) # use sd to update hosted "Service Definition" file
        log("Overwriting existing feature service ...")


        if item == 'Service Definition':
            fs = item.publish(overwrite=True)  # publish "Service Definition"

            if shrOrg or shrEveryone or shrGroups: # update sharing groups
                log("Setting sharing options ...")
                fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)

        log("Updating Metadata...")
        item.update(item_properties={'snippet': fc['summary'],
                                     'tags': fc['tags'],
                                     'description': fc['description']})
        try:
            item.publish(overwrite=True)
        except:
            print('Could Not Publish!!!!')

        log(f"Finished updating: {list[i].title} – ID: {list[i].id}")
        log('')
        log('*********************************************')
        log('')

def config_options(files, csv_dir, sign, date, acs_year, ds_gdb, cf_gdb, title_vi_gdb):
    ap.env.workspace = os.path.join(AutomationExports, ds_gdb)

    return {
        "sign": sign,
        "csv_dir": csv_dir,
        "date": date,
        "acs_year": acs_year,
        "title_vi_gdb": title_vi_gdb,
        "files": files,
        "org_dir": csv_dir['org_dir'],
        "processed_dir": csv_dir['processed_dir'],
        "ds_gdb": ds_gdb, 
        "cf_gdb": cf_gdb,
        "files": {
            "ada": f'ADA-ROUTES-LIST',
            "ghoststops": f'METROBUS-GHOSTSTOPS{date}',
            "patterns": {
                "xy": f'METRO_PATTERNS_XY_{date}',
                "name": f'METRO_PATTERNS{date}',
                "line": f'METRO_PATTERNS{date}_{sign}',
            },
            "stops": f'METROBUS-STOP-EXTRACTION{date}',
            "stops_by_line": f'METROBUS-STOPBYLINE_EXTRACTION-WITH-DISTANCE{date}',
        "feat_classes":{
            "ghoststops": f'MetroBusGhostStops_{sign}_{date}',
            "routes": f'MetroBusRoutes_{sign}_{date}',
            "route_buffer": "MetroBusRouteBuffer_",
            "routes_dir": f'MetroBusRoutes_dir_{sign}_{date}',
            "stops": f'MetroBusStops_{sign}_{date}',
            "sys_buffer": "MetroBusSystemBuffer_",
        },
        "registered": {
            "stops": "MetroBusStops_REGISTERED",
            "grid1000": "MGRS_Grid_1000",
            "eam_stops_1000": "EAMMetroBusStops_1000",
            "grid1000": "MGRS_Grid_1000",
            "grid10000": "MGRS_Grid_10000",
            "eam_stops": "EAMMetroBusStops_REGISTERED",
            
        }

        }
    }

def createLocalFiles(config):
    routesCreation(config)
    routeBuffers(config)
    stopsCreation(config)
    ghosttopsCreation(config)
    adaCreation(config)
    updateCurrentGDB(config)


# admin functions
# DEFINE FEATURES AN FIELD FOR EACH PORTAL
agol_fc = featureList(feature_classes, 'agol')
enterprise_fc = featureList(feature_classes, 'enterprise')
csvs = files_spec(date)
acs_year = title_vi_gdb[-6:-4]
sched_sign = currentSign(os.path.join(sql_exports, f'METROBUS-STOP-EXTRACTION{sched_date}.csv'))

clearDataStore(AutomationExports, date)

# add headers to dba csv exports
csv_dir = addCollumns(sql_exports, csvs, f'{date}')

config = config_options(csvs, csv_dir, sched_sign, date, acs_year, ds_gdb, cf_gdb)

createLocalFiles(config)
updateWebLayers(agol_fc, agol_user, agol_password, agol_url, agolProj)
updateWebLayers(enterprise_fc, enterprise_user, enterprise_password, enterprise_url, enterpriseProj)