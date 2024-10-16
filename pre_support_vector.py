import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib 

# Load data
df = pd.read_csv('btc_data_with_indicators.csv')  # Update the path as needed

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
df['RSI'] = calculate_rsi(df['close'])
df['MACD'], df['MACD_signal'] = calculate_macd(df['close'])
df['SMA_50'] = df['close'].rolling(window=50).mean()
df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

# Remove missing values
df = df.dropna()

# Create target variable
df['target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)

# Select features and target
features = ['SMA_50', 'EMA_20', 'RSI', 'MACD', 'MACD_signal']
X = df[features]
y = df['target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Support Vector Classifier model
svc_model = SVC(probability=True)
svc_model.fit(X_train, y_train)

# Make predictions
y_pred = svc_model.predict(X_test)

model_filename = 'support_vector_model.pkl'
joblib.dump(log_model, model_filename)
print(f"Model saved to {model_filename}")