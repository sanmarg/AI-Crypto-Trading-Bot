import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib  # Import joblib for model serialization

# Load data
df = pd.read_csv('btc_data_with_indicators.csv')  # Assuming you saved indicators here

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

# Calculate indicators
df['RSI'] = calculate_rsi(df['close'])
df['MACD'], df['MACD_signal'] = calculate_macd(df['close'])

# Calculate Simple Moving Average (SMA) and Exponential Moving Average (EMA)
df['SMA_50'] = df['close'].rolling(window=50).mean()
df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

# Remove missing values
df = df.dropna()

# Create target variable (1 for price increase, 0 for price decrease)
df['target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)  # Using .loc to avoid SettingWithCopyWarning

# Select features and target
features = ['SMA_50', 'EMA_20', 'RSI', 'MACD', 'MACD_signal']
X = df[features]
y = df['target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions
y_pred = rf_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred))

# Save the model to a file
model_filename = 'random_forest_model.pkl'
joblib.dump(rf_model, model_filename)
print(f'Model saved to {model_filename}')
