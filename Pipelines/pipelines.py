import json

file = "merger/IGGIELGN/data/IGGIELGN_PipeSegments.geojson"

with open(file, 'r', encoding = 'utf-8') as f:
	pipeData = json.load(f)

finalData = []

for pipe in pipeData["features"]:
	props = pipe["properties"]
	
	if (props["country_code"][0] != "DE" and props["country_code"][1] != "DE"): continue # If the pipe doesn't have anything to do with Germany, don't include it
	
	finalData.append(pipe)

with open('germanPipes.json', 'w') as json_file:
    json.dump(finalData, json_file, indent = 4)