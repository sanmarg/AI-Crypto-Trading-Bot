---

# 🚀 AI Crypto Trading Bot 🧠📊

Welcome to the **AI Crypto Trading Bot** repository! This project integrates machine learning models with the Binance API to automate crypto trading decisions based on real-time market data. The bot implements a variety of models to make **buy** and **sell** recommendations, using an ensemble approach to ensure the best possible trading strategy. The bot can also place take-profit orders and calculate overall profit and loss (PnL) based on trading history.

## Dashboard
![image](https://github.com/user-attachments/assets/01a42316-7abe-4753-b07a-30d4d8dfaf37)

![image](https://github.com/user-attachments/assets/cbcce679-6f7b-4869-a364-744336449f88)

## Logs of the nohup command
### Starting 25 lines of the log: Here mark the value of Profit and Loss
![image](https://github.com/user-attachments/assets/bfd655a8-55ba-4d57-a015-7a09bd07534e)
### Ending 25 lines of the log: Here mark the value of Profit and Loss
![image](https://github.com/user-attachments/assets/b4a590e2-532f-4adb-8f7c-a8bc2bef75a3)


## 📜 Features

- **Multiple Machine Learning Models:** Combines recommendations from multiple models including:
  - Random Forest
  - Gradient Boosting
  - Support Vector Classifier (SVC)
  - Logistic Regression

- **Trade Automation:** Automatically places market buy/sell orders with Binance using the official **Binance API**. Supports placing **Take Profit** limit orders after each trade.
  
- **Profit and Loss Calculation:** Calculates the overall PnL based on executed trades and open orders.

- **Account Overview:** Fetches account balance and open order information for the specified trading pair.
  
- **Trade History Retrieval:** Tracks and retrieves historical trades for a specified trading pair.

## 🛠️ Technologies Used

- **Binance API:** Real-time crypto trading and account management.
- **Python** for logic and trading operations.
- **Machine Learning Models** for buy/sell recommendation (Random Forest, Gradient Boosting, SVC, Logistic Regression).
  
## ⚙️ Project Workflow

1. **Read Model Recommendations:** The bot reads trading recommendations from model output files (e.g., `random_forest_recommendation.txt`, `gradient_boost_recommendation.txt`).
  
2. **Aggregate Recommendations:** The bot uses majority voting to determine the final trading recommendation (buy or sell).
  
3. **Place Orders:** 
   - If the final recommendation is **Buy**, a market buy order is placed and a **Take Profit** sell order is set at a specified profit percentage.
   - If the final recommendation is **Sell**, a market sell order is placed, followed by a **Take Profit** buy order after shorting.
  
4. **Track Profit and Loss:** The bot tracks profit and loss based on trade execution and open orders.

5. **Monitor Account:** The bot fetches the current balance, open orders, and trade history for the trading pair, ensuring real-time monitoring of your account.

## 🏗️ How to Run the Bot

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/ai-crypto-trading-bot.git
   cd ai-crypto-trading-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your **Binance API Keys**:
   - Replace the placeholders for `API_KEY` and `API_SECRET` in the code with your actual Binance API keys.

4. Place your model recommendations in `.txt` files:
   - Ensure the recommendation files (e.g., `random_forest_recommendation.txt`, `gradient_boost_recommendation.txt`) exist and contain either "Buy" or "Sell" based on your model predictions.

5. Run the bot:
   ```bash
   python trading_bot.py
   ```

## 📝 Example Output

- **Overall Recommendation:**
  ```
  Overall Recommendation: Buy
  ```

- **Trade Execution:**
  ```
  Buy order placed: {'symbol': 'BTCUSDT', 'orderId': 12345, ...}
  Take Profit order placed at 43000: {'symbol': 'BTCUSDT', 'orderId': 12346, ...}
  ```

- **Profit and Loss Calculation:**
  ```
  Total Profit/Loss: 50 USDT
  ```

## 💡 Future Improvements

- **Integration with More Machine Learning Models:** Expand the set of models to include more advanced algorithms such as XGBoost, LSTM, or Reinforcement Learning.
  
- **Backtesting:** Implement a backtesting framework to simulate trades and test different strategies before deploying in real-time trading.
  
- **Risk Management:** Add risk management features such as stop-loss, trailing stop orders, and dynamic position sizing based on account balance and market conditions.

## ⚖️ Disclaimer

This bot is for educational purposes only. Trading cryptocurrencies is risky, and the authors are not responsible for any financial losses incurred by using this bot. Always perform thorough research and consider consulting with a financial advisor before engaging in trading activities.

---

🔗 **Check out the code and contribute to the project**: [GitHub Repository](https://github.com/sanmarg/ai-crypto-trading-bot)

