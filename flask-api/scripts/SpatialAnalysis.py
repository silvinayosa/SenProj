
import pandas as pd
import numpy as np
import sqlite3
# connect db
conn = sqlite3.connect("SeniorProject.db")
print("Database is connect successfully!")
cursor = conn.cursor()

co2_data = pd.read_sql_query("SELECT * FROM estimated_co2", conn)
venue_data = pd.read_sql_query("SELECT * FROM venue", conn)
# Load the datasets
# venue_data = pd.read_csv('venue.csv')
# co2_data = pd.read_csv('co2.csv')

# Ensure 'Time' column is in datetime format
co2_data['DateTime'] = pd.to_datetime(co2_data['DateTime'])
print("ok")

def idw_interpolation(x, y, z, xi, yi, power=1.0):
    """
    Perform Inverse Distance Weighting (IDW) interpolation.

    Parameters:
    - x, y: Arrays of x and y coordinates of the data points.
    - z: Array of values at the data points.
    - xi, yi: Coordinates where to interpolate.
    - power: Power parameter for the IDW.

    Returns:
    - Interpolated value at the xi, yi location.
    """
    distances = np.sqrt((x - xi)**2 + (y - yi)**2)
    distances = np.where(distances == 0, 1e-10, distances)
    weights = 1.0 / distances**power
    weighted_sum = np.sum(weights * z)
    sum_of_weights = np.sum(weights)
    return weighted_sum / sum_of_weights if sum_of_weights != 0 else 0

# Get unique dates from the 'co2_data'
unique_dates = co2_data['DateTime'].dt.date.unique()

# Initialize a list to store the results
results = []
print("ok")

# Perform IDW interpolation for each date and each venue location
for date in unique_dates:
    # Filter the CO2 data for the current date
    date_filter = co2_data['DateTime'].dt.date == date
    x = co2_data.loc[date_filter, 'Longitude'].values
    y = co2_data.loc[date_filter, 'Latitude'].values
    z = co2_data.loc[date_filter, 'Co2Emission'].values

    # Perform interpolation for each venue
    for index, row in venue_data.iterrows():
        interpolated_value = idw_interpolation(x, y, z, row['Longitude'], row['Latitude'])
        results.append({
            'Latitude': row['Latitude'],
            'Longitude': row['Longitude'],
            'DateTime': pd.to_datetime(date),
            'Co2Emission': interpolated_value
        })

# Create a DataFrame from the results
interpolated_df = pd.DataFrame(results)

# Save the result to a new CSV file
interpolated_df.to_csv('estimated_data_sorted_by_date.csv', index=False)


cursor.close()
conn.close()