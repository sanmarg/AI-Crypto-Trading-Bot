import ccxt
import pandas as pd
from datetime import datetime, timedelta
import os

# Initialize the Binance exchange API
exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '15m'  # 15-minute timeframe
limit = 500  # Max 500 entries per request

# Calculate the timestamp for 6 months ago from now
now = datetime.utcnow()
six_months_ago = now - timedelta(days=6*30)  # Approx 6 months as 180 days
since = exchange.parse8601(six_months_ago.strftime('%Y-%m-%dT%H:%M:%SZ'))

all_ohlcv = []

while since < exchange.parse8601(now.strftime('%Y-%m-%dT%H:%M:%SZ')):
    try:
        # Fetch OHLCV data in batches of 500
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit=limit)

        if not ohlcv:
            break  # Exit if no more data is returned

        all_ohlcv += ohlcv
        since = ohlcv[-1][0] + 1  # Update 'since' to the last timestamp

    except ccxt.NetworkError as e:
        print(f"Network error: {str(e)}")
        break
    except ccxt.BaseError as e:
        print(f"Exchange error: {str(e)}")
        break

# Convert to DataFrame
df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Specify the CSV file path
csv_file_path = 'btc_data.csv'


df.to_csv(csv_file_path, mode='w', header=True, index=False)

print(f"Fetched {len(df)} entries. BTC/USDT data from the last 15 minutes has been appended to '{csv_file_path}'.")
