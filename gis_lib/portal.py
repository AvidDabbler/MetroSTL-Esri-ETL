import os
import arcpy as ap
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection


from .helpers import deleteFolder
     
# functions updates itemss using the return of the portal_config() and config_options()
# function cycles through features.py return that has a list of each feature class 
# information and the information that pertains to each portal
def updateItemsByID(portal, config):
    url = portal['portal']
    user = portal['user']
    password = portal['password']
    features = portal['features']
    portal_type = portal['portal_type']
    
    cf_gdb = config['cf_gdb']
    
    # connect to the specified portal
    gis = GIS(url, user, password)  # connect to what portal you are interested in publishing to using variables user and password
    
    # cycles throug the list of features that are filted by portal
    # controled by either agol or enterprise boolean field to determine 
    # if it a part of the list see the portal_config() return object
    for feature in features:
        print(f'Updating:')
        print(feature['title'])
        
        item_id = feature[f'{portal_type}_id']
        feature_layer = gis.content.get(item_id)
        print(item_id)
        # get the feature layer collection by unique id
        feature_layer_collection = FeatureLayerCollection.fromitem(feature_layer)
        # feature_layer = FeatureLayer.fromitem(feature_layer)
        print(feature_layer_collection.properties.description)
        
        # Feature Layer Collection Docs
        # https://developers.arcgis.com/python/api-reference/arcgis.features.toc.html?highlight=update%20metadata#featurelayercollection
        feature_layer_collection.manager.overwrite(os.path.join(cf_gdb, f'{feature["title"]}_REGISTERED'))
        
        # Update definition docs (Update Metadata)
        # https://developers.arcgis.com/python/api-reference/arcgis.features.managers.html?highlight=update_defin#arcgis.features.managers.FeatureLayerCollectionManager.update_definition
        feature_layer_collection.manager.update_definition({'description': feature['description']})
        
        
        
# OLD WAY OF PUBLISHING WITH APRX
# is not called by default but could be useful in the future
# you would need to specify the aprx project that has a bunch 
# of maps that have services that have previously been published 
def updatePortalLayers(portal):
    # def updateWebLayers(fc_list, user, password, url, project, enterprise=False):
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

    url = portal['portal']
    project = portal['project']
    password = portal['password']
    user = portal['user']
    features = portal['features']

    folder = 'REGISTERED_SERVICES'

    # Set sharing options
    shrOrg = False
    shrEveryone = False
    shrGroups = ""

    print('*****************************************************')
    print(f"Connecting to {url}...")

    gis = GIS(url, user, password)  # connect to what portal you are interested in publishing to using variables user and password

    print(' ')
    print(f"Connected!!!")
    print('*****************************************************')
    print(' ')
    print(' ')

    # End setting variables
    for fc in features:
        # Local paths to create temporary content
        print(f"Start of: {fc['title']}")
        print('*****************************************************')
        print(' ')
        relPath = 'A:\Open Data Admin\AutomationExports'
        print(f'relPath = {relPath}')

        sddraft = os.path.join(relPath, "WebUpdate.sddraft")
        sd = os.path.join(relPath, "WebUpdate.sd")

        # Create a new SDDraft and stage to SD
        print("Creating SD file")
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
        print("Search for original SD on portal ...")
        print(f"Query: {hosted_file_name}")

        updateList =["Service Definition",
                     ""]

        for item in updateList:
            print('')
            print(f'Start of {fc["title"]} {item}')
            print("*******************************")
            print('')
            list = gis.content.search(query=hosted_file_name, item_type=item)

            # scan list of items to make sure they are an exact match to hosted_file_name
            # preform update() and publish() to "Service Definition"
            i = 0
            # cycle through the list that search() brought back to make sure that it is an exact match to hosted_file_name
            while list[i].title != hosted_file_name:
                i += 1

            print('MATCH FOUND!!!')
            print(list[i])
            print(f'item[i].title = {list[i].title}, hosted_file_name = {hosted_file_name}')
            item = list[i] # define item based on above findings

            item.update(data=sd) # use sd to update hosted "Service Definition" file
            print("Overwriting existing feature service ...")


            if item == 'Service Definition':
                fs = item.publish(overwrite=True)  # publish "Service Definition"

                if shrOrg or shrEveryone or shrGroups: # update sharing groups
                    print("Setting sharing options ...")
                    fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)

            print("Updating Metadata...")
            item.update(item_properties={'snippet': fc['summary'],
                                         'tags': fc['tags'],
                                         'description': fc['description']})

            try:
                item.publish(overwrite=True)
                print('Published Service Definition!!!')
            except:
                print('Could Not Publish!!!!')



        # START OF UPDATE TO VIEWS ON PORTAL

        print("")
        print(f"Start of {fc['view_title']} View Update")
        print("*******************************")
        print("")
        print("Search for view portal ...")
        print(f"Query: {fc['view_title']}, folder: 'REGISTERED VIEWS'")

        list = gis.content.search(query=f"title: '{fc['view_title']}'", item_type='')
        print(list)
        # scan list of items to make sure they are an exact match to hosted_file_name
        # preform update() and publish() to "Service Definition"
        i = 0
        # cycle through the list that search() brought back to make sure that it is an exact match to hosted_file_name
        while list[i].title != fc['view_title']:
            i += 1

        print('MATCH FOUND!!!')
        print(list[i])
        print(f'item[i].title = {list[i].title}, hosted_file_name = {fc["view_title"]}')
        item = list[i] # define item based on above findings

        item.update(data=sd) # use sd to update hosted "Service Definition" file
        print("Overwriting existing feature service ...")


        if item == 'Service Definition':
            fs = item.publish(overwrite=True)  # publish "Service Definition"

            if shrOrg or shrEveryone or shrGroups: # update sharing groups
                print("Setting sharing options ...")
                fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)

        print("Updating Metadata...")
        item.update(item_properties={'snippet': fc['summary'],
                                     'tags': fc['tags'],
                                     'description': fc['description']})
        try:
            item.publish(overwrite=True)
        except:
            print('Could Not Publish!!!!')

        print(f"Finished updating: {list[i].title} – ID: {list[i].id}")
        print('')
        print('*********************************************')
        print('')