import json
import time
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim


with open('json-locations-15min-around-exchange-district.json', 'rb') as file:
    data = json.load(file)

json_extract = data['results'][0]['shapes'][0]['shell']


# load json location data into dataframe
locations = pd.DataFrame(json_extract, columns=['lng', 'lat'])

# convert lat and lon into geopandas
geometry = [Point(xy) for xy in zip(locations['lng'], locations['lat'])]
gdf_points_srnd = gpd.GeoDataFrame(locations, geometry=geometry)
# assign crs 4326 to gdf_points
gdf_points_srnd = gdf_points_srnd.set_crs('EPSG:4326')

# load dissemination area from shape file. source: statistics canada
shapefile = gpd.read_file('statistics-canada-dissemination-areas.shp')
# Extract only valid geometries
shapefile = shapefile[shapefile.is_valid]

# convert all to same coordinate reference system
gdf_points_srnd = gdf_points_srnd.to_crs(shapefile.crs)

# Exchange district = points between min and max of gdf_points
exchange_district_bounds = gdf_points_srnd.total_bounds

exchange_district = shapefile.cx[exchange_district_bounds[0]:exchange_district_bounds[2],
                                 exchange_district_bounds[1]:exchange_district_bounds[3]]

# print(exchange_district)

# # spatial join
# gdf = gpd.sjoin(gdf_points, shapefile, how = 'left', op='within')
# print(gdf)

# Dissemination areas to csv file
# exchange_district.to_csv('exchange-district-dissemination-areas.csv',
#                          columns=['DAUID','DGUID','LANDAREA','PRUID'],
#                          index = False)

# # Plot exchange district dissemination areas
# ax = shapefile.plot(edgecolor = 'blue')
# gdf_points_srnd.plot(ax = ax, color = 'red', markersize = 15)
# plt.show()

# Convert crs to lat/lon
exchange_district_4326 = exchange_district.to_crs(epsg=4326)
# extract centroid of DA
exchange_district_4326['centroid'] = exchange_district_4326.geometry.centroid

# lon/lan from centroid
exchange_district_4326['lon'] = exchange_district_4326.centroid.x
exchange_district_4326['lat'] = exchange_district_4326.centroid.y


# Convert 'lon' and 'lat' columns into Point geometry (GeoDataFrame)
gdf_points = gpd.GeoDataFrame(
    exchange_district_4326[['lon', 'lat']],  # DataFrame containing lon/lat
    geometry=gpd.points_from_xy(
        exchange_district_4326['lon'], exchange_district_4326['lat']),
    crs='EPSG:4326'  # Coordinate system for lon/lat
)


# initialize nominatim
geolocator = Nominatim(user_agent="Ayotunde_Exchange_district_map")


def reverse_geocode(lat, lon):
    '''Function to obtain address from longitude and latitude'''
    time.sleep(1)
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location and 'road' in location.raw['address']:
        return location.raw['address']['road']
    return None


exchange_district_4326['address'] = exchange_district_4326.apply(
    lambda row: reverse_geocode(row['lat'], row['lon']), axis=1)
gdf_points['address'] = gdf_points.apply(
    lambda row: reverse_geocode(row['lat'], row['lon']), axis=1)
# Add dissemination numbers to gdf_points
gdf_points = pd.merge(gdf_points, exchange_district_4326[[
                      'DAUID', 'address']], on='address', how='left')
# create plot labels
gdf_points['plot_label'] = gdf_points.apply(
    lambda row: f"{row['address']} (DAUID: {row['DAUID']})", axis=1)


# Save exchange district DA and location
# exchange_district_4326.to_csv('exchange-district-dissemination-areas.csv',
#                               columns=['DAUID', 'DGUID', 'LANDAREA', 'PRUID', 'centroid', 'lon', 'lat', 'address'])

# Plot exchange district dissemination areas
ax = exchange_district_4326['geometry'].plot(
    edgecolor='blue', figsize=(20, 18))
gdf_points.plot(ax=ax, color='red', markersize=15)

for x, y, label in zip(gdf_points.geometry.x, gdf_points.geometry.y, gdf_points['plot_label']):
    ax.text(x, y, label, fontsize=5, ha='right', va='bottom', color='black')
plt.show()
