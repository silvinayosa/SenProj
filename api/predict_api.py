from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from keras import models, layers
# from keras.models import Sequential
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import SimpleRNN, LSTM, Dense
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to the SQLite database
def connect_to_db():
    conn = sqlite3.connect("SeniorProject.db", check_same_thread=False)
    return conn


# http://127.0.0.1:5001/process-data
@app.route('/process-data', methods=['GET'])
def process_data():
    # Connect to the database
    conn = connect_to_db()

    # Query to retrieve data
    query = "SELECT DateTime, Latitude, Longitude, Co2Emission FROM estimated_co2"
    data = pd.read_sql(query, con=conn)
    
    # Close the connection
    conn.close()

    # Convert the DateTime column to datetime
    data['DateTime'] = pd.to_datetime(data['DateTime'], errors='coerce')
    
    # Drop rows where DateTime conversion failed
    data = data.dropna(subset=['DateTime'])
    
    # Convert the DateTime column to ordinal
    data['DateTime'] = data['DateTime'].apply(lambda x: x.toordinal())

    # Normalize the data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    X = scaled_data[:, :-1]
    y = scaled_data[:, -1]
    X = X.reshape((X.shape[0], 1, X.shape[1]))

    # Build and train the RNN model
    rnn_model = keras.Sequential([
        keras.layers.SimpleRNN(50, activation='relu', input_shape=(X.shape[1], X.shape[2])),
        keras.layers.Dense(1)
    ])
    rnn_model.compile(optimizer='adam', loss='mse')
    rnn_model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

    # Build and train the LSTM model
    lstm_model = keras.Sequential([
        keras.layers.LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])),
        keras.layers.Dense(1)
    ])
    lstm_model.compile(optimizer='adam', loss='mse')
    lstm_model.fit(X, y, epochs=50, batch_size=16, validation_split=0.2, verbose=1)

    # Make predictions with both models
    actual_co2 = data['Co2Emission'].values
    rnn_predictions = rnn_model.predict(X).flatten()
    lstm_predictions = lstm_model.predict(X).flatten()

    # Inverse transform the predictions to original scale
    rnn_scaled_data = np.copy(scaled_data)
    lstm_scaled_data = np.copy(scaled_data)
    rnn_scaled_data[:, -1] = rnn_predictions
    lstm_scaled_data[:, -1] = lstm_predictions
    rnn_predictions = scaler.inverse_transform(rnn_scaled_data)[:, -1]
    lstm_predictions = scaler.inverse_transform(lstm_scaled_data)[:, -1]

    # Convert DateTime back to datetime format
    data['DateTime'] = pd.to_datetime(data['DateTime'], origin='ordinal', unit='D')
    data_grouped = data.groupby('DateTime').mean().reset_index()
    dates = data_grouped['DateTime']
    actual_co2_grouped = data_grouped['Co2Emission']

    # Group predictions by date
    rnn_predictions_grouped = []
    lstm_predictions_grouped = []
    for date in dates:
        mask = data['DateTime'] == date
        rnn_predictions_grouped.append(rnn_predictions[mask].mean())
        lstm_predictions_grouped.append(lstm_predictions[mask].mean())

    # Smooth the data for better visualization
    def smooth_data(data, window_size=3):
        return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

    smooth_actual_co2 = smooth_data(actual_co2_grouped)
    smooth_rnn_predictions = smooth_data(rnn_predictions_grouped)
    smooth_lstm_predictions = smooth_data(lstm_predictions_grouped)
    smooth_dates = dates[:len(smooth_actual_co2)]

    # Return the processed data as a JSON response
    return jsonify({
        "dates": smooth_dates.dt.strftime('%Y-%m-%d').tolist(),
        "actual_co2": smooth_actual_co2.tolist(),
        "rnn_predictions": smooth_rnn_predictions.tolist(),
        "lstm_predictions": smooth_lstm_predictions.tolist()
    })

if __name__ == '__main__':
    app.run(port=5001, debug=True)


# myenv\Scripts\activate