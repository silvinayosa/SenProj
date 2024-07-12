from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, LSTM, Dense

app = Flask(__name__)
CORS(app)

@app.route('/process-data', methods=['GET'])
def process_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-05-01', end='2023-05-10', freq='D')
    latitudes = np.random.uniform(-90, 90, size=len(dates) * 3)
    longitudes = np.random.uniform(-180, 180, size=len(dates) * 3)
    co2_emissions = np.random.uniform(350, 450, size=len(dates) * 3)

    data = pd.DataFrame({
        'Date': np.tile(dates, 3),
        'Latitude': latitudes,
        'Longitude': longitudes,
        'CO2_Emissions': co2_emissions
    })

    data['Date'] = data['Date'].map(pd.Timestamp.toordinal)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    X = scaled_data[:, :-1]
    y = scaled_data[:, -1]
    X = X.reshape((X.shape[0], 1, X.shape[1]))

    rnn_model = Sequential()
    rnn_model.add(SimpleRNN(50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
    rnn_model.add(Dense(1))
    rnn_model.compile(optimizer='adam', loss='mse')
    rnn_model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

    lstm_model = Sequential()
    lstm_model.add(LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
    lstm_model.add(Dense(1))
    lstm_model.compile(optimizer='adam', loss='mse')
    lstm_model.fit(X, y, epochs=50, batch_size=16, validation_split=0.2, verbose=1)

    actual_co2 = data['CO2_Emissions'].values
    rnn_predictions = rnn_model.predict(X).flatten()
    lstm_predictions = lstm_model.predict(X).flatten()

    rnn_scaled_data = np.copy(scaled_data)
    lstm_scaled_data = np.copy(scaled_data)
    rnn_scaled_data[:, -1] = rnn_predictions
    lstm_scaled_data[:, -1] = lstm_predictions
    rnn_predictions = scaler.inverse_transform(rnn_scaled_data)[:, -1]
    lstm_predictions = scaler.inverse_transform(lstm_scaled_data)[:, -1]

    data['Date'] = pd.to_datetime(data['Date'])
    data_grouped = data.groupby('Date').mean().reset_index()
    dates = data_grouped['Date']
    actual_co2_grouped = data_grouped['CO2_Emissions']

    rnn_predictions_grouped = []
    lstm_predictions_grouped = []
    for date in dates:
        mask = data['Date'] == date
        rnn_predictions_grouped.append(rnn_predictions[mask].mean())
        lstm_predictions_grouped.append(lstm_predictions[mask].mean())

    def smooth_data(data, window_size=3):
        return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

    smooth_actual_co2 = smooth_data(actual_co2_grouped)
    smooth_rnn_predictions = smooth_data(rnn_predictions_grouped)
    smooth_lstm_predictions = smooth_data(lstm_predictions_grouped)
    smooth_dates = dates[:len(smooth_actual_co2)]

    return jsonify({
        "dates": smooth_dates.dt.strftime('%Y-%m-%d').tolist(),
        "actual_co2": smooth_actual_co2.tolist(),
        "rnn_predictions": smooth_rnn_predictions.tolist(),
        "lstm_predictions": smooth_lstm_predictions.tolist()
    })

if __name__ == '__main__':
    app.run(port=5001, debug=True)
