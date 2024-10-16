import os
from binance.client import Client

# Binance API keys
API_KEY = 'QuXGsx73cNxrA3OKD8lQqwdOUynUSnWLnbvtqaCahMXLjZ8CcNTBvB2T2Dp5TJpl'
API_SECRET = 'DgQ9mWhKeLUHdoEL70DPRmOPzLroCwQTIgDBy7YinxFt1x8ooTUp0sEGSCq8xay6'


# Initialize the Binance client
client = Client(API_KEY, API_SECRET, testnet=True)

# Fetch account balance
def get_account_balance():
    try:
        account_info = client.get_account()
        balances = account_info['balances']
        btc_balance = 0
        for asset in balances:
            if asset['asset'] == 'BTC':
                btc_balance = float(asset['free']) + float(asset['locked'])
                print(f"BTC Balance: {btc_balance} BTC")
                return btc_balance
        print("BTC balance not found.")
    except Exception as e:
        print(f"Error fetching account balance: {e}")

def get_trade_amounts(symbol='BTCUSDT'):
    try:
        trades = client.get_my_trades(symbol=symbol)
        total_bought = 0
        total_sold = 0
        
        for trade in trades:
            qty = float(trade['qty'])
            is_buy = trade['isBuyer']
            
            if is_buy:
                total_bought += qty
            else:
                total_sold += qty

        return total_bought, total_sold

    except Exception as e:
        print(f"Error fetching trade history: {e}")
        return 0, 0  # Return zeros in case of error



# Main function to execute the balance check
if __name__ == "__main__":
    print("Fetching BTC holdings...")
    get_account_balance()
    print("Fetching BTC trade amounts...")
    total_bought, total_sold = get_trade_amounts(symbol='BTCUSDT')
    print(f"Total BTC Bought: {total_bought} BTC")
    print(f"Total BTC Sold: {total_sold} BTC")
