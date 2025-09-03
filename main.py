import yfinance as yf
import math

ticker = "AAPL"
data = yf.download(ticker, period="1y")
close_prices = data["Close"][ticker]
n = 50
position_array = []

for t in range(n, len(close_prices)):
    moving_average = sum(close_prices[t - n:t]) / n
    position_array.append(1 if close_prices[t] >= moving_average else -1)

# Total Return
cumulative_pnl = 0
for t in range(n + 1, len(close_prices)):
    pnl = position_array[t - (n + 1)] * (close_prices[t - n] - close_prices[t - (n + 1)])
    cumulative_pnl += pnl
print(f"Total Return: ${cumulative_pnl}")

# Sharpe Ratio
daily_return_list = []
for t in range(n + 1, len(close_prices)):
    daily_return = (close_prices[t] - close_prices[t - 1]) / close_prices[t - 1]
    daily_return_list.append(daily_return)

avg_daily_return = sum(daily_return_list) / len(daily_return_list)
squared_difference = 0
for t in range(1, len(daily_return_list)):
    squared_difference += (daily_return_list[t] - daily_return_list[t - 1]) ** 2
std_dev_daily_return = math.sqrt(squared_difference / (len(daily_return_list) - 1))
sharpe = avg_daily_return / std_dev_daily_return
print(f"Sharpe Ratio: ${sharpe}")
