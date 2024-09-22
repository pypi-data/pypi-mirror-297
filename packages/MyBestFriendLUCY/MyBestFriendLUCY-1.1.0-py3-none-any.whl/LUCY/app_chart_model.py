import ccxt
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import matplotlib.pyplot as plt
import pandas_ta as ta  # For technical indicators like ATR

# Load both models and scalers
model_1h = tf.keras.models.load_model('eth_lstm_model-h.h5')
scaler_1h = joblib.load('scaler-h.pkl')

model_30m = tf.keras.models.load_model('eth_lstm_model.h5')
scaler_30m = joblib.load('scaler.pkl')

# Initialize Binance API
binance = ccxt.binance()

# Function to fetch the current price
def fetch_current_price(symbol='ETH/USDT'):
    try:
        ticker = binance.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"Error fetching current price: {str(e)}")
        return None

# Function to fetch latest data (OHLCV) for the given symbol and timeframe
def fetch_latest_data(symbol='ETH/USDT', timeframe='30m', limit=48):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        return np.array([x[4] for x in ohlcv]), pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching latest data: {str(e)}")
        return None, None

# Function to preprocess the data
def preprocess_data(data, scaler):
    data = data.reshape(-1, 1)
    data_scaled = scaler.transform(data)
    data_scaled = data_scaled.reshape(1, data_scaled.shape[0], 1)
    return data_scaled

# Function to make predictions using the model
def predict_price(model, scaler, data):
    data_scaled = preprocess_data(data, scaler)
    prediction = model.predict(data_scaled, verbose=0)  # Suppressed verbose output
    predicted_price = scaler.inverse_transform(prediction).flatten()[0]
    return predicted_price

# Function to calculate support and resistance levels
def calculate_support_resistance(ohlcv_df):
    support_level = ohlcv_df['low'].min()  # Simplistic approach; you could use more complex methods
    resistance_level = ohlcv_df['high'].max()
    return support_level, resistance_level

# Function to show the live Ethereum price
def show_live_price():
    current_price = fetch_current_price()
    if current_price is not None:
        print(f"\nLive Ethereum Price: ${round(current_price, 3)}")
    else:
        print("Unable to fetch the current price.")

# Function to predict only the next 30 minutes using the 30-minute model, and 1 hour using the 1-hour model
def predict_next_30m_1h(symbol='ETH/USDT'):
    current_price = fetch_current_price(symbol)
    if current_price is None:
        print("Unable to fetch the current price. Exiting.")
        return None, None

    # Fetch the latest data for 30-minute intervals
    latest_data_30m, ohlcv_df_30m = fetch_latest_data(symbol=symbol, timeframe='30m', limit=48)
    if latest_data_30m is None or len(latest_data_30m) < 48:
        print('Not enough data to make a prediction. Exiting.')
        return None, None

    # Predict the next 30 minutes using the 30-minute model
    predicted_price_30m = predict_price(model_30m, scaler_30m, latest_data_30m)
    
    # Predict the next 1 hour using the 1-hour model
    predicted_price_1h = predict_price(model_1h, scaler_1h, latest_data_30m)

    return current_price, predicted_price_30m, predicted_price_1h, latest_data_30m

# Function to generate predictions and display results
def make_prediction_and_suggest_stop_loss():
    symbol = 'ETH/USDT'
    
    # Fetch current price
    current_price = fetch_current_price(symbol)
    if current_price is None:
        print("Unable to fetch the current price. Exiting.")
        return
    
    # Fetch the latest data points for 1 hour interval
    latest_data_1h, ohlcv_df_1h = fetch_latest_data(symbol=symbol, timeframe='1h', limit=48)

    # Predict the next 30 minutes and 1 hour
    current_price_30m, predicted_price_30m, predicted_price_1h, past_data = predict_next_30m_1h()

    # Calculate support and resistance
    support_level, resistance_level = calculate_support_resistance(ohlcv_df_1h)

    # Display the predictions
    print(f"\nLive Ethereum Price: ${round(current_price_30m, 3)}")
    print(f"Predicted Price in 30 Minutes: ${round(predicted_price_30m, 3)}")
    print(f"Predicted Price in 1 Hour: ${round(predicted_price_1h, 3)}")
    print(f"Support Level: ${round(support_level, 3)}")
    print(f"Resistance Level: ${round(resistance_level, 3)}")

    # Graph the predictions
    plot_predictions(current_price_30m, past_data, predicted_price_30m, predicted_price_1h, support_level, resistance_level)

# Function to plot past data and predictions with support and resistance
def plot_predictions(current_price, past_data, predicted_price_30m, predicted_price_1h, support_level, resistance_level):
    time_points_past = [f'-{(48-i)*30}m' for i in range(len(past_data))]
    time_points_future = ['Now', '+30m', '+1h']
    time_points = time_points_past + ['Now'] + time_points_future

    prices_past = list(past_data)
    prices = [current_price, predicted_price_30m, predicted_price_1h]

    plt.figure(figsize=(10, 6))
    
    # Plot past prices (blue)
    plt.plot(time_points_past, prices_past, marker='o', linestyle='-', color='blue', label="Past Prices")
    
    # Plot predicted prices (green)
    plt.plot(['Now'] + time_points_future, [current_price] + prices, marker='o', linestyle='-', color='green', label="Predicted Prices")
    
    # Plot support and resistance levels
    plt.axhline(y=support_level, color='g', linestyle='--', label='Support Level')
    plt.axhline(y=resistance_level, color='r', linestyle='--', label='Resistance Level')
    
    plt.title('Ethereum Price Prediction with Past Values and Support/Resistance Levels')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    
    # Adjust y-axis limits to tighten the range and enhance visibility of small changes
    y_min = min(prices_past + prices + [support_level, resistance_level]) * 0.995  # Add buffer to make changes more visible
    y_max = max(prices_past + prices + [support_level, resistance_level]) * 1.005
    plt.ylim([y_min, y_max])  # Set y-axis range based on predictions and support/resistance levels

    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

# Function to enter calculator mode
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

# Main function to interact with the user
def main():
    print("Type 'predict' to make a prediction, 'calculator' to use the calculator, or 'exit' to quit.")

    while True:
        user_input = input("\nEnter command: ").strip().lower()
        
        if user_input == 'predict' or user_input == 'pr':
            make_prediction_and_suggest_stop_loss()
        elif user_input == 'calc':
            calculator()
        elif user_input == 'exit':
            print("Exiting...")
            break
        elif user_input == 'p':
            show_live_price()
        else:
            print("Invalid command. Please type 'predict', 'calc', 'p', or 'exit'.")

if __name__ == '__main__':
    main()