import os
import arcpy as ap
import glob

from gis_lib import *


# TODO: specify portal ids for feature classes

def local_config():
    
    def local_date(text):
        for file in glob.glob(text):
            dates = []
            dates.append(int(file[-10:-4]))
        date = str(max(dates))
        print(f'{text[:-1]} Date: {date}')
        return date

    sched_date = local_date('METRO_PATTERNS*')
    Automation_Exports = os.getenv('AUTOMATION_EXPORTS')
    Sql_Exports = os.getenv('SQL_Exports')

    return {
        "ACS_Year": os.getenv('TITLE_VI_GDB')[-6:-4],
        "Automation_Exports": Automation_Exports,
        "cf_gdb": os.path.join(Automation_Exports, "CurrentFiles.gdb"),
        "ds_gdb": os.path.join(Automation_Exports, f"DataStore_{sched_date}.gdb"),
        "sched_date": sched_date,
        "sign": current_sign(os.path.join(Sql_Exports, f'METROBUS-STOP-EXTRACTION{sched_date}.csv')),
        "Sql_Exports": Sql_Exports,
        "TitleVI": os.getenv('TITLE_VI_GDB'),
    }

def portal_config(fc_list, portal):
    features = []

    for fc in fc_list:
        if fc[portal] is True:
            list.append(fc)
            print(f"- {fc['title']}")

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
    else:
        print(f"{portal} is not a valid pole")
    profile["features"] = features
    return profile

def config_options(files, csv_dir, local):
    ap.env.workspace = os.path.join(local.Automation_Exports, local.ds_gdb)
    # csvs, csv_dir, local.sign, local.sched_date, local.ACS_Year, local.ds_gdb, local.cf_gdb
    sign = local.sign
    date = local.sched_date
    acs_year = local.ACS_Year
    ds_gdb = local.ds_gdb
    cf_gdb = local.cf_gdb
    title_vi_gdb = local.TitleVI

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
                "lightrail_buffer": "Lightrail_buffer"
            },
            "updateList":[
                "MetroBusRoutes",
                "MetroBusStops",
                "MetroBusGhostStops",
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
        }
    }
