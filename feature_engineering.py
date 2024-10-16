import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('btc_data.csv')

# Check if required columns exist
if 'close' not in df.columns:
    raise ValueError("DataFrame must contain a 'close' column.")

# Function to calculate Simple Moving Average (SMA)
def calculate_sma(df, column='close', window=50):
    return df[column].rolling(window=window).mean()

# Function to calculate Exponential Moving Average (EMA)
def calculate_ema(df, column='close', span=20):
    return df[column].ewm(span=span, adjust=False).mean()

# Function to calculate Relative Strength Index (RSI)
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate MACD
def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    return macd, macd_signal

# Calculate indicators
df['SMA_50'] = calculate_sma(df, window=50)
df['EMA_20'] = calculate_ema(df, span=20)
df['RSI'] = calculate_rsi(df['close'])
df['MACD'], df['MACD_signal'] = calculate_macd(df['close'])

# Remove rows with NaN values
df = df.dropna()

# Optional: Save the DataFrame with calculated indicators back to a new CSV
df.to_csv('btc_data_with_indicators.csv', index=False)

print("Indicators calculated and saved to 'btc_data_with_indicators.csv'.")
