import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load the 5-minute interval data
data = pd.read_csv('CSV/eth_price_data_5m.csv')
data.set_index('timestamp', inplace=True)

# Normalize the 'close' price using MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data['close'].values.reshape(-1, 1))

# Save the scaler for future inverse transformation
joblib.dump(scaler, 'scaler-h.pkl')

# Create the time-series dataset
def create_dataset(data, time_step=48):  # Adjusted to 48 time steps (4 hours of past data)
    X, Y = [], []
    for i in range(len(data)-time_step-1):
        X.append(data[i:(i+time_step), 0])  # X is the past 48 data points
        Y.append(data[i + time_step, 0])    # Y is the next price after the past 48 data points (5-minute steps)
    return np.array(X), np.array(Y)

# Using 48 time steps (representing 4 hours of past data for prediction)
time_step = 48
X, Y = create_dataset(scaled_data, time_step)

# Reshape the input data to be in 3D for LSTM [samples, time steps, features]
X = X.reshape(X.shape[0], X.shape[1], 1)

# Save the processed datasets for model training
np.save('NPY/X-5.npy', X)
np.save('NPY/Y-5.npy', Y)

print("Preprocessing complete and data saved.")
