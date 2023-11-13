import json

file = "data/IGGIELGN_Storages.geojson"

with open(file, 'r', encoding = 'utf-8') as f:
	stoData = json.load(f)


finalSto = []
for sto in stoData["features"]:
	if (sto["properties"]["country_code"] != "DE"): continue
	
	finalSto.append(sto)

with open('germanStorages.json', 'w') as json_file:
    json.dump(finalSto, json_file, indent = 4)