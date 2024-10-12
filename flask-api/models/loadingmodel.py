
import os

import tensorflow as tf
from tensorflow import keras
import joblib  

print(tf.version.VERSION) # min. version 2.17.0

lstm = tf.keras.models.load_model('model/lstm1.keras')
rnn = tf.keras.models.load_model('model/rnn2.keras')

"""Process Data"""

# Load the necessary modules
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
df = pd.read_csv('./csv/estimated_co2.csv')

# checking how the dataset looks
print(df.head(10))

# Checking all the columns & datatype in the dataset
print(df.info())

# Convert the DateTime column to Cyclical Features of the year
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['DateTime'] = df['DateTime'].dt.dayofyear # extract day of the year
df['DateSin'] = np.sin(2 * np.pi * df['DateTime'] / 365.25)
df['DateCos'] = np.cos(2 * np.pi * df['DateTime'] / 365.25)
df = df.drop(columns='DateTime')
print(df)

# deleting messy data
df.dropna(inplace=True) # delete null if any
df.drop_duplicates(inplace=True) # delete duplicated
print(df.info())

df.reset_index(drop = True, inplace = True)
print(df.info())

# Normalize the data
# As we have many outliers for co2emission value, we will use robust scaling
from sklearn.preprocessing import RobustScaler

min_max_scaler = MinMaxScaler()
df[['Latitude', 'Longitude']] = min_max_scaler.fit_transform(df[['Latitude', 'Longitude']])

# save MinMaxScaler
joblib.dump(min_max_scaler, 'latitude_longitude_scaler.pkl')

# 2. Apply RobustScaler to Co2Emission
robust_scaler = RobustScaler()
df['Co2Emission'] = robust_scaler.fit_transform(df[['Co2Emission']])

# save RobustScaler
joblib.dump(robust_scaler, 'co2_scaler.pkl')

# Display the final DataFrame
print(df)

# dividing data into features and label
# dividing dataset into training and testing dataset
# reshaping data

from sklearn.model_selection import train_test_split

y = df['Co2Emission']
X = df.drop(columns= 'Co2Emission')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()

X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# Make predictions with the SimpleRNN model
simple_rnn_predictions = rnn.predict(X_test)
lstm_predictions = lstm.predict(X_test)

# Inverse transform the predictions (back to original scale)
simple_rnn_predictions = robust_scaler.inverse_transform(simple_rnn_predictions)
lstm_predictions = robust_scaler.inverse_transform(lstm_predictions)

# Inverse transform y_test as well for comparison
y_test_inverse = robust_scaler.inverse_transform(y_test.to_numpy().reshape(-1, 1))

from sklearn.metrics import mean_squared_error, mean_absolute_error

# Evaluate SimpleRNN model
simple_rnn_mse = mean_squared_error(y_test_inverse, simple_rnn_predictions)
simple_rnn_mae = mean_absolute_error(y_test_inverse, simple_rnn_predictions)

# Evaluate LSTM model
lstm_mse = mean_squared_error(y_test_inverse, lstm_predictions)
lstm_mae = mean_absolute_error(y_test_inverse, lstm_predictions)

print("SimpleRNN MSE:", simple_rnn_mse)
print("SimpleRNN MAE:", simple_rnn_mae)

print("LSTM MSE:", lstm_mse)
print("LSTM MAE:", lstm_mae)

print("Comparison of RNN Models:")
print(f"SimpleRNN MSE: {simple_rnn_mse:.4f}, MAE: {simple_rnn_mae:.4f}")
print(f"LSTM MSE: {lstm_mse:.4f}, MAE: {lstm_mae:.4f}")

if simple_rnn_mse < lstm_mse:
    print("SimpleRNN performed better.")
else:
    print("LSTM performed better.")