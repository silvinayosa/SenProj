import pandas as pd
import glob
import os

# Path pattern for the CSV files
file_pattern = "../Database/database-csv/co2-avg/*.csv"  # Adjust this pattern if files are stored in a specific folder, e.g., "output/*.csv"

# Initialize a dictionary to store data from each file
dataframes = {}

# Dictionary to store average data
avg = []

# Loop through each CSV file that matches the pattern
for file_path in glob.glob(file_pattern):
    # Extract filename without the path and extension
    file_name = os.path.basename(file_path).split('.')[0]  # Remove .csv extension and path
    
    # Check if filename has the expected underscore pattern
    if '_' in file_name:
        province, month = file_name.split('_', 1)  # Split only on the first underscore
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Store the DataFrame in the dictionary with a descriptive key
        dataframes[file_name] = df

        # Calculate the average CO2 for the month in this province
        avg_co2 = df['CO2'].mean()
        # print(province,month,avg_co2)
        # Append the result to avg_data as a dictionary
        avg.append([province, month, avg_co2])

avg = pd.DataFrame(avg, columns=['Province', 'Month', 'CO2'])
# print(avg)

avg.sort_values(['Province'], inplace=True, ignore_index=True)
# print(avg)

avg.to_csv('avgCO2_Province_Month.csv', index=False)