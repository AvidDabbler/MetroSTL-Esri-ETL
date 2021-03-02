import os
import arcpy as ap

# helpers
from .helpers import * 


def stopsCreation(config):
    ap.env.overwriteOutput = True

    date = config.date
    sign = config.sign
    acs_year = config.acs_year
    title_vi_gdb = config.title_vi_gdb

    csv_dir = config.processed_dir
    ds_gdb = config.ds_gdb
    cf_gdb = config.cf_gdb
    
    # CSV TABLES
    stops_name = config.files.stops
    stopsbyline_name = config.files.stopsbyline

    # FEATURE CLASS NAMES
    stops_output = config.feat_classes.stops
    stopsbyline_output = config.feat_classes.stopsbyline


    # CSV LOCATIONS    
    stops_table = os.path.join(csv_dir, f'{stops_name}.csv')
    stopsbyline_table = os.path.join(csv_dir, f'{stopsbyline_name}.csv')

    # deleteFeatureClass(stops_output, ds_gdb)
    # deleteFeatureClass(stopsbyline_output, ds_gdb)

    ap.management.XYTableToPoint(stops_table, stops_output, 'GPS_Lon', 'GPS_Lat', '', ap.SpatialReference(4326))
    print('Stops Created')
    ap.management.XYTableToPoint(stopsbyline_table, stopsbyline_output,'GPS_LON', 'GPS_LAT', '', ap.SpatialReference(4326))
    print('Stops By Line Created')

    county = os.path.join(cf_gdb, 'State_County')

    stops_state_county = os.path.join(ds_gdb, 'stopsStateCounty')

    # deleteFeatureClass(stops_state_county, cf_gdb)


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

    print("done")

def ghosttopsCreation(config):
    ap.env.overwriteOutput = True

    date = config.date
    sign = config.sign
    
    csv_dir = config.processed_dir
    ds_gdb = config.ds_gdb
    cf_gdb = config.cf_gdb
    
    # CSV TABLES
    ghoststops_name = config.files.ghoststops

    # FEATURE CLASS NAMES
    ghoststops_output = config.feat_classes.ghoststops

    # CSV LOCATIONS    
    ghoststops_table = os.path.join(csv_dir, f'{ghoststops_name}.csv')
    
    # deleteFeatureClass(file_name, ds_gdb)
    ap.management.XYTableToPoint(ghoststops_table, ghoststops_output,'GPS_LON', 'GPS_LAT', '', ap.SpatialReference(4326))
    print('Stops By Line Created')
    county = os.path.join(cf_gdb, 'State_County')
    stops_state_county = os.path.join(ds_gdb, 'stopsStateCounty')

    # deleteFeatureClass(stops_state_county, cf_gdb)


    # STOPS COUNTY SPATIAL JOIN
    ap.SpatialJoin_analysis(ghoststops_output, county, stops_state_county)


    # STOPS COUNTY CALUCLATION

    ap.AddField_management(ghoststops_output, "CountyName", "TEXT")
    ap.JoinField_management(ghoststops_output, "StopID", stops_state_county, "StopID", ["GEOID", "NAME"])
    ap.CalculateField_management(ghoststops_output, f"CountyCode", '!GEOID!', "PYTHON3")
    ap.CalculateField_management(ghoststops_output, f"CountyName", '!NAME!', "PYTHON3")
    ap.DeleteField_management(ghoststops_output, "GEOID")
    ap.DeleteField_management(ghoststops_output, "NAME")

    print("done")
