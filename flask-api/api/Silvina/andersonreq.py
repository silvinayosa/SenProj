import pandas as pd

# Load the dataset
df = pd.read_csv('../Database/database-csv/co2-csv/venue_co2.csv')

# Ensure the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

# Create an empty dictionary to hold the subsets
subset_data = {}

# Loop through each province, create subsets, and save to CSV files
for province in df['Prov_Terr'].unique():
    # Filter by province
    province_data = df[df['Prov_Terr'] == province]
    
    # Sort by date
    province_data = province_data.sort_values(by='Date')
    
    # Store the subset in the dictionary with a descriptive key
    var_name = f"{province.upper()}"
    subset_data[var_name] = province_data
    
    # Save each province's data to a CSV file
    filename = f"{var_name}.csv"
    province_data.to_csv(filename, index=False)
    
    print(f"Data saved to {filename}")

# subset_data now contains each subset by province
