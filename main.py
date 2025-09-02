import yfinance as yf
import math

ticker = "AAPL"
data = yf.download(ticker, period="1y")
close_prices = data["Close"][ticker]
n = 50
pos_array = []

for t in range(n, len(close_prices)):
    moving_average = sum(close_prices[t - n:t]) / n
    pos_array.append(1 if close_prices[t] >= moving_average else -1)

# Total Return
cumulative_pnl = 0
for t in range(n + 1, len(close_prices)):
    pnl = pos_array[t - (n + 1)] * (close_prices[t - n] - close_prices[t - (n + 1)])
    cumulative_pnl += pnl
print(f"Total Return: ${cumulative_pnl}")

# Sharpe Ratio
daily_return = []
for t in range(n + 1, len(close_prices)):
    ret = (close_prices[t] - close_prices[t - 1]) / close_prices[t - 1]
    daily_return.append(ret)

avg_daily_return = sum(daily_return) / len(daily_return)
squared_difference = 0
for t in range(1, len(daily_return)):
    squared_difference += (daily_return[t] - daily_return[t - 1]) ** 2
std_dev_dr = math.sqrt(squared_difference / (len(daily_return) - 1))
sharpe = avg_daily_return / std_dev_dr
print(f"Sharpe Ratio: ${sharpe}")
