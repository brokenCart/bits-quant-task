import yfinance as yf
import math
import matplotlib.pyplot as plt
import os

# Creating directory for images
os.makedirs("images", exist_ok=True)

TICKER = "AAPL"
DATA = yf.download(TICKER, period="max")
CLOSE_PRICES = DATA["Close"][TICKER].tolist()
N = 10

dates = DATA.index[N:]
position_array = [1 if CLOSE_PRICES[t] >= sum(CLOSE_PRICES[t - N:t]) / N else -1 for t in range(N, len(CLOSE_PRICES))]
daily_pnl_array = [position_array[i - (N + 1)] * (CLOSE_PRICES[i] - CLOSE_PRICES[i - 1]) for i in range(N + 1, len(CLOSE_PRICES))]
cumulative_pnl_array = [sum(daily_pnl_array[:t - N]) for t in range(N + 1, len(CLOSE_PRICES))]

# Total Return
print(f"Total Return: {cumulative_pnl_array[-1]}")

# Sharpe Ratio
daily_return_list = [position_array[t - (N + 1)] * (CLOSE_PRICES[t] - CLOSE_PRICES[t - 1]) / CLOSE_PRICES[t - 1] for t in range(N + 1, len(CLOSE_PRICES))]
avg_daily_return = sum(daily_return_list) / len(daily_return_list)
std_dev_daily_return = math.sqrt(sum((daily_return_list[t] - avg_daily_return) ** 2 for t in range(len(daily_return_list))) / (len(daily_return_list) - 1))
sharpe = avg_daily_return / std_dev_daily_return
print(f"Sharpe Ratio: {sharpe}")

# Max Drawdown
max_cpnl = float("-inf")
max_drawdown = float("+inf")
for t in range(N + 1, len(CLOSE_PRICES)):
    cpnl = cumulative_pnl_array[t - (N + 2)]
    max_cpnl = max(max_cpnl, cpnl)
    drawdown = (cpnl - max_cpnl) / max_cpnl if max_cpnl != 0 else float("+inf")
    max_drawdown = min(max_drawdown, drawdown)
print(f"Max Drawdown: {max_drawdown}")

# Plotting cumulative PnL
plt.figure(1)
plt.plot(dates[1:], cumulative_pnl_array)
plt.xlabel("Days")
plt.ylabel("Cumulative PnL")
plt.title(f"Cumulative PnL for {TICKER}")
plt.savefig("images/cumulative_pnl.png")

# Time series for positions and cumulative PnL
# for date, pos in zip(dates, position_array):
#     print(date.date(), pos)

# for date, pnl in zip(dates, daily_pnl_array):
#     print(date.date(), pnl)

# Plotting daily positions
plt.figure(2)
plt.plot(dates, position_array, "o")
plt.xlabel("Days")
plt.ylabel("Position")
plt.title(f"Daily Position for {TICKER}")
plt.savefig("images/daily_position.png")

# Plotting daily PnL
plt.figure(3)
plt.plot(dates[1:], daily_pnl_array)
plt.xlabel("Days")
plt.ylabel("PnL")
plt.title(f"Daily PnL for {TICKER}")
plt.savefig("images/daily_pnl.png")

plt.close("all")
