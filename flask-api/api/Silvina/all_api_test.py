import pandas as pd
import numpy as np
import sqlite3
from pymoo.algorithms.moo.spea2 import SPEA2
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem
from datetime import datetime, timedelta
import joblib
from tensorflow import keras
from tqdm import tqdm
import os
import warnings

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Suppress sklearn warnings
warnings.filterwarnings("ignore", category=UserWarning)


def connect_to_db():
    conn = sqlite3.connect("../database/SeniorProject.db", check_same_thread=False)
    return conn

city_coordinates = {
    "Saskatchewan Province": {"lat_min": 49.000000, "lat_max": 60.000000, "lon_min": -110.000000, "lon_max": -101.000000},
    "Prince Edward Island": {"lat_min": 45.948493, "lat_max": 47.072784, "lon_min": -64.424743, "lon_max": -62.023504},
    "Ontario": {"lat_min": 41.676555, "lat_max": 56.850102, "lon_min": -95.156227, "lon_max": -74.320860},
    "Nova Scotia": {"lat_min": 43.375111, "lat_max": 47.030530, "lon_min": -66.418161, "lon_max": -59.726333},
    "Alberta": {"lat_min": 49.000000, "lat_max": 60.000000, "lon_min": -120.000000, "lon_max": -110.000000},
    "British Columbia": {"lat_min": 48.308978, "lat_max": 60.000000, "lon_min": -139.041853, "lon_max": -114.039580},
    "Manitoba": {"lat_min": 49.000000, "lat_max": 60.000000, "lon_min": -102.000000, "lon_max": -95.000000},
    "Newfoundland and Labrador": {"lat_min": 46.559847, "lat_max": 60.000000, "lon_min": -67.800000, "lon_max": -52.616667},
    "New Brunswick": {"lat_min": 44.501873, "lat_max": 48.070121, "lon_min": -69.065808, "lon_max": -63.664500},
    "Quebec": {"lat_min": 45.000000, "lat_max": 62.583446, "lon_min": -79.762590, "lon_max": -57.100000}
}

# Load the Keras models
lstm_model = keras.models.load_model('./models/lstm1.keras')
rnn_model = keras.models.load_model('./models/rnn2.keras')

# Load the saved scalers
min_max_scaler = joblib.load('./models/latitude_longitude_scaler.pkl')
co2_scaler = joblib.load('./models/co2_scaler.pkl')


try:
    # Get the data from the request
    # data = request.get_json()
    # Extract selected city and days to predict
    city_name = 'Manitoba'
    days_to_predict = 3
    datetime_str = '2023-06-23'  # Actual code: data.get('datetime')
    model_name = 'LSTM'

    # Validate city and model name
    if city_name not in city_coordinates:
        print({"error": "Invalid city selected"}), 400
    if model_name not in ['LSTM', 'RNN']:
        print({"error": "Invalid model selected"}), 400

    # Get province boundaries
    lat_min = city_coordinates[city_name]['lat_min']
    lat_max = city_coordinates[city_name]['lat_max']
    lon_min = city_coordinates[city_name]['lon_min']
    lon_max = city_coordinates[city_name]['lon_max']

    # Connect to the database and retrieve venue lat/lon within the province
    conn = connect_to_db()
    query = f"""
        SELECT Latitude, Longitude 
        FROM venue 
        WHERE Latitude BETWEEN {lat_min} AND {lat_max} 
        AND Longitude BETWEEN {lon_min} AND {lon_max}
    """
    venues = pd.read_sql_query(query, conn)

    if venues.empty:
        print({"error": "No venues found in the selected province"}), 404

    # Prepare for predictions
    start_date = datetime.strptime(datetime_str, "%Y-%m-%d")
    all_predictions = []
    
    total_tasks = len(venues) * days_to_predict
    progress_bar = tqdm(total=total_tasks, desc="Predicting CO2 emissions", unit="task")


    for index, row in venues.iterrows():
        original_latitude = row['Latitude']
        original_longitude = row['Longitude']

        # Normalize the Latitude and Longitude
        latitude, longitude = min_max_scaler.transform([[original_latitude, original_longitude]])[0]

        province_predictions = []
        
        for i in range(days_to_predict):
            # Calculate the date for the prediction
            current_date = start_date + timedelta(days=i)
            day_of_year = current_date.timetuple().tm_yday

            # Cyclical transformation for date
            date_sin = np.sin(2 * np.pi * day_of_year / 365.25)
            date_cos = np.cos(2 * np.pi * day_of_year / 365.25)

            # Combine features into a single array
            features = np.array([[latitude, longitude, date_sin, date_cos]])

            # Reshape the input data to match the model's input shape
            features_array = features.reshape((features.shape[0], 1, features.shape[1]))

            # Choose the correct model for prediction
            if model_name == 'LSTM':
                prediction = lstm_model.predict(features_array)
            else:  # model_name == 'RNN'
                prediction = rnn_model.predict(features_array)

            # Perform inverse normalization on the predicted CO2 value
            co2_emission_scaled = float(prediction[0][0])
            co2_emission = co2_scaler.inverse_transform([[co2_emission_scaled]])[0][0]

            province_predictions.append(co2_emission)
            
            progress_bar.update(1)


        # Calculate the mean prediction for this venue
        mean_prediction = np.mean(province_predictions)
        all_predictions.append(mean_prediction)
        
    progress_bar.close()

    # Calculate the overall mean for the province
    overall_mean_co2 = np.mean(all_predictions)

    print({
        "mean_CO2_emission": overall_mean_co2,
        "days_predicted": days_to_predict
    })

except Exception as e:
    # Return error message if something goes wrong
    print({"error": str(e)}), 500