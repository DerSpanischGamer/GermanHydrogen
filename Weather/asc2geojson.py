import numpy as np
import json
from pyproj import Proj, transform

# THIS CODE ACCEPTS DATA FROM THE GERMAN NATIONAL WEATHER ENTITY : https://www.dwd.de/EN/ourservices/solarenergy/maps_globalradiation_sum_new.html AND ALL THE INFORMATION REMOVED, EXCEPT THE NCOLS TO NODATA LINES

for m in range(1, 13):
	# Read the ASC file and extract header information
	inputFile = f"INPUT/grids_germany_monthly_radiation_direct_2022{m:02}.asc"
	with open(inputFile, 'r') as file:
		header = [next(file).strip().split() for _ in range(6)]

	# Extract header information
	ncols = int(header[0][1])
	nrows = int(header[1][1])
	xllcorner = float(header[2][1])
	yllcorner = float(header[3][1])
	cellsize = float(header[4][1])
	nodata_value = float(header[5][1])

	# Read the data as a numpy array
	data = np.loadtxt(inputFile, skiprows=6)

	# Create a grid of coordinates based on the header information
	x = np.arange(xllcorner, xllcorner + (ncols * cellsize), cellsize)
	y = np.arange(yllcorner + (nrows * cellsize), yllcorner, -cellsize) # DEAR FUTURE READER : I DON'T KNOW WHY , BUT THE Y-AXIS IS FLIPPED
	xx, yy = np.meshgrid(x, y)
	
	# Create GeoJSON-like representation of the grid
	features = []
	for i in range(nrows):
		for j in range(ncols):
			if data[i][j] != nodata_value:
				feature = {
					'type': 'Feature',
					'geometry': {
						'type': 'Point',
						'coordinates': [xx[i][j], yy[i][j]] # Coordinates of the point
					},
					'properties': {
						'value': float(data[i][j])  # Solar irradiation
					}
				}
				features.append(feature)

	# Create a GeoJSON-like object
	geojson_data = {
		'type': 'FeatureCollection',
		'features': features
	}

	# Write the GeoJSON-like data to a file
	outputFile = f"OUTPUT/radiation_2022_{m:02}.geojson"
	with open(outputFile, 'w') as file:
		json.dump(geojson_data, file, indent = 4)