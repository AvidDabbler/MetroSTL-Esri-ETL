import os
import arcpy as ap
import pandas as pd

# helpers
from .helpers import deleteFeatureClass

# function to create the routes by dir and routes file in the weekely datastore gdb
# this function takes in the return of the config_options() in the run.py file
def routesCreation(config):
    ap.env.overwriteOutput = True

    csv_dir = config['processed_dir']
    ds_gdb = config['ds_gdb']
    
    # CSV TABLES
    patterns_xy = config['files']['patterns']['xy']
    patterns_name = config['files']['patterns']['name']
    patterns_line = config['files']['patterns']['line']
    ada_table = config["files"]["ada"]

    # FEATURE CLASS NAMES
    routes_dir_line = config['files']['feat_classes']['routes_dir']
    routes_line = config['files']['feat_classes']['routes']
    ada_table_loc = os.path.join(csv_dir, f'{ada_table}.csv')

    # CSV LOCATIONS
    patterns_line_loc = os.path.join(ds_gdb, patterns_line)
    patterns_table = os.path.join(csv_dir, f'{patterns_name}.csv')


    # delete patterns if it has already been run today
    deleteFeatureClass(patterns_xy, ds_gdb)
    # TURN CSV TO POINTS FEATURE CLASS
    ap.management.XYTableToPoint(patterns_table, patterns_xy, "shape_lon", "shape_lat", "", ap.SpatialReference(4326))
    print("Created Points file from CSV file")

    # CHECK FOR FILE AND DELETE IF IT EXISTS
    deleteFeatureClass(patterns_line, ds_gdb)
    ap.PointsToLine_management(patterns_xy,
                               patterns_line,
                               'ShapeID',
                               'SHAPE_PT_SEQUENCE')

    print("Created Line file from Point file")

    # ADD IN PATTERNS GROUP ATTRIBUTES TO PATTERNS LINE
    ap.JoinField_management(patterns_line_loc, 
                            'ShapeID', 
                            patterns_table, 
                            'ShapeID', 
                            ['RouteAbbr', 'DirName', 'LineName', 'PubNum', 'PubName', 'LineNum'])
    print("Added fields to Patterns")

    # GET RID OF METROLINK 
    with ap.da.UpdateCursor(patterns_line_loc, ['ROUTEABBR']) as cursor:
        for row in cursor:
            if row[0] == 3599:
                cursor.deleteRow()

    # START OF ADDING ADA INFORMATION
    ap.AddField_management(patterns_line_loc, "ADA", "SHORT")
    # add in ADAAbbr is the same as RouteAbbr but you cannot add in another field with the same name
    # if it is not in the ada table that means that it is not an ada route
    ap.JoinField_management(patterns_line_loc, 'RouteAbbr', ada_table_loc, 'ADAAbbr', ['ADAAbbr'])

    # COMPARE ROUTE_ABBR IN ADA ROUTES AND PATTERNS_LINE_LOC
    adaCalc = """def ada(adaRoute):
        if adaRoute is None:
            return 0
        else:
            return 1"""

    ap.CalculateField_management(patterns_line_loc, 'ADA', 'ada(!ADAAbbr!)', "PYTHON3", adaCalc)
    ap.DeleteField_management(patterns_line_loc, "ADAAbbr")

    # ROUTES BY DIRECTION CREATION

    deleteFeatureClass(routes_dir_line, ds_gdb)

    # CREATE ROUTE DIR SHAPEFILE
    ap.Dissolve_management(patterns_line, routes_dir_line, ['ROUTEABBR', 'LINENAME', 'PUBNUM', 'LINENUM', 'DIRNAME', 'ADA'])
    print('Created Routes Dir Lines')

    # ROUTES CREATION

    deleteFeatureClass(routes_line, ds_gdb)

    # CREATE ROUTE SHAPEFILE
    ap.Dissolve_management(patterns_line, routes_line, ['ROUTEABBR', 'LINENAME', 'PUBNUM', 'LINENUM', 'ADA'])
    print('Created Routes Lines')


    # DELETE MetroPatterns_XY
    ap.Delete_management(patterns_xy)

