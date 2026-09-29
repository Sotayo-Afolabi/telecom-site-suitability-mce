import requests
import os
import zipfile
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry


# if __name__ == "__main__":
#   DB_URL = ""


class TelecomETL:
    def __init__(self, db_url, local_csv_file_dir, local_shapefile_dir, target_region_name):
        self.db_url = db_url
        self.local_csv_file_path = local_csv_file_dir
        self.local_shapefile_dir = local_shapefile_dir
        self.target_region_name = target_region_name
        self.engine = create_engine(self.db_url)

        self.tele_csv_df = None
        self.tele_csv_gdf = None
        self.shapefile_boundry_gdf = None
        self.region_name_gdf = None
        self.vectors = {}  # stores all our vector layers in a dictionary
        # we dont actually need this because our rater doesnt save to the database
        self.raster_path = {}

    def extract(self):
        # extracts our csv file
        csv_file = os.path.join(self.local_csv_file_path, "621.csv")
        if not os.path.exists(csv_file):
            raise FileNotFoundError('Couldnt find the csv file')
        print(f'collecting your csv file from {csv_file}')
        self.tele_csv_df = pd.read_csv(csv_file)

        # extract All needed vector files

        vector_files = {
            'Boundary': 'gis_osm_adminareas_a_free_1.shp',
            'Roads': 'gis_osm_roads_free_1.shp',
            'Hydrology_line': 'gis_osm_waterways_free_1.shp',
            'Hydrology_polygon': 'gis_osm_water_a_free_1.shp',
            'landuse': 'gis_osm_landuse_a_free_1.shp'
        }

        for feature_name, shp_file in vector_files.items():
            path = os.path.join(self.local_shapefile_dir, shp_file)
            if os.path.exists(path):
                print(f'Extracting {feature_name} shapefile from {path}')
                self.vectors[feature_name] = gpd.read_file(path)
            else:
                print(
                    f'file {shp_file} not found, skipping {feature_name} moving on to the next shapefile'
                )

        # dem raster extraction which we dont actually need, but, why not
        dem_path = os.path.join(
            self.local_shapefile_dir, 'ogun_dem_clipped.tif')
        if os.path.exists(dem_path):
            print(f'extracting your dem from {dem_path}')
            self.raster_path['dem'] = dem_path
            print('EXTRACTION COMPLETED!!!')

        else:
            print('raster file not found')

    # transforms the data
    def transform(self):
        print("Transforming your data")

    # Delete incomplete row of lon and lat from the csv
        self.tele_csv_df.dropna(subset=['lon', 'lat'], inplace=True)

        # converts the csv long and lat colomns numbers to wgs84 (EPSG:4326) long and lat
        self.temp_tele_csv_gdf = gpd.GeoDataFrame(
            self.tele_csv_df,
            geometry=gpd.points_from_xy(
                self.tele_csv_df.lon, self.tele_csv_df.lat),
            crs="EPSG:4326"
        )

        # reproject the shapefiles and the csv in EPSG:4326 to utm 31N(EPSG: 32631)
        self.tele_csv_gdf = self.temp_tele_csv_gdf.to_crs(epsg=32631)

        for feature_name in self.vectors:
            self.vectors[feature_name] = self.vectors[feature_name].to_crs(
                epsg=32631)

        # Filter the location we need(i.e abeokuta from the shape file), we could choose to do this from the database as well
        boundary_layer = self.vectors["Boundary"]
        self.region_name_gdf = boundary_layer[boundary_layer['name']
                                              == self.target_region_name]

       # merge hydrographic layers
        if ('Hydrology_line' in self.vectors and 'Hydrology_polygon' in self.vectors):
            print('merging Hydro layers..........')
            lines = self.vectors['Hydrology_line'][['geometry']]
            poly = self.vectors['Hydrology_polygon'][['geometry']]
            self.vectors['unified_water'] = pd.concat(
                [lines, poly], ignore_index=True)
            print("Transformation  complete")

    # Loading our data into the postgis database
    def load(self):
        print('Loading data into postgres/postgis')
        self.tele_csv_gdf.to_postgis(
            name='telecom_tower',
            con=self.engine,
            if_exists='replace',
            index=False,
            dtype={'geometry': Geometry('POINT', srid=32631)}
        )

        if self.region_name_gdf is not None:
            self.region_name_gdf.to_postgis(
                name='target_region',
                con=self.engine,
                index=False,
                if_exists='replace',
                dtype={'geometry': Geometry('MULTIPOLYGON', srid=32631)}
            )

        for feature_name, gdf in self.vectors.items():
            gdf.to_postgis(
                name=f'layer_{feature_name}',
                con=self.engine,
                index=False,
                if_exists='replace',
                dtype={'geometry': Geometry('GEOMETRY', srid=32631)}
            )


# Database connection setup
host = "localhost"
database = "telecom_gis"
# for your use you can directly write your username and password
user = os.getenv('SQL_USER')
password = os.getenv('SQL_PASSWORD')


DB_URL = f"postgresql://{user}:{password}@{host}/{database}"
csv_location = r'C:\Users\user\Documents\Gis Project 1\telecom csv'
shapefile_dir = r'C:\Users\user\Documents\Gis Project 1\nigeria-260712-free.shp'
focus_region = 'Ogun'


ogunstate_etl = TelecomETL(
    db_url=DB_URL,
    local_csv_file_dir=csv_location,
    local_shapefile_dir=shapefile_dir,
    target_region_name=focus_region,
)


# execution of our class functions
ogunstate_etl.extract()
ogunstate_etl.transform()
ogunstate_etl.load()

