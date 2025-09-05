import yfinance as yf
import math

TICKER = "AAPL"
DATA = yf.download(TICKER, period="1y")
CLOSE_PRICES = DATA["Close"][TICKER].tolist()
N = 10

position_array = []

for t in range(N, len(CLOSE_PRICES)):
    moving_average = sum(CLOSE_PRICES[t - N:t]) / N
    position_array.append(1 if CLOSE_PRICES[t] >= moving_average else -1)

def calculate_cumulative_pnl(index):
    cpnl = 0
    for t in range(N + 1, index):
        pnl = position_array[t - (N + 1)] * (CLOSE_PRICES[t] - CLOSE_PRICES[t - 1])
        cpnl += pnl
    return cpnl

# Total Return
print(f"Total Return: {calculate_cumulative_pnl(len(CLOSE_PRICES))}")

# Sharpe Ratio
daily_return_list = []
for t in range(N + 1, len(CLOSE_PRICES)):
    daily_return = position_array[t - (N + 1)] * (CLOSE_PRICES[t] - CLOSE_PRICES[t - 1]) / CLOSE_PRICES[t - 1]
    daily_return_list.append(daily_return)

avg_daily_return = sum(daily_return_list) / len(daily_return_list)
squared_difference = 0
for t in range(len(daily_return_list)):
    squared_difference += (daily_return_list[t] - avg_daily_return) ** 2
std_dev_daily_return = math.sqrt(squared_difference / (len(daily_return_list) - 1))
sharpe = avg_daily_return / std_dev_daily_return
print(f"Sharpe Ratio: {sharpe}")

# Max Drawdown
max_cpnl = float("-inf")
max_drawdown = float("+inf")
for t in range(N + 1, len(CLOSE_PRICES)):
    cpnl = calculate_cumulative_pnl(t)
    max_cpnl = max(max_cpnl, cpnl)
    drawdown = (cpnl - max_cpnl) / max_cpnl if max_cpnl != 0 else float("+inf")
    max_drawdown = min(max_drawdown, drawdown)
print(f"Max Drawdown: {max_drawdown}")
