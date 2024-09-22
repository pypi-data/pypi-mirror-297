import os
from pathlib import Path
import ccxt
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib

# Load the model and scaler
base_dir = Path(__file__).resolve().parent
model_path = os.path.join(base_dir, 'eth_lstm_model-30m.h5')
scaler_path = os.path.join(base_dir, 'scaler-h.pkl')

model = tf.keras.models.load_model(model_path)  # Load the model
scaler = joblib.load(scaler_path)  # Load the scaler

# Initialize Binance API
binance = ccxt.binance()

# Function to fetch the current price
def fetch_current_price(symbol):
    try:
        ticker = binance.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"Error fetching current price: {str(e)}")
        return None

# Function to fetch historical OHLCV data
def fetch_ohlcv(symbol, timeframe='5m', limit=500):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching OHLCV data: {str(e)}")
        return None

# Function to fetch the latest 48 close prices in real-time (5-minute intervals)
def fetch_latest_close_data(symbol='ETH/USDT', timeframe='5m', limit=288):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        close_prices = np.array([x[4] for x in ohlcv])  # Extract close prices
        return close_prices  # Return the close prices
    except Exception as e:
        print(f"Error fetching latest close data: {str(e)}")
        return None

# Function to calculate support and resistance levels
def calculate_support_resistance(ohlcv_df):
    support_level = ohlcv_df['low'].min()  # Simplistic approach; for a real strategy, use more advanced methods
    resistance_level = ohlcv_df['high'].max()
    return support_level, resistance_level

# Function to calculate and display predictions and related stats
def predict_30m_ahead():
    symbol = 'ETH/USDT'

    # Fetch the current price
    current_price = fetch_current_price(symbol)
    if current_price is None:
        print("Unable to fetch the current price. Exiting.")
        return
    
    # Fetch the latest 48 close prices (5-minute intervals)
    latest_close_data = fetch_latest_close_data(symbol=symbol, timeframe='5m', limit=48)
    
    if latest_close_data is None or len(latest_close_data) < 48:
        print('Not enough data to make a prediction. Exiting.')
        return
    
    # Preprocess the data (scale the latest close prices using the same scaler)
    latest_close_data_scaled = scaler.transform(latest_close_data.reshape(-1, 1))
    
    # Reshape the data for LSTM input: [samples, time steps, features]
    latest_close_data_scaled = latest_close_data_scaled.reshape(1, latest_close_data_scaled.shape[0], 1)
    
    # Make prediction: Predict the close price 30 minutes ahead (6 steps into the future)
    prediction_scaled = model.predict(latest_close_data_scaled)
    
    # Inverse transform the prediction to get the predicted price
    predicted_price = scaler.inverse_transform(prediction_scaled)
    predicted_close_price = predicted_price[0][0]

    # Calculate the percentage change
    percentage_change = ((predicted_close_price - current_price) / current_price) * 100
    
    # Fetch historical data to calculate support/resistance levels
    ohlcv_df = fetch_ohlcv(symbol)
    if ohlcv_df is None:
        print("Unable to fetch OHLCV data. Exiting.")
        return
    
    support_level, resistance_level = calculate_support_resistance(ohlcv_df)

    # Calculate stop loss: Current price minus the difference between predicted and current price
    if predicted_close_price > current_price:
        stop_loss = current_price - abs(predicted_close_price - current_price)
    else:
        stop_loss = current_price + abs(predicted_close_price - current_price)

    # Determine Buy/Sell suggestion
    if percentage_change > 0.5:
        suggestion = "\033[92mSuggested Buy\033[0m"  # Green text
    elif percentage_change < -0.5:
        suggestion = "\033[93mSuggested Sell\033[0m"  # Orange text
    elif 0.2 <= percentage_change <= 0.5:
        suggestion = "\033[92mShort Buy\033[0m"
    elif -0.5 <= percentage_change <= -0.2:
        suggestion = "\033[93mShort Sell\033[0m"
    elif -0.19 <= percentage_change <= 0.19:
        suggestion = "\033[90mNEUTRAL\033[0m"
    else:
        suggestion = "No strong suggestion"

    # Print the outputs including the stop loss, prediction, and live price
    print(f"\nLive Ethereum Price: ${round(current_price, 2)}")
    print(f"Predicted Price in 30 Minutes: ${round(predicted_close_price, 2)}")
    print(f"Predicted Percentage Change: {round(percentage_change, 2)}%")
    print(f"Suggested Stop Loss: ${round(stop_loss, 2)}")
    print(f"Support Level: ${round(support_level, 2)}")
    print(f"Resistance Level: ${round(resistance_level, 2)}")
    print(suggestion)

def calculator():
    print("Entering calculator mode. Type 'exitc' to quit.")
    while True:
        user_input = input("Enter a mathematical expression (e.g., 2 + 2): ").strip().lower()
        if user_input == 'exitc':
            print("Exiting calculator mode.")
            break
        try:
            result = eval(user_input)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("Type 'predict' to make a prediction for 30 minutes ahead, 'calculator' to use the calculator, or 'exit' to quit.")

    while True:
        user_input = input("\nEnter command: ").strip().lower()
        
        if user_input == 'pr':
            predict_30m_ahead()
        elif user_input == 'calc':
            calculator()
        elif user_input == 'exit':
            print("Exiting...")
            break
        else:
            print("Invalid command. Please type 'predict', 'calculator', or 'exit'.")

if __name__ == '__main__':
    main()
