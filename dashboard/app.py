import os
import io
import base64
from flask import Flask, render_template, jsonify
from binance.client import Client
from binance.helpers import round_step_size
import datetime
import subprocess
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

# Binance API keys
API_KEY = 'QuXGsx73cNxrA3OKD8lQqwdOUynUSnWLnbvtqaCahMXLjZ8CcNTBvB2T2Dp5TJpl'
API_SECRET = 'DgQ9mWhKeLUHdoEL70DPRmOPzLroCwQTIgDBy7YinxFt1x8ooTUp0sEGSCq8xay6'

client = Client(API_KEY, API_SECRET, testnet=True)
app = Flask(__name__)

# Fetch account balance
def get_account_balance(limit=5):
    try:
        account_info = client.get_account()
        balances = account_info['balances']
        balance_list = []

        for asset in balances:
            free_amount = float(asset['free'])
            locked_amount = float(asset['locked'])
            total_amount = free_amount + locked_amount
            if total_amount > 0:
                balance_list.append({
                    'asset': asset['asset'],
                    'free': free_amount,
                    'locked': locked_amount,
                    'total': total_amount
                })

        # Sort by total amount and limit to 'limit' entries
        sorted_balances = sorted(balance_list, key=lambda x: x['total'], reverse=True)[:limit]
        return sorted_balances
    except Exception as e:
        print(f"Error fetching account balance: {e}")
        return []

# Fetch detailed trade history
# Fetch detailed trade history
def get_detailed_trade_history(symbol='BTCUSDT'):
    try:
        trades = client.get_my_trades(symbol=symbol)
        # Convert the 'time' to a datetime object for each trade
        for trade in trades:
            trade['time'] = datetime.datetime.fromtimestamp(trade['time'] / 1000)
        return sorted(trades, key=lambda x: x['time'])
    except Exception as e:
        print(f"Error fetching trade history: {e}")
        return []


# Fetch current price of BTC in USD
def get_current_btc_price():
    try:
        ticker = client.get_symbol_ticker(symbol="BTCUSDT")
        return float(ticker['price'])
    except Exception as e:
        print(f"Error fetching BTC price: {e}")
        return None

# Calculate Profit and Loss (PnL) for BTC
def calculate_btc_pnl():
    try:
        btc_balance = 0
        total_btc_spent = 0
        total_btc_sold = 0
        total_sell_revenue = 0

        trades = get_detailed_trade_history(symbol='BTCUSDT')

        for trade in trades:
            qty = float(trade['qty'])
            price = float(trade['price'])
            if trade['isBuyer']:
                btc_balance += qty
                total_btc_spent += qty * price
            else:  # Sell trade
                btc_balance -= qty
                total_sell_revenue += qty * price

        current_btc_price = get_current_btc_price()
        current_btc_value = btc_balance * current_btc_price if current_btc_price else 0
        pnl = total_sell_revenue - total_btc_spent

        return {
            'btc_balance': btc_balance,
            'total_btc_spent': total_btc_spent,
            'total_sell_revenue': total_sell_revenue,
            'current_btc_price': current_btc_price,
            'current_btc_value': current_btc_value,
            'pnl': pnl
        }
    except Exception as e:
        print(f"Error calculating PnL: {e}")
        return {}

def generate_trade_history_chart(detailed_trades):
    try:
        buy_times = []
        buy_prices = []
        sell_times = []
        sell_prices = []

        for trade in detailed_trades:
            trade_time = trade['time']  # This is already a datetime object
            if trade['isBuyer']:
                buy_times.append(trade_time)
                buy_prices.append(float(trade['price']))
            else:  # Sell trade
                sell_times.append(trade_time)
                sell_prices.append(float(trade['price']))

        plt.figure(figsize=(10, 5))
        plt.plot(buy_times, buy_prices, marker='o', label='Buy Orders', color='green')
        plt.plot(sell_times, sell_prices, marker='o', label='Sell Orders', color='red')
        plt.xlabel('Time')
        plt.ylabel('Price (USDT)')
        plt.title('Trade History')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return base64.b64encode(img.getvalue()).decode()
    except Exception as e:
        print(f"Error generating chart: {e}")
        return None

# Fetch log file using SCP command
def fetch_logs():
    try:
        scp_command = "scp -i ~/Downloads/san.pem azureuser@20.193.156.25:/home/azureuser/trade/crypto-trading-bot/output.log /home/sanmarg/crypto-trading-bot/dashboard/"
        result = subprocess.run(scp_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "Logs fetched successfully" if result.returncode == 0 else f"Error fetching logs: {result.stderr.decode('utf-8')}"
    except Exception as e:
        return f"Error: {e}"

# API route to fetch logs
@app.route('/fetch_logs')
def logs():
    return jsonify(message=fetch_logs())

# Home route to show account information and trade details
@app.route('/')
def dashboard():
    balances = get_account_balance(limit=5)
    detailed_trades = get_detailed_trade_history(symbol='BTCUSDT')
    pnl_data = calculate_btc_pnl()
    chart_image = generate_trade_history_chart(detailed_trades)

    return render_template(
        'dashboard.html',
        balances=balances,
        detailed_trades=detailed_trades,
        pnl_data=pnl_data,
        chart_image=chart_image
    )

if __name__ == "__main__":
    app.run(debug=True)