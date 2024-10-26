from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow import keras
from datetime import datetime, timedelta
import joblib  
import pandas as pd
import os
import json

app = Flask(__name__)
CORS(app)

# Load the Keras models
lstm_model = tf.keras.models.load_model('./models/lstm1.keras')
rnn_model = tf.keras.models.load_model('./models/rnn2.keras')

# Load the saved scalers
min_max_scaler = joblib.load('./models/latitude_longitude_scaler.pkl')
co2_scaler = joblib.load('./models/co2_scaler.pkl')

# City latitude and longitude mapping
city_coordinates = {
    "Saskatchewan Province": (55.000000, -106.000000),
    "Prince Edward Island": (46.250000, -63.000000),
    "Ontario": (50.000000, -85.000000),
    "Nova Scotia": (45.000000, -63.000000),
    "Alberta": (55.000000, -115.000000),
    "British Columbia": (53.726669, -127.647621),
    "Manitoba": (56.415211, -98.739075),
    "Newfoundland and Labrador": (53.135509, -57.660435),
    "New Brunswick": (46.498390, -66.159668),
    "Quebec": (53.000000, -70.000000)
}

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
        latitude, longitude = city_coordinates[city_name]

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
    app.run(debug=True,port=8080)
