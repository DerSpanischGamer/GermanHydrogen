import csv
import json
import sys

def csv_to_dict(input_csv):
	with open(input_csv, 'r') as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter = ';')
		data = list(csv_reader)
	return data

def dict_to_json(data, output_json):
	with open(output_json, 'w') as json_file:
		json.dump(data, json_file, indent=4)

if len(sys.argv) != 3:
	print("Usage: python csv_to_json.py input.csv output.json")
	quit()

input_csv = sys.argv[1]
output_json = sys.argv[2]

data = csv_to_dict(input_csv)
dict_to_json(data, output_json)

print(f"Conversion successful. Data saved to {output_json}.")