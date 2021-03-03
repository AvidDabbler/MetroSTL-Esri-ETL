import os
import arcpy as ap


def adaCreation(config):
    sign = config.sign
    date = config.date
    cf_gdb = config.cf_gdb
    ds_gdb = config.ds_gdb
    lightrail_buffer = config.registered.lightrail_buffer

    print('start of ada creation')
    # sign = s
    mb_sys_buffer = f'MetroBusRouteBuffer_075_{sign}_{date}'
    mb_sys_buffer_loc = os.path.join(ds_gdb, mb_sys_buffer)

    # SETTING UP FOR MetroADAServiceArea
    ada_fill = os.path.join(cf_gdb, 'ADA_Fill')
    lightrail_buffer_loc = os.path.join(cf_gdb, lightrail_buffer)
    ada_system_merge = os.path.join(ds_gdb, f'MetroADASysMerge_{sign}_{date}')
    ada_service_area = os.path.join(ds_gdb, f'MetroADAServiceArea_{sign}_{date}')
    ada_route_buffer = f"ADARouteBuffer_{sign}_{date}"
    ada_route_buffer_loc = os.path.join(ds_gdb, ada_route_buffer)

    ap.env.overwriteOutput = True

    # deleteFeatureClass(ada_service_area, ds_gdb)
    # deleteFeatureClass(ada_system_merge, ds_gdb)
    # deleteFeatureClass(ada_route_buffer, ds_gdb)

    # MERGE METROBUS SYSTEM BUFFER WITH LIGHTRAIL ALIGNMENT BUFFER AND 270 FILL IN
    ap.FeatureClassToFeatureClass_conversion(mb_sys_buffer_loc, ds_gdb, ada_route_buffer, 'ADA = 1')
    ap.Merge_management([ada_fill, ada_route_buffer, lightrail_buffer_loc], ada_system_merge)
    ap.AddField_management(ada_system_merge, 'Name', 'TEXT')
    ap.CalculateField_management(ada_system_merge, "Name", "'Metro ADA Service Area'", "PYTHON3")

    # DISSOLVE MERGED LAYERS INTO MetroADAServiceArea
    ap.Dissolve_management(ada_system_merge, ada_service_area, "Name")
    # deleteFeatureClass(ada_system_merge, ds_gdb)
    print('end of ada creation')
