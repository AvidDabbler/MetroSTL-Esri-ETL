import os
import arcpy as ap
import pandas as pd

# helpers
from .helpers import deleteFeatureClass



def eamStopCreation(config):
    ap.env.overwriteOutput = True

    cf_gdb = config['cf_gdb'] 
    # FEATURE CLASS NAMES
    bus_stops = config['registered']['stops']
    eam_stops = config['registered']['eam_stops']
    eam_stops_1000 = config['registered']['eam_stops_1000']
    grid1000 = config['registered']['grid1000']
    grid10000 = config['registered']['grid10000']

    deleteFeatureClass('EAMMetroBusStops_REGISTERED', 'A:\Open Data Admin\AutomationExports\CurrentFiles.gdb')
    deleteFeatureClass('EAMMetroBusStops_1000', 'A:\Open Data Admin\AutomationExports\CurrentFiles.gdb')

    ap.analysis.SpatialJoin(
        os.path.join(cf_gdb, bus_stops),
        os.path.join(cf_gdb, grid1000),
        os.path.join(cf_gdb, eam_stops_1000),
        "JOIN_ONE_TO_ONE", "KEEP_ALL", 
        # r'SignID "SignID" true true false 4 Long 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,SignID,-1,-1;StopID "StopID" true true false 4 Long 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,StopID,-1,-1;StopAbbr "StopAbbr" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,StopAbbr,0,5000;StopName "StopName" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,StopName,0,5000;OnSt "OnSt" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,OnSt,0,5000;AtSt "AtSt" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,AtSt,0,5000;Lines "Lines" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,Lines,0,5000;Routes "Routes" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,Routes,0,5000;StopPos "StopPos" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,StopPos,0,5000;PrefTrans "PrefTrans" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,PrefTrans,0,5000;Bench "Bench" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,Bench,0,5000;Shelter "Shelter" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,Shelter,0,5000;Transfer "Transfer" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,Transfer,0,5000;ADA "ADA" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,ADA,0,5000;PubWay "PubWay" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,PubWay,0,5000;CountyCode "CountyCode" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,CountyCode,0,5000;Juris "Juris" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,Juris,0,5000;CountyName "CountyName" true true false 255 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MetroBusStops_REGISTERED,CountyName,0,255;Grid1000 "Grid1000" true true false 255 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MGRS_Grid_1000,Grid,0,255;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MGRS_Grid_1000,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MGRS_Grid_1000,Shape_Area,-1,-1', 
        match_option="WITHIN")

    ap.analysis.SpatialJoin(
        os.path.join(cf_gdb, eam_stops_1000),
        os.path.join(cf_gdb, grid10000),
        os.path.join(cf_gdb, eam_stops),
        "JOIN_ONE_TO_ONE", "KEEP_ALL", 
        # r'SignID "SignID" true true false 4 Long 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,SignID,-1,-1;StopID "StopID" true true false 4 Long 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,StopID,-1,-1;StopAbbr "StopAbbr" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,StopAbbr,0,5000;StopName "StopName" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,StopName,0,5000;OnSt "OnSt" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,OnSt,0,5000;AtSt "AtSt" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,AtSt,0,5000;Lines "Lines" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,Lines,0,5000;Routes "Routes" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,Routes,0,5000;StopPos "StopPos" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,StopPos,0,5000;PrefTrans "PrefTrans" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,PrefTrans,0,5000;Bench "Bench" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,Bench,0,5000;Shelter "Shelter" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,Shelter,0,5000;Transfer "Transfer" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,Transfer,0,5000;ADA "ADA" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,ADA,0,5000;PubWay "PubWay" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,PubWay,0,5000;CountyCode "CountyCode" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,CountyCode,0,5000;Juris "Juris" true true false 5000 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,Juris,0,5000;CountyName "CountyName" true true false 255 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\EAMMetroBusStops_1000,CountyName,0,255;Grid1000 "Grid1000" true true false 255 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MGRS_Grid_1000,Grid1000,0,255;Grid10000 "Grid10000" true true false 255 Text 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MGRS_Grid_10000,Grid,0,255;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MGRS_Grid_10000,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,A:\Open Data Admin\AutomationExports\CurrentFiles.gdb\MGRS_Grid_10000,Shape_Area,-1,-1', 
        match_option="WITHIN",)
    ap.Delete_management(os.path.join(cf_gdb, eam_stops_1000))