# creates the route and system buffers file in the weekly datastore gdb 
# route buffers are just of the route system buffers are the dissolved verion of route buffers
def routeBuffers(config):
    ap.env.overwriteOutput = True

    date = config['date']
    sign = config['sign']
    acs_year = config['acs_year']
    title_vi_gdb = config['title_vi_gdb']

    csv_dir = config['processed_dir']
    ds_gdb = config['ds_gdb']
    
    # CSV TABLES
    patterns_name = config['files']['patterns']['name']
    patterns_table = os.path.join(csv_dir, f'{patterns_name}.csv')

    # FEATURE CLASS NAMES
    routes_dir_line = config['files']['feat_classes']['routes_dir']
    routes_line = config['files']['feat_classes']['routes']
    route_buffer = config['files']['feat_classes']['route_buffer']
    sys_buffer = config['files']['feat_classes']['sys_buffer']

    # MetroBusRoutes_Buffer and MetroBusSystem_Buffer
    buffer_list = [{'dist': '0.75 miles', 'name': '075'},
                   {'dist': '0.5 miles', 'name': '05'},
                   {'dist': '0.25 miles', 'name': '025'}]

    # BUFFERING 0.75, 0.5, 0.25 MILES
    # has subsiquent for loops that run for each of the populations calcualtion as a part of titlevi
    for dist in buffer_list:

        # ROUTE BUFFER
        routes_buffer = f'{route_buffer}{dist["name"]}_{sign}_{date}'
        routes_buffer_loc = os.path.join(ds_gdb, routes_buffer)

        # DELETE DUPLICATE ROUTE FILE
        # deleteFeatureClass(routes_buffer, ds_gdb)

        ap.Buffer_analysis(routes_line, routes_buffer,
                           dist['dist'], "FULL", "ROUND", "NONE")
        print('Routes Buffered')

        # PATTERNS GROUP
        patterns_pd = pd.read_csv(patterns_table).groupby(
            ['RouteAbbr', 'LineName', 'PubNum', 'LineNum', 'ShapeID', 'DirName']).mean()
        patterns_pd.drop(['shape_lat', 'shape_lon', 'shape_pt_sequence'], axis=1)
        print('Unique Routes table created')

        # SYSTEM BUFFER (dissolves the route buffers)
        mb_sys_buffer = f'{sys_buffer}{dist["name"]}_{sign}_{date}'
        mb_sys_buffer_loc = os.path.join(ds_gdb, mb_sys_buffer)

        ap.Dissolve_management(routes_buffer, mb_sys_buffer)
        print('System Buffered')
        ap.AddField_management(mb_sys_buffer, 'type', 'TEXT')
        ap.CalculateField_management(mb_sys_buffer, 'type', '"system"')

    
        # TITLE VI POPULATION ANALYSIS

        # TITLE VI ANALYSIS FOR STANDARD FILES
        # ACS INPUT, TOTAL POPULATION FIELD, DENSITY POPULATION COUNT
        # takes the data from the titlevi fields and calculates the population 
        # density for specific groups in order to get the total population of each group
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

            print('')
            print('-------------------------')
            print(f'Start of {acs_out} Creation')
            print('-------------------------')
            print('')

            ap.Clip_analysis(acs_in, mb_sys_buffer, acs_out)
            ap.AddFields_management(acs_out,
                                    [[acs['field'], 'DOUBLE'],
                                     ['ClipSqMiles', 'DOUBLE']])
            print(f'Added fields to {acs_out} ')
            ap.CalculateFields_management(acs_out, 'PYTHON3', [['ClipSqMiles', "!shape.area@squaremiles!"],
                                                               [acs['field'], f'{acs["calc"]} * !ClipSqMiles!']])
            print(f'Calculated fields for {acs_out}')

            # dissolve out file name
            acs_out_diss = f'{acs_out}_dissolve'


            ap.Dissolve_management(acs_out, acs_out_diss, '', [[acs['field'], 'SUM']])
            ap.AddField_management(acs_out_diss, 'type', 'TEXT')
            ap.CalculateField_management(acs_out_diss, 'type', '"system"')
            ap.JoinField_management(mb_sys_buffer, 'type', acs_out_diss, 'type', f'SUM_{acs["field"]}')
            ap.AddField_management(mb_sys_buffer, acs['field'], 'DOUBLE')
            ap.CalculateField_management(mb_sys_buffer, acs["field"], f'!SUM_{acs["field"]}!')
            ap.DeleteField_management(mb_sys_buffer, f'SUM_{acs["field"]}')

            # DELETE EXTRA FIELDS
            delete_list = [acs_out, acs_out_diss]
            for d in delete_list:
                ap.Delete_management(d)