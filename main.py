import argparse
from sqlalchemy import create_engine
import geopandas as gpd
from pathlib import Path
import psycopg2


HOST = ''
USER = ''
DB = ''
PW = ''
INPUT_DIR = ''
TABLE = ''

ROOT_DIR = Path('.').absolute()
SHP_DIR = ROOT_DIR.joinpath(Path('most-granular-shapefiles'))
EXT = '.shp'


def get_directories():
    """ Return a list of subdirectories containing shapefiles """
    return [Path(SEARCH_DIR).joinpath(Path(f)) for f in Path(SEARCH_DIR).iterdir() if Path(f).is_dir()]
    


def get_shapefiles(dir_path):
    """ Return a list of shapefiles contained in the directory of a country"""
    return [str(Path(dir_path).joinpath(Path(f))) for f in Path(dir_path).iterdir() if str(f).endswith(EXT)]


def get_most_granular(files):
    """ Return dataframe and filename of the shapefile with highest granularity """
    max_rows = -1
    most_granular_df = gpd.GeoDataFrame()
    most_granular_filename = ''
    for file in files:
        file_df = gpd.read_file(file, encoding='utf-8')
        rows = len(file_df)
        if rows > max_rows:
            max_rows = rows
            most_granular_df = gpd.GeoDataFrame(file_df)
            most_granular_filename = str(Path(file).stem)
    return most_granular_df, most_granular_filename


def geo_preprocessing(dataframe):
    """ Preprocess dataframe for export to PostGIS - reproject to EPSG:3857 and convert geometry to POLYGON """
    reprojected = dataframe.to_crs(epsg=3857)
    return reprojected.explode(index_parts=False)


def export_files(dirs):
    """ Export to PostGIS shapefile with highest granularity from the subdirectory of each country """
    engine = create_engine(f"postgresql://{USER}:{PW}@{HOST}/{DB}")
    for dir in dirs:
        files = get_shapefiles(dir)
        most_granular, table_name = get_most_granular(files)
        preprocessed = geo_preprocessing(most_granular)
        # preprocessed.to_file(f"{SHP_DIR}/{table_name}.shp")
        preprocessed.to_postgis(f"{TABLE}", engine, if_exists='append', index=False)
        print(f"Exported {table_name} to {TABLE}")

def add_primary_key(table):
    conn = psycopg2.connect(database=f"{DB}", user=f"{USER}", password=f"{PW}", host=f"{HOST}")
    cursor = conn.cursor()
    sql = f'''ALTER TABLE {table} ADD ID SERIAL PRIMARY KEY;'''
    cursor.execute(sql)
    cursor.close()
    conn.commit()

if __name__ == "__main__":
  
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--user', type=str, required=True)
    parser.add_argument('--db', type=str, required=True)
    parser.add_argument('--pw', type=str, required=True)
    parser.add_argument('--dir', type=str, required=True)
    parser.add_argument('--table', type=str, required=True)
    args = parser.parse_args()

    HOST = args.host
    USER = args.user
    DB = args.db
    PW = args.pw.strip('"')
    INPUT_DIR = args.dir
    TABLE = args.table

    print("HOST: ", HOST)
    print("USER: ", USER)
    print("DB: ", DB)
    print("PW: ", PW)
    print("INPUT_DIR: ", INPUT_DIR)
    print("TABLE: ", TABLE)


    SEARCH_DIR = f"{ROOT_DIR}/{INPUT_DIR}"
    print(SEARCH_DIR)

    dirs = get_directories()
    export_files(dirs)
    #add_primary_key(TABLE)
    


   

    