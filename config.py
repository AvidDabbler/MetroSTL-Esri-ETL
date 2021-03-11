import os
import arcpy as ap
import glob

from gis_lib.helpers import * 


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
    Automation_Exports = os.environ['AUTOMATION_EXPORTS']
    Sql_Exports = os.environ['SQL_Exports']

    return {
        "ACS_Year": os.environ['TITLE_VI_GDB'][-6:-4],
        "Automation_Exports": Automation_Exports,
        "cf_gdb": os.path.join(Automation_Exports, "CurrentFiles.gdb"),
        "ds_gdb": os.path.join(Automation_Exports, f"DataStore_{sched_date}.gdb"),
        "sched_date": sched_date,
        "sign": current_sign(os.path.join(Sql_Exports, f'METROBUS-STOP-EXTRACTION{sched_date}.csv')),
        "Sql_Exports": Sql_Exports,
        "TitleVI": os.environ['TITLE_VI_GDB'],
    }

def portal_config(fc_list, portal):
    features = []

    for fc in fc_list:
        if fc[portal] is True:
            features.append(fc)
            print(f"- {fc['title']}")

    if portal == 'agol':
        profile = {
            "portal": 'https://www.arcgis.com/',
            "user": os.environ['AGOL_USER'],
            "password": os.environ['AGOL_PASSWORD'],
            "project": os.environ['AGOL_PROJECT'],
        }
    elif portal == 'enterprise':
        profile = {
            "portal": os.environ['ENTERP_PORTAL'],
            "user": os.environ['ENTERP_USER'],
            "password": os.environ['ENTERP_PASSWORD'],
            "project": os.environ['ENTERP_PROJECT'],
        }
    else:
        print(f"{portal} is not a valid portal")
    profile["portal_type"] = portal
    profile["features"] = features
    return profile

def config_options(files, csv_dir, local):
    ap.env.workspace = os.path.join(local['Automation_Exports'], local['ds_gdb'])
    # csvs, csv_dir, local.sign, local.sched_date, local.ACS_Year, local.ds_gdb, local.cf_gdb
    sign = local['sign']
    date = local['sched_date']
    acs_year = local['ACS_Year']
    ds_gdb = local['ds_gdb']
    cf_gdb = local['cf_gdb']
    title_vi_gdb = local['TitleVI']

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
            "ada": f'ADA_ROUTES{date}',
            "ghoststops": f'GHOST-STOPS-EXTRACTION{date}',
            "patterns": {
                "xy": f'METRO_PATTERNS_XY_{date}',
                "name": f'METRO_PATTERNS{date}',
                "line": f'METRO_PATTERNS{date}_{sign}',
            },
            "stops": f'METROBUS-STOP-EXTRACTION{date}',
            "stops_by_line": f'METROBUS-STOPBYLINE_EXTRACTION-WITH-DISTANCE{date}',
            "feat_classes":{
                "eam_stops": f"EAMMetroBusStops_{sign}_{date}",
                "eam_stops_1000": f"EAMMetroBusStops_1000_{sign}_{date}",
                "ghoststops": f'MetroBusGhostStops_{sign}_{date}',
                "routes": f'MetroBusRoutes_{sign}_{date}',
                "route_buffer": "MetroBusRouteBuffer_",
                "routes_dir": f'MetroBusRoutes_dir_{sign}_{date}',
                "stops": f'MetroBusStops_{sign}_{date}',
                "stops_by_line": f'MetroBusStopsByLine_{sign}_{date}',
                "sys_buffer": "MetroBusSystemBuffer_",
            },
            "registered": {
                "stops": "MetroBusStops_REGISTERED",
                "grid1000": "MGRS_Grid_1000",
                "eam_stops_1000": "EAMMetroBusStops_1000",
                "grid1000": "MGRS_Grid_1000",
                "grid10000": "MGRS_Grid_10000",
                "eam_stops": "EAMMetroBusStops_REGISTERED",
                "eam_stops": "EAMMetroBusStops_1000_REGISTERED",
                "lightrail_buffer": "Lightrail_buffer"
            },
            "updateList":[
                "MetroBusRoutes_REGISTERED",
                "MetroBusStops_REGISTERED",
                "MetroBusGhostStops_REGISTERED",
                "MetroBusStopsByLine_REGISTERED",
                "MetroBusRouteBuffer_05_REGISTERED",
                "MetroBusRouteBuffer_025_REGISTERED",
                "MetroBusRouteBuffer_075_REGISTERED",
                "MetroBusSystemBuffer_05_REGISTERED",
                "MetroBusSystemBuffer_025_REGISTERED",
                "MetroBusSystemBuffer_075_REGISTERED",
                "MetroBusRoutes_dir_REGISTERED",
                "EAMMetroBusStops_REGISTERED",
                "MetroADAServiceArea_REGISTERED"
            ]
        }
    }
