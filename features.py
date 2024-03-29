def features(date_formatted):
    return  [{"title": "MetroBusRoutes",
            "view_title": "Metro St. Louis MetroBus Routes",
            "summary": f"Current MetroBus Routes for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes for the Metro Saint Louis Transit system as of {date_formatted}. "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984</div></div>"
                           f"<div><div><br /><b>Field Names and Descriptions:</b>"
                           f"<div><div><br />RouteAbbr: Private Route code (Text)"
                           f"<div><div><br />LineName: Public Route Number and Route Name "
                           f"<div><div><br />PubNum: Public Route Number "
                           f"<div><div><br />LineNum: Private Route code (Integer)"
                           f"<div><div><br />ADA: Does this route have ADA Call-a-ride service (1 = True, 0 = False)",
            "tags": ["routes", "metrobus", "bus"],
            "enterprise": True,
            "enterprise_id": "03640efc5849498eaca1afb7d4610c86",
            "agol": True,
            "agol_id": "08a5bfc4fb974e94b03cfe24627cc43c",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroBusStops",
            "view_title": "Metro St. Louis MetroBus Stops",
            "summary": f"Current MetroBus Stops for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Stops for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b>"
                           f"<div><div><br />Seq: Stop Sequence"
                           f"<div><div><br />SignID: Sign associated with the schedule release with file"
                           f"<div><div><br />StopID: Id associated with the Stop location"
                           f"<div><div><br />StopAbbr: Stop Abbreviation"
                           f"<div><div><br />StopName: Stop Name"
                           f"<div><div><br />OnSt: Street that the stop is on"
                           f"<div><div><br />AtSt: Cross street that the stop is on"
                           f"<div><div><br />StopPos: Stop Position"
                           f"<div><div><br />PrefTrans: Preferred Transfer location"
                           f"<div><div><br />Bench: Bench located at stop (1 = True, 0 = False)"
                           f"<div><div><br />Shelter: Shelter located at stop (1 = True, 0 = False)"
                           f"<div><div><br />Transfer: Transfer located at stop (1 = True, 0 = False)"
                           f"<div><div><br />PubWay: Stop in public right of way (1 = True, 0 = False)"
                           f"<div><div><br />Node: Id for timepoint"
                           f"<div><div><br />LineName: Public number and route name associated with this iteration of the stop."
                           f"<div><div><br />RouteCode: Private route code associated with this iteration of the stop."
                           f"<div><div><br />Dir: Direction of route"
                           f"<div><div><br />CountyCode: County code where the stop is located"
                           f"<div><div><br />Juris: Jurisdiction code where the stop is located"
                           f"<div><div><br />GPS_Lon: Longitude"
                           f"<div><div><br />GPS_Lat: Latitude",
            "tags": ["stops","metrobus","bus"],
            "enterprise": True,
            "enterprise_id": "0e86eeb07c924b5497639870cdb8192e",
            "agol": True,
            "agol_id": "b7c1023f73b646cba96408cf396b7605",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroBusStopsByLine",
            "view_title": "Metro St. Louis MetroBus Stops By Line",
            "summary": f"Current MetroBus Stops by Line for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Stops by Line for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />Seq: Stop Sequence"
                           f"<div><div><br />SignID: Sign associated with the schedule release with file"
                           f"<div><div><br />StopID: Id associated with the Stop location"
                           f"<div><div><br />StopAbbr: Stop Abbreviation"
                           f"<div><div><br />StopName: Stop Name"
                           f"<div><div><br />OnSt: Street that the stop is on"
                           f"<div><div><br />AtSt: Cross street that the stop is on"
                           f"<div><div><br />StopPos: Stop Position"
                           f"<div><div><br />PrefTrans: Preferred Transfer location"
                           f"<div><div><br />Bench: Bench located at stop (1 = True, 0 = False)"
                           f"<div><div><br />Shelter: Shelter located at stop (1 = True, 0 = False)"
                           f"<div><div><br />Transfer: Transfer located at stop (1 = True, 0 = False)"
                           f"<div><div><br />PubWay: Stop in public right of way (1 = True, 0 = False)"
                           f"<div><div><br />Node: Id for timepoine"
                           f"<div><div><br />LineName: Public number and route name associated with this iteration of the stop."
                           f"<div><div><br />RouteCode: Private route code associated with this iteration of the stop."
                           f"<div><div><br />Dir: Direction of route"
                           f"<div><div><br />CountyCode: County code where the stop is located"
                           f"<div><div><br />Juris: Jurisdiction code where the stop is located"
                           f"<div><div><br />GPS_Lon: Longitude"
                           f"<div><div><br />GPS_Lat: Latitude"
                           f"<div><div><br />Dist: Distance to next stop",
            "tags": ["stops by line", "stops", "metrobus", "bus"],
            "enterprise": True,
            "enterprise_id": "73008c5a2efc4b6c8b67e277e3fd288e",
            "agol": True,
            "agol_id": "da870654315144468d08af756b2522f1",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroFacilities",
            "view_title": "Metro St. Louis Facilities Locations",
            "summary": f"Current Metro Saint Louis Transit Facility Location points as of {date_formatted}.",
            "description": f"Current Metro Saint Louis Transit Facility Locations as of {date_formatted}."
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />NAME: Name of Facility"
                           f"<div><div><br />TYPE: Type of Facility"
                           f"<div><div><br />ADDRESS: Mailing Address"
                           f"<div><div><br />CITY: City"
                           f"<div><div><br />STATE: State"
                           f"<div><div><br />ZIP: Zipcode"
                           f"<div><div><br />POINT_X: Longitude"
                           f"<div><div><br />POINT_Y: Latitude",
            "tags": ["metrolink", "light rail", "metrobus", "bus", "assets"],
            "enterprise": True,
            "enterprise_id": "e1b4b2d39e1944b38b198fe2d502d3fd",
            "agol": True,
            "agol_id": "9d783ce8a4b041a8b4c3d6cfe58c43be",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroFacilitiesPoly",
            "view_title": "Metro St. Louis Facilities Boundaries",
            "summary": f"Current Metro Saint Louis Transit Facility Location polygons as of {date_formatted}.",
            "description": f"Current Metro Saint Louis Transit Facility Location polygons as of {date_formatted}. "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />NAME: Name of Facility"
                           f"<div><div><br />TYPE: Type of Facility",
            "tags": ["metrolink", "light rail", "metrobus", "bus", "assets"],
            "enterprise": True,
            "enterprise_id": "27312f0d93ef4855b126b3751085e268",
            "agol": True,
            "agol_id": "85b81bbee972424289b7338321fce1c5",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroLinkAlignment",
            "view_title": "MetroLink Alignment",
            "summary": f"Current MetroLink light rail Alignment for the Metro Saint Louis Transit system covering the Blue and Red lines as of {date_formatted}.",
            "description": f"Current MetroLink light rail Alignment for the Metro Saint Louis Transit system covering the Blue and Red lines as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />I_RTE_CO: Internal Route Code"
                           f"<div><div><br />RTE_NAME: Route Name"
                           f"<div><div><br />P_RTE_CO: Private Route Code",
            "tags": ["metrolink", "light rail", "alignment"],
            "enterprise": True,
            "enterprise_id": "27e064330e1d4d57a0057dff1a684b6c",
            "agol": True,
            "agol_id": "c4aee4a01cc044baa2dfdaca14676ced",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroLinkStations",
            "view_title": "MetroLink Stations",
            "summary": f"MetroLink Stations for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"MetroLink Stations for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />SIGNID: Updated Sign ID sign assciated with the service update that is associated with the last update "
                           f"<div><div><br />Stop ID (STP_ID): Official Stop ID code "
                           f"<div><div><br />STP_ABBR: Stop Abbreviation "
                           f"<div><div><br />Stop Name (STP_NAME): The official Public name of the stop "
                           f"<div><div><br />On Street (ON_ST): The On Street that the Station is physically located on. "
                           f"<div><div><br />At Street (AT_ST): The At Street that the Station is located (Adjacent road) "
                           f"<div><div><br />STP_P: Stop Position "
                           f"<div><div><br />P_TRF: If the station is a preferred transfer (1 = True, 0 = False) "
                           f"<div><div><br />BNCH: If the station has a bench (1 = True, 0 = False) "
                           f"<div><div><br />SHLT: If the station has a shelter (1 = True, 0 = False) "
                           f"<div><div><br />TRF: If the station is a transfer location (1 = True, 0 = False) "
                           f"<div><div><br />County: County that the Station is in "
                           f"<div><div><br />Municipality (JURIS): Municipality the Station is in "
                           f"<div><div><br />GPS_LON: Longitude "
                           f"<div><div><br />GPS_LAT: Latitude",
            "tags": ["metrolink", "light rail", "assets"],
            "enterprise": True,
            "enterprise_id": "e817476fde2347f3886114b1b5df1396",
            "agol": True,
            "agol_id": "cb5103b6e529476699c88d92b9e40627",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "ServiceArea",
            "view_title": "MetroBus & MetroLink Service Area",
            "summary": f"Metro Service Area for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Metro Service Area for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />STATEFP: Census State Code"
                           f"<div><div><br />COUNTYFP: Census County Code "
                           f"<div><div><br />AFFGEOID: Full Census GeoID"
                           f"<div><div><br />GEOID: Census State County Code"
                           f"<div><div><br />NAME: Name of County"
                           f"<div><div><br />StCoCode: Census State County Code",
            "tags": ["service area", "polygons", "service area"],
            "enterprise": True,
            "enterprise_id": "83158acf097f47b0a7f4a313a40a0df7",
            "agol": True,
            "agol_id": "6c8fa107508041c39ae9a7497f6c8d60",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroBusRoutes_dir",
            "view_title": "MetroBus & MetroLink St. Louis Route Buffers by Route Direction",
            "summary": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted} "
                           f"<div><div><br />Projection: WGS1984 "
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />RouteAbbr: Private Route Number (Text) "
                           f"<div><div><br />DirName: Direction name of route feature "
                           f"<div><div><br />LineName: Public Route Number and Name "
                           f"<div><div><br />PubNum: Public Route Name "
                           f"<div><div><br />LineNum:	Private Route Number (Integer)"
                           f"<div><div><br />ADA: Does this route have ADA Call-a-ride service (1 = True, 0 = False)",
            "tags": ["routes","metrobus","bus"],
            "enterprise": True,
            "enterprise_id": "b0b48ae406f545cab540513ebf67cb49",
            "agol": True,
            "agol_id": "36da9094e82e46ce9b2322ddf0b9e07d",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "SystemBuffers",
            "view_title": "MetroBus & MetroLink St. Louis System Buffers",
            "summary": f"Current MetroBus System buffered by 1/4, 1/2, and 3/4 miles for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.  <div><div><br />Date Published: {date_formatted} <div><div><br />Projection: WGS1984 "
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />type: States the buffer type "
                           f"<div><div><br />ClipPop025: Estimated population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipMin025: Estimated Minority population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipLEP025: Estimated Limited English Proficiency population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipPov025: Estimated Poverty population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipSen025: Estimated Senior population within 0.25 miles of system buffer "
                           f"<div><div><br />ClipNoCar025: Estimated population with no cars in household within 0.25 miles of system buffer "
                           f"<div><div><br />ClipLowCar025: Estimated population within a Low Car household within 0.25 miles of system buffer"
                           f"<div><div><br />ClipPop050: Estimated population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipMin050: Estimated Minority population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipLEP050: Estimated Limited English Proficiency population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipPov050: Estimated Poverty population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipSen050: Estimated Senior population within 0.50 miles of system buffer "
                           f"<div><div><br />ClipNoCar050: Estimated population with no cars in household within 0.50 miles of system buffer "
                           f"<div><div><br />ClipLowCar050: Estimated population within a Low Car household within 0.50 miles of system buffer "
                           f"<div><div><br />ClipPop075: Estimated population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipMin075: Estimated Minority population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipLEP075: Estimated Limited English Proficiency population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipPov075: Estimated Poverty population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipSen075: Estimated Senior population within 0.75 miles of system buffer "
                           f"<div><div><br />ClipNoCar075: Estimated population with no cars in household within 0.75 miles of system buffer "
                           f"<div><div><br />ClipLowCar075: Estimated population within a Low Car household within 0.75 miles of system buffer "
                           f"<div><div><br />***ALL POPULATIONS ARE BASED ON THE 2017 US CENSUS. FOR METHODOLOGIES CONTACT METRO SAINT LOUIS RESEARCH & DEVELOPMENT",
            "tags": ["system buffers", "system", "buffers", "transit", "bus"],
            "enterprise": True,
            "enterprise_id": "d2655007b5844e7e996683c05d8cf9b8",
            "agol": True,
            "agol_id": "50ee3c009b3849e999358a7a1ef3c1f1",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "RouteBuffers",
            "view_title": "MetroBus & MetroLink St. Louis Route Buffers",
            "summary": f"Current MetroBus Routes buffered by 1/4, 1/2, and 3/4 miles for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.  <div><div><br />Date Published: {date_formatted} <div><div><br />Projection: WGS1984"
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br />RouteAbbr: Private Route Code (Text)"
                           f"<div><div><br />LineName: Public Route Number and Name"
                           f"<div><div><br />PubNum: Public Route Number"
                           f"<div><div><br />LineNum: Private Route Number (Integer"
                           f"<div><div><br />BUFF_DIST: Distance the Route was Buffered (Miles)",
            "tags": ["route buffers", "route", "buffers", "bus"],
            "enterprise": True,
            "enterprise_id": "e3c61352ccbe4dbea65d5b505c930425",
            "agol": True,
            "agol_id": "6460f4de7bbe44a3b3f3214a2ee660ff",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "MetroADAServiceArea",
            "view_title": "Metro St. Louis ADA Service Area",
            "summary": f"Current MetroBus Routes buffered by 1/4, 1/2, and 3/4 miles for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus Routes by Direction for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br />Date Published: {date_formatted}"
                           f"<div><div><br />Projection: WGS1984 "
                           f"<div><div><br /><b>Field Names and Descriptions:</b> "
                           f"<div><div><br /><br />Name: Name of the service area",
            "tags": ["system", "route", "buffers", "bus", "ada"],
            "enterprise": True,
            "enterprise_id": "f7594284f2044bd1bcc829772320bf24",
            "agol": True,
            "agol_id": "4767d12a9c354c9a9892436bcddf18eb",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "CurrentSystem",
            "view_title": "Current MetroBus & MetroLink Stops and Routes",
            "summary": f"Current MetroBus and MetroLink system for the Metro Saint Louis Transit system as of {date_formatted}.",
            "description": f"Current MetroBus and MetroLink system for the Metro Saint Louis Transit system as of {date_formatted}.  "
                           f"<div><div><br /><br />Date Published: {date_formatted} "
                           f"<div><div><br /><br />Projection: WGS1984",
            "tags": ["route buffers", "route", "bus", "metrobus", "metrolink"],
            "enterprise": True,
            "enterprise_id": "0d3ce62d6a08433c906fc7d6809d0d1f",
            "agol": True,
            "agol_id": "0926acd392b641feb0e1957fa624171d",
            "enterprise_fields": [],
            "agol_fields": [],
            },

            {"title": "EAMMetroBusStops",
            "view_title": "EAM MetroBus Stops",
            "summary": f"Current MetroBus formatted for the Metro Saint Louis Transit EAM system as of {date_formatted}.",
            "description": f"Current MetroBus formatted for the Metro Saint Louis Transit EAM system as of {date_formatted}.  "
                           f"<div><div><br /><br />Date Published: {date_formatted} "
                           f"<div><div><br /><br />Projection: WGS1984",
            "tags": ["EAM", "stops", "bus", "metrobus"],
            "enterprise": True,
            "enterprise_id": "7f358dbcfdfd4086a7a4ebaba33f4d06",
            "agol": False,
            "agol_id": "2de76e0953d2466d8604c8280dda1857",
            "enterprise_fields": [],
            "agol_fields": [],
            },
            # {"title": "GhostStops",
            # "view_title": "MetroBus Ghost Stops",
            # "summary": f"Current inactive MetroBus Stops for Metro Saint Louis Transit as of {date_formatted}.",
            # "description": f"Current MetroBus formatted for the Metro Saint Louis Transit EAM system as of {date_formatted}.  "
            #                f"<div><div><br /><br />Date Published: {date_formatted} "
            #                f"<div><div><br /><br />Projection: WGS1984",
            # "tags": ["ghost", "stops", "bus", "metrobus"],
            # "enterprise": True,
            # "enterprise_id": "4f8abd9b058f4efeb7d6f8d643e723e7",
            # "agol": False,
            # "enterprise_fields": [],
            # "agol_fields": [],
            # },
            ]

