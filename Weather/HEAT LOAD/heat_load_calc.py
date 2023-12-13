import os
import pandas as pd
from sklearn.preprocessing import normalize

# Assuming your CSV files are in a folder named 'data_folder'
folder_path = "SH"
column_name = "space_heat_load_in_MW"

# List of periods with start and end rows
periods = {
	"1":  [2, 2997],
	"2":  [2998, 5665],
	"3":  [5666, 8641],
	"4":  [8642, 11521],
	"5":  [11522, 14497],
	"6":  [14498, 17377],
	"7":  [17378, 20353],
	"8":  [20354, 23329],
	"9":  [23330, 26209],
	"10": [26210, 29185],
	"11": [29186, 32065],
	"12": [32066, 35041]
}
# Read ags2nuts3.csv to map file_number to nuts3 number
ags2nuts3_df = pd.read_csv('ags2nuts3.csv')  # Replace 'ags2nuts3.csv' with the correct path
file_number_map = dict(zip(ags2nuts3_df['AGS'], ags2nuts3_df['NUTS3']))

def calculate_averages(file_path, period, column_name):
	df = pd.read_csv(file_path)  # Read the CSV file
	start_row, end_row = periods[period]

	# Slice the dataframe based on start and end rows for the period
	period_data = df.iloc[start_row - 1:end_row]  # Adjust for 0-based indexing

	# Calculate the average of values in the specified column
	average_value = period_data[column_name].mean()
	return average_value

# Create a dictionary to store averages
averages_dict = {}

# Iterate through each CSV file and calculate averages for each period
for file_name in os.listdir(folder_path):
	file_path = os.path.join(folder_path, file_name)
	if file_name.endswith('.csv'):
		# Extracting the number from the filename
		file_number = int(file_name.split('=')[-1].split('.')[0])
		
		if file_number in file_number_map:
			nuts3_number = file_number_map[file_number]
			
			averages_dict[nuts3_number] = {}
			for period in periods:
				average = calculate_averages(file_path, period, column_name)
				averages_dict[nuts3_number][f"Period {period}"] = average

# Convert the dictionary to a DataFrame
averages_df = pd.DataFrame.from_dict(averages_dict, orient='index')
averages_df.index.name = 'nuts3'  # Set the index name

print(averages_df)
# Normalize the dataframe to get relative averages
normalized_df = pd.DataFrame(normalize(averages_df, norm='l1'), columns=averages_df.columns, index=averages_df.index)

# Write the DataFrame to a CSV file
output_file = 'SH_profile.csv'
normalized_df.to_csv(output_file)
print(f"Relative average results saved to '{output_file}'")