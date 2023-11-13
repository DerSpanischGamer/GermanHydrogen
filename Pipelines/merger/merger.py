import json

archivos = ["EMAP_raw/data/EMAP_PipeSegments.geojson", "IGGI/data/IGGI_PipeSegments.geojson", "INET_Filled/data/INET_PipeSegments.geojson", "LKD_Raw/data/LKD_Raw_PipeSegments.geojson", "IGGIELGN/data/IGGIELGN_PipeSegments.geojson"]

finalGermanList = []

# Check variables
names = []
originalCoordinate = []

for a in archivos:
	temp = []
	
	with open(a, 'r', encoding = "utf-8") as file:
		temp = json.load(file)
	
	for linea in temp["features"]:
		if (linea["properties"]["name"] in names): continue # Use the coordinates of a pipe as the identifier
		if (linea["properties"]["country_code"][0] != "DE" and linea["properties"]["country_code"][1] != "DE"): continue
		if (linea["geometry"]["coordinates"] in originalCoordinate): continue
		
		originalCoordinate.append(linea["geometry"]["coordinates"])
		names.append(linea["properties"]["name"])
		finalGermanList.append(linea)

print(len(names), "elements merged")

with open('germanPipesMerged.json', 'w') as json_file:
    json.dump(finalGermanList, json_file, indent = 4)