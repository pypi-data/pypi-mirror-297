import numpy as np
import tensorflow as tf
import keras_tuner as kt
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore

# Load the preprocessed datasets
X = np.load('NPY/X-5.npy')  # Now includes close, RSI, MA, MACD, etc.
Y = np.load('NPY/Y-5.npy')

# Define the model
def build_model(hp):
    model = Sequential()
    
    # First LSTM layer with hyperparameter tuning for number of units
    model.add(LSTM(units=hp.Int('units_1', min_value=50, max_value=200, step=50), 
                   return_sequences=True, input_shape=(X.shape[1], X.shape[2])))  # Adjust input_shape for multi-features
    
    # Dropout layer with a tunable dropout rate
    model.add(Dropout(hp.Float('dropout_1', 0.2, 0.5, step=0.1)))
    
    # Second LSTM layer with hyperparameter tuning for number of units
    model.add(LSTM(units=hp.Int('units_2', min_value=50, max_value=200, step=50), 
                   return_sequences=False))
    
    # Another Dropout layer with a tunable dropout rate
    model.add(Dropout(hp.Float('dropout_2', 0.2, 0.5, step=0.1)))
    
    # Dense layer with tunable units
    model.add(Dense(units=hp.Int('dense_units', min_value=25, max_value=100, step=25)))
    
    # Output layer for predicting the next close price
    model.add(Dense(1))
    
    # Compile the model with the 'adam' optimizer and 'mean_squared_error' loss
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    return model

# Initialize the tuner
tuner = kt.RandomSearch(build_model,
                        objective='val_loss',
                        max_trials=10,  # Number of trials for hyperparameter search
                        executions_per_trial=4,  # Each trial runs 4 executions
                        directory='tuning',
                        project_name='eth_lstm_with_indicators')

# Set early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=3)

# Perform the hyperparameter search
tuner.search(X, Y, epochs=15, validation_split=0.2, callbacks=[early_stopping])

# Get the best model after hyperparameter tuning
best_model = tuner.get_best_models(num_models=1)[0]

# Print model summary
best_model.summary()

# Save the best model
best_model.save('H5/eth_lstm_model-30m.h5')
print("Hyperparameter tuning complete and best model saved.")
