import os
from binance.client import Client

# Binance API keys
API_KEY = 'QuXGsx73cNxrA3OKD8lQqwdOUynUSnWLnbvtqaCahMXLjZ8CcNTBvB2T2Dp5TJpl'
API_SECRET = 'DgQ9mWhKeLUHdoEL70DPRmOPzLroCwQTIgDBy7YinxFt1x8ooTUp0sEGSCq8xay6'

client = Client(API_KEY, API_SECRET, testnet=True)

# Store trade information
trade_info = {}

# File paths for each model's recommendation
files = [
    "random_forest_recommendation.txt",
    "gradient_boost_recommendation.txt",
    "svc_recommendation.txt",
    "logistic_regression_recommendation.txt"
]

recommendations = []

# Read each recommendation from the files
for file in files:
    if os.path.exists(file):
        with open(file, "r") as f:
            rec = f.read().strip()  # Read recommendation and strip any newlines
            recommendations.append(rec)
    else:
        print(f"Recommendation file {file} not found!")

# Check if we have recommendations from all models
if len(recommendations) < len(files):
    print("Not all recommendations are available.")
else:
    # Aggregate recommendations (e.g., majority voting)
    final_recommendation = max(set(recommendations), key=recommendations.count)
    print(f"Overall Recommendation: {final_recommendation}")

# Buy function with Take Profit limit sell order
def buy_order(symbol, quantity, take_profit_price):
    try:
        # Place market buy order
        order = client.order_market_buy(
            symbol=symbol,
            quantity=quantity
        )
        entry_price = float(order['fills'][0]['price'])  # Entry price from the order response
        print(f"Buy order placed: {order}")

        # Store trade information
        if symbol not in trade_info:
            trade_info[symbol] = []
        trade_info[symbol].append({'type': 'buy', 'quantity': quantity, 'price': entry_price})

        # Place a limit sell order (Take Profit)
        sell_order = client.order_limit_sell(
            symbol=symbol,
            quantity=quantity,
            price=str(take_profit_price)  # Convert to string
        )
        print(f"Take Profit order placed at {take_profit_price}: {sell_order}")

    except Exception as e:
        print(f"An error occurred while placing buy order: {e}")

# Sell function with Take Profit limit buy order
def sell_order(symbol, quantity, take_profit_price):
    try:
        # Place market sell order
        order = client.order_market_sell(
            symbol=symbol,
            quantity=quantity
        )
        exit_price = float(order['fills'][0]['price'])  # Exit price from the order response
        print(f"Sell order placed: {order}")

        # Store trade information
        if symbol not in trade_info:
            trade_info[symbol] = []
        trade_info[symbol].append({'type': 'sell', 'quantity': quantity, 'price': exit_price})

        # Place a limit buy order (Take Profit after shorting)
        buy_order = client.order_limit_buy(
            symbol=symbol,
            quantity=quantity,
            price=str(take_profit_price)  # Convert to string
        )
        print(f"Take Profit buy order placed at {take_profit_price}: {buy_order}")

    except Exception as e:
        print(f"An error occurred while placing sell order: {e}")

# Set the symbol and quantity for trading
symbol = 'BTCUSDT'  # Symbol for Bitcoin/USDT trading pair
quantity = 0.004  # Amount of BTC to buy/sell (adjust as needed)

# Define take profit percentage (e.g., 1% profit)
take_profit_percentage = 0.01

# Get the current price of the symbol
ticker = client.get_symbol_ticker(symbol=symbol)
current_price = float(ticker['price'])
print(f"Current price of {symbol}: {current_price}")

# Calculate the take profit prices for buy and sell orders
take_profit_buy_price = current_price * (1 + take_profit_percentage)  # For buy orders
take_profit_sell_price = current_price * (1 - take_profit_percentage)  # For sell orders

# Execute buy or sell based on final recommendation
if final_recommendation == "Buy":
    buy_order(symbol, quantity, take_profit_buy_price)
elif final_recommendation == "Sell":
    sell_order(symbol, quantity, take_profit_sell_price)

# Fetch account balance
def get_account_balance():
    try:
        account_info = client.get_account()
        balances = account_info['balances']
        for asset in balances:
            if float(asset['free']) > 0 or float(asset['locked']) > 0:
                print(f"Asset: {asset['asset']}, Free: {asset['free']}, Locked: {asset['locked']}")
    except Exception as e:
        print(f"Error fetching account balance: {e}")

# Fetch open orders for a specific symbol
def get_open_orders(symbol=None):
    try:
        open_orders = client.get_open_orders(symbol=symbol)
        if len(open_orders) == 0:
            print("No open orders.")
        else:
            for order in open_orders:
                print(order)
        return open_orders  # Return the open orders for further processing
    except Exception as e:
        print(f"Error fetching open orders: {e}")
        return []  # Return an empty list on error

# Fetch trade history for a symbol
def get_trade_history(symbol):
    try:
        trades = client.get_my_trades(symbol=symbol)
        if trades:  # If trades are returned, return them
            return trades
        else:
            print(f"No trade history for {symbol}.")
            return []  # Return an empty list if no trades
    except Exception as e:
        print(f"Error fetching trade history: {e}")
        return []  # Return an empty list on error

# Calculate total profit and loss
def calculate_profit_loss(open_orders, trade_history, current_price):
    total_profit_loss = 0

    # Calculate profit/loss from trade history
    for trade in trade_history:
        price = float(trade['price'])
        qty = float(trade['qty'])
        is_buy = trade['isBuyer']

        # Check if trade is a buy or sell
        if is_buy:
            # For buy trades, we deduct the cost from total profit/loss
            total_profit_loss -= price * qty
        else:
            # For sell trades, we add the revenue from the sale
            total_profit_loss += price * qty

    # Calculate unrealized profit/loss from open orders
    for order in open_orders:
        qty = float(order['origQty'])
        if order['side'] == 'SELL':
            # If it's a sell order, calculate profit/loss as current price minus order price
            sell_price = float(order['price'])
            total_profit_loss += (sell_price - current_price) * qty  # Assume sell order will be filled at current price
        elif order['side'] == 'BUY':
            # If it's a buy order, calculate profit/loss as current price minus order price
            buy_price = float(order['price'])
            total_profit_loss += (current_price - buy_price) * qty  # Assume buy order will be filled at current price

    return total_profit_loss

# Get trade history
trade_history = get_trade_history(symbol='BTCUSDT')
open_orders = get_open_orders(symbol='BTCUSDT')  # Get open orders and handle the returned value
profit_loss = calculate_profit_loss(open_orders, trade_history, current_price)
print(f"Total Profit/Loss: {profit_loss} USDT")

# Print current price
print(f"Current price of BTCUSDT: {current_price}")

# Calculate and print total profit and loss
total_profit_and_loss = profit_loss
print(f"Total Profit and Loss: {total_profit_and_loss}")
