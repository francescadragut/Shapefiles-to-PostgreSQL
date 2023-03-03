# Shapefiles to PostgreSQL

## Important information

The script was originally designed to take the most granular shapefile from a subfolder and upload it to a table in PostgreSQL. On the original structure, the files were in many subfolders belonging to a root folder, which you pass as an argument when running the script. If you have all your data in one folder, make sure you either add it to a root folder or that you modify the code to your needs.

**Make sure your PostgreSQL database has the PostGIS extension enabled.**

## Functions

- `get_directories()` - returns a list of all subdirectories of the directory passed as an argument
- `get-shapefiles()` - returns a list of all shapefiles present in a directory
- `get-most-granular()` - returns the most granular shapefile from a list of shapefiles; this is a filtering functionality that takes the richest-in-data file from a bunch of similar files
- `geo-preprocessing()` - converts the shapefile to a 3857 projection and makes sure that the MULTIPOLYGON features are converted to POLYGON, for uniform data
- `export-files()` - exports the highest-granularity shapefile to PostgreSQL 


## Run script

Open terminal, cd to project folder and run the following command, with the input and output directory of the files:
`python3 main.py --host <HOST> --user <USER> --db <DATABASE> --pw <PASSWORD> --dir <INPUT-DIRECTORY> --table <OUTPUT-TABLE>`

If the '''table''' does not exist in the database, the program will create it.
