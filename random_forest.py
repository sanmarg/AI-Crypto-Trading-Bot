import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the saved model
model_filename = 'random_forest_model.pkl'
loaded_model = joblib.load(model_filename)

# Load data (ensure this CSV has the required indicators)
df = pd.read_csv('btc_data_with_indicators.csv')  # Assuming indicators are included here

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

# Check if required columns exist
required_columns = ['close']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"DataFrame must contain the following columns: {required_columns}")

# Calculate indicators if not already present
if 'RSI' not in df.columns or 'MACD' not in df.columns:
    df['RSI'] = calculate_rsi(df['close'])
    df['MACD'], df['MACD_signal'] = calculate_macd(df['close'])

# Calculate Simple Moving Average (SMA) and Exponential Moving Average (EMA)
df['SMA_50'] = df['close'].rolling(window=50).mean()
df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

# Remove missing values
df = df.dropna()

# Prepare features for prediction
features = ['SMA_50', 'EMA_20', 'RSI', 'MACD', 'MACD_signal']

# Make predictions for all data points in the DataFrame
df['prediction'] = loaded_model.predict(df[features])

# Convert prediction from numeric to categorical recommendation
df['recommendation'] = np.where(df['prediction'] == 1, 'Buy', 'Sell')

# Determine overall recommendation based on the majority of recommendations
overall_recommendation = df['recommendation'].mode()[0]  # Get the most common recommendation

# Display the overall recommendation
print(f"Overall Recommendation: {overall_recommendation}")

# Assume 'overall_recommendation' contains "Buy" or "Sell"
with open("random_forest_recommendation.txt", "w") as file:
    file.write(overall_recommendation)


# Optionally, display the full DataFrame with predictions if needed
# print(df[['timestamp', 'close', 'SMA_50', 'EMA_20', 'RSI', 'MACD', 'MACD_signal', 'prediction', 'recommendation']])


print(type(loaded_model))