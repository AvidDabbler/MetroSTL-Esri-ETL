import os
import arcpy as ap
import pandas as pd

# helpers
from .helpers import deleteFeatureClass


# this function is used to create the eam stops that are used by the eam team
# this function will create a eam stops file in the weekly and current gdb that
# has information about the 1000 and 1000 km grid
def eamStopCreation(config):
    ap.env.overwriteOutput = True

    ds_gdb = config['ds_gdb'] 
    cf_gdb = config['cf_gdb'] 
    
    # FEATURE CLASS NAMES
    bus_stops = config['files']['feat_classes']['stops']
    eam_stops = config['files']['feat_classes']['eam_stops']
    eam_stops_1000 = config['files']['feat_classes']['eam_stops_1000']
    grid1000 = config['files']['registered']['grid1000']
    grid10000 = config['files']['registered']['grid10000']

    # join the bus stops file to the 1000 grid
    ap.analysis.SpatialJoin(
        os.path.join(ds_gdb, bus_stops),
        os.path.join(cf_gdb, grid1000),
        os.path.join(ds_gdb, eam_stops_1000),
        "JOIN_ONE_TO_ONE", "KEEP_ALL", 
        match_option="WITHIN")

    # join the bus stops file to the 10000 grid
    ap.analysis.SpatialJoin(
        os.path.join(ds_gdb, eam_stops_1000),
        os.path.join(cf_gdb, grid10000),
        os.path.join(ds_gdb, eam_stops),
        "JOIN_ONE_TO_ONE", "KEEP_ALL", 
        match_option="WITHIN",)
    