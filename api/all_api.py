from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow import keras
from datetime import datetime, timedelta
import joblib  # For loading the scalers


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the Keras models
lstm_model = keras.models.load_model('model/lstm1.keras')
rnn_model = keras.models.load_model('model/rnn2.keras')

# Load the saved scalers
min_max_scaler = joblib.load('model/latitude_longitude_scaler.pkl')
co2_scaler = joblib.load('model/co2_scaler.pkl')

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


def connect_to_db():
    conn = sqlite3.connect("SeniorProject.db", check_same_thread=False)
    return conn


@app.route('/get_cost_by_location', methods=['GET'])
def get_cost_by_location():
    location = request.args.get('location')
    
   
    if location not in city_coordinates:
        return jsonify({"error": "Invalid location"}), 400
    
    
    lat_min = city_coordinates[location]['lat_min']
    lat_max = city_coordinates[location]['lat_max']
    lon_min = city_coordinates[location]['lon_min']
    lon_max = city_coordinates[location]['lon_max']
    
    conn = connect_to_db()
    cursor = conn.cursor()
    
    
    query = """
        SELECT Facility_Name, Price 
        FROM cost 
        WHERE Latitude BETWEEN ? AND ? 
        AND Longitude BETWEEN ? AND ?
    """
    
    cursor.execute(query, (lat_min, lat_max, lon_min, lon_max))
    results = cursor.fetchall()
    
    
    if results:
        return jsonify([{"Facility_Name": row[0], "Price": row[1]} for row in results])
    else:
        return jsonify({"message": "No facilities found in this location"}), 404



@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the request
        data = request.get_json()

        # Extract selected city and days to predict
        city_name = data.get('city_name')
        days_to_predict = int(data.get('days'))
        datetime_str = data.get('datetime')
        model_name = data.get('model_name')

        # Validate city and model name
        if city_name not in city_coordinates:
            return jsonify({"error": "Invalid city selected"}), 400
        if model_name not in ['LSTM', 'RNN']:
            return jsonify({"error": "Invalid model selected"}), 400

        # Get latitude and longitude for the selected city
        # Get latitude and longitude for the selected city (use the center of the lat/lon range)
        lat_min = city_coordinates[city_name]['lat_min']
        lat_max = city_coordinates[city_name]['lat_max']
        lon_min = city_coordinates[city_name]['lon_min']
        lon_max = city_coordinates[city_name]['lon_max']

        # Calculate the center of the latitude and longitude range
        latitude = (lat_min + lat_max) / 2
        longitude = (lon_min + lon_max) / 2


        # Normalize the Latitude and Longitude using the loaded scaler
        latitude, longitude = min_max_scaler.transform([[latitude, longitude]])[0]

        # Convert Start Date to a datetime object
        start_date = datetime.strptime(datetime_str, "%Y-%m-%d")

        predictions = []

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

            # Append the prediction for the current date
            predictions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "CO2Emission": co2_emission
            })

        # Return predictions for all requested days
        return jsonify({"predictions": predictions})

    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


# CO2 prediction api :(POST) http://127.0.0.1:5000/predict
# Cost location api :(GET) http://127.0.0.1:5000/get_cost_by_location?location=Ontario