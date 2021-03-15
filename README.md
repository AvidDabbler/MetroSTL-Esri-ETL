# Metro St Louis GIS Data Pipeline

## Intro
This script was created to keep the Metro St Louis datastores up to date for both the AGOL and on-site ArcGIS Enterprise instances. This script is meant to pull data from a static directory as CSV files and tranfer them into geographic datasets stored in gdb's then update a local current files gdb and publish all of the file in the current gdb to both of the clouds.


![GIS Data Pipeline Diagram](./GIS_Data_Pipeline.svg)


Moving forward with Apache Airflow, the necessity of static file directories and the Cronjob's that end up calling them will be obsolete. Instead what will end up happening will be a every Monday AirFlow will run the queries for all of the files to run via Python. These tables could be stored in a static directory for safe keeping or they could just be run and stored in the weekly gdb's. If that were the case it would be best to have them set up in parallel jobs separating out each of the specific queries to the dependencies as opposed to just running the queries and then storing them then have another job to follow immediately. This would save memory and allow it to run faster especially for some of the larger files like *patterns*.

This project is broken up into 4 different parts:
- .env
- Config
- SQL
- Features
- Gis Library

## General File Architecture
These files are broken out into specific groups to improve the ability of debugging and ensuring that each of the functions is not dependent on global variables. Instead objects are passed in through a single variable in the call that has all of the information it needs to run. These objects are addressed in the config section. To ensure that the file is as short hand as possible the objects are destructured at the top of each functions turning `config['date]` into a short of `date`.

## Running the Script
In order to run this script you will need to start up a local ArcGIS Python environment. It is recomended that you make a copy of the main ArcGIS Python environment using ArcPro and then activate the environment or run something like:
 
 `activate C:\Users\%USER%\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone3`
 
 Other than the standard ArcPy environments that you need you will need a `dotenv` lib called [python-dotenv](https://pypi.org/project/python-dotenv/). Once you have your environment setup you will need to run in the terminal:
 
  `python run()` 
  
  in the root directory of this project. Everything should do its thing after that.

## .env
The .env file is something that is NOT updated when pushed to github. In the project there is a *template.env* that you could customize with the neccessary variables that allow you to connect the AGOL / Enterprise accounts as well as the local directories that you are using to store files. 

## Config
The config files are broken up into a couple of different funnctions and for the most part you don't need to change as they really only take the date in as a parameter.

### local_config()
Local config is a file that sets up all of your local file variables and will return a config file that will be useful throughout the project.

### portal_config()
For each of the portals there is a portal_config function that takes in a portal type and a features_list (*see [Features](#Features)). This could have been a Class, but I don't like writing classes :p . 

### config_options()
Config Options is the consolidation of all of the config files.

## SQL
In the root directory of the project there are some backedup sql files in the `./sql` directory. These files are used to call the associated tables that are used throughout the process. In the DBA directory is the version that goes to the DBA's that allows them to export all of the columns in a concatonated single column with a `, ` as a seperator so it can be used later. The DBA way of exporting does not allow for the easy export of deliminated files with column names so add_columns() is used to add back in the column names. When AirFlow is implemented this will be a non-issue and will allow for the deprication of add_columns as well as the need for DBA's to run that on a schedule.

## Features
The features file is a list of Feature Services that exist either on the Enterprise, AGOL or Both. The return value is a list of feature's objects that contain all of the metadata for that feature service. When it is called inthe portal_config() if filtered each of the items in the list using the enterprise / agol boolean value field.

## Gis Library
The gis_lib directory is where all of the functions for transforming and publishing all of the non-spatial tables to gdb's to each of the portals. When the files finally make it to the Current GDB the portal config file is used for each portal to determine which files in the Current GDB get published to which portal using the associated portal id field.



**IMPORTANT NOTE ON PUBLISHIN**

If you  end up having to republish or are having a hard time publishing a specific feature service. Make sure that the portal item id's match. 
