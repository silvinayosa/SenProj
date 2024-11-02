import pandas as pd
import json
from shapely.geometry import Point, mapping

# Load the CSV file
df = pd.read_csv('../Database/database-csv/co2-csv/venue_co2.csv')

# Ensure the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Convert to specified format

df = df[df['Prov_Terr']=='qc']
print(df)

# Initialize an empty dictionary to store GeoJSON data
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

# Loop through each row to create GeoJSON features
for _, row in df.iterrows():
    feature = {
        "type": "Feature",
        "properties": {
            "measurement": "CO2",
            "tag": row['Facility_Name'],
            "type": row['ODRSF_facility_type'],
            "province": row['Prov_Terr'],
            "field": [row['CO2']],
            "time": row['Date']
        },
        "geometry": {
            "type": "Point",
            "coordinates": [row['Longitude'], row['Latitude']]
        }
    }
    
    # Append each feature to the GeoJSON features list
    geojson_data["features"].append(feature)

# Save the GeoJSON data to a file
output_file = "province_co2_data.geojson"
with open(output_file, "w") as f:
    json.dump(geojson_data, f, indent=2)

print(f"GeoJSON data saved to {output_file}")
