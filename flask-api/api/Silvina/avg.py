import pandas as pd

df = pd.read_csv('../Database/database-csv/co2-csv/venue_co2.csv')

df['Date'] = pd.to_datetime(df['Date'])

# Create an empty dictionary to hold the subsets
subset_data = {}

# Loop through each province and month, create subsets, and save to CSV files
for province in df['Prov_Terr'].unique():
    province_data = df[df['Prov_Terr'] == province]  # Filter by province
    
    for month in province_data['Date'].dt.month.unique():
        month_data = province_data[province_data['Date'].dt.month == month]  # Filter by month
        
        # Create a variable name dynamically
        var_name = f"{province.upper()}_{pd.to_datetime(month, format='%m').strftime('%B')}"
        
        # Store the subset in the dictionary
        subset_data[var_name] = month_data
        
        # Save to CSV
        filename = f"{var_name}.csv"
        month_data.to_csv(filename, index=False)
        
        print(f"Data saved to {filename}")

# subset_data now contains each subset by province and month