import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from tensorflow import keras


# Connection to SQLite database file
conn = sqlite3.connect('api/SeniorProject.db')
df = pd.read_sql("SELECT * FROM Venue", conn)
conn.close()  # Close connection after loading data

# print(df.head())

# Date range from 2022-11-27 to 2023-03-25
start_date = datetime(2022, 11, 27)
end_date = datetime(2023, 3, 25)
date_range = pd.date_range(start=start_date, end=end_date)

# Expanding each venue with all dates in the range
df = pd.merge(
    df.assign(key=1),  # Add a temporary key for cross join
    pd.DataFrame({'Date': date_range, 'key': 1}),  # Date dataframe with the same key
    on='key'
).drop(columns=['key'])

expanded_data=df
df.drop(df['ID'], inplace=True)
print(expanded_data.head(10))

# Getting cyclical feature of date/time
expanded_data['Date'] = expanded_data['Date'].dt.dayofyear # extract day of the year
expanded_data['DateSin'] = np.sin(2 * np.pi * expanded_data['Date'] / 365.25)
expanded_data['DateCos'] = np.cos(2 * np.pi * expanded_data['Date'] / 365.25)
expanded_data = expanded_data.drop(columns='Date')

# print(expanded_data.head(10))

expanded_data.drop_duplicates(inplace=True)
expanded_data = expanded_data[['Latitude', 'Longitude', 'DateSin','DateCos']]

# print(expanded_data.head(10))

min_max_scaler = MinMaxScaler()
expanded_data[['Latitude', 'Longitude']] = min_max_scaler.fit_transform(expanded_data[['Latitude', 'Longitude']])
# print(expanded_data.head(10))

lstm_model = keras.models.load_model('models/lstm1.keras')
rnn_model = keras.models.load_model('models/rnn2.keras')


test_data = expanded_data.to_numpy()
X_test = test_data.reshape((test_data.shape[0], 1, test_data.shape[1]))

simple_rnn_predictions = rnn_model.predict(X_test)

# Preparing Robust Scaler##################
###########################################
###########################################
robust_scaler = RobustScaler()

df1 = pd.read_csv('../Database/database-csv/co2-csv/output_concatenated.csv')
df1['CO2'] = robust_scaler.fit_transform(df1[['CO2']])

simple_rnn_predictions = robust_scaler.inverse_transform(simple_rnn_predictions)

print(simple_rnn_predictions)

# saving the new data

# Ensure the predictions array has the same length as the expanded_data DataFrame
if len(simple_rnn_predictions) == len(df):
    # Add predictions as a new column to expanded_data DataFrame
    df['CO2'] = simple_rnn_predictions.astype(np.float32)

    # Save the DataFrame with the new column to a CSV file
    output_file_path = 'venue_co2.csv'
    df.to_csv(output_file_path, index=False)

    print(f"Data saved successfully to {output_file_path}")
else:
    print("Error: The length of predictions does not match the number of rows in expanded_data.")