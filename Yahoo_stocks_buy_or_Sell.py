import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import timedelta
from tabulate import tabulate

# Updated list of stocks to analyze
stocks = [
    "V", "TSLA", "COST", "META", "AMD", "PEP", "PYPL", "BABA", "CLDX", "BTC-USD", "TMUS",
    "AMZN", "MSFT", "JPM", "MA", "INTU", "CME", "PANW", "TSM", "SONY", "AGO", "C", "ADBE", "DELL", "SPOT"
]

# Initialize a list to store buy/sell signals summary
summary = []

for ticker in stocks:
    # Download historical stock data (last 3 months, daily granularity)
    stock = yf.Ticker(ticker)
    data = stock.history(period="3mo", interval="1d")  # 3 months of daily data

    # Calculate 5-day and 30-day Moving Averages
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA30'] = data['Close'].rolling(window=30).mean()

    # Identify Buy and Sell signals
    buy_signals = (data['MA5'].shift(1) < data['MA30'].shift(1)) & (data['MA5'] >= data['MA30'])
    sell_signals = (data['MA5'].shift(1) > data['MA30'].shift(1)) & (data['MA5'] <= data['MA30'])

    # Find the most recent Buy/Sell signal dates within the last 3 days
    recent_buy_dates = data.index[buy_signals][-3:]
    recent_sell_dates = data.index[sell_signals][-3:]

    # Check if a Buy/Sell signal occurred in the last 3 days
    recent_buy = buy_signals.tail(3).any()
    recent_sell = sell_signals.tail(3).any()

    # Determine the latest Buy/Sell signal status and date
    latest_buy = '\033[1;32mY\033[0m' if recent_buy else 'NA'  # Bold Green Y for Buy
    latest_sell = '\033[1;31mY\033[0m' if recent_sell else 'NA'  # Bold Red Y for Sell
    signal_date = recent_buy_dates[-1].strftime('%Y-%m-%d') if recent_buy else (recent_sell_dates[-1].strftime('%Y-%m-%d') if recent_sell else 'NA')

    # Add to summary
    summary.append({
        'Stock': ticker,
        'Buy': latest_buy,
        'Sell': latest_sell,
        'Signal Date': signal_date
    })

# Create a DataFrame for the summary and sort by Sell and Buy (prioritizing 'Y' values)
def sort_priority(value):
    return 0 if '\033[1;31mY\033[0m' in value or '\033[1;32mY\033[0m' in value else 1

summary_df = pd.DataFrame(summary, columns=['Stock', 'Buy', 'Sell', 'Signal Date'])
summary_df.sort_values(by=['Sell', 'Buy'], key=lambda col: col.map(sort_priority), inplace=True)

# Display the sorted summary table with borders and colored 'Y' values
print("\nSummary of Buy/Sell Signals (within the last 3 days):")
print(tabulate(summary_df, headers='keys', tablefmt='fancy_grid', showindex=False))

# Plotting after printing the summary
for ticker in stocks:
    stock = yf.Ticker(ticker)
    data = stock.history(period="3mo", interval="1d")
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA30'] = data['Close'].rolling(window=30).mean()
    buy_signals = (data['MA5'].shift(1) < data['MA30'].shift(1)) & (data['MA5'] >= data['MA30'])
    sell_signals = (data['MA5'].shift(1) > data['MA30'].shift(1)) & (data['MA5'] <= data['MA30'])

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label=f'{ticker} Close Price', alpha=0.7)
    plt.plot(data.index, data['MA5'], label='5-Day MA', linewidth=2)
    plt.plot(data.index, data['MA30'], label='30-Day MA', linewidth=2)
    plt.scatter(data.index[buy_signals], data['Close'][buy_signals], label='Buy Signal', marker='^', color='green', s=100)
    plt.scatter(data.index[sell_signals], data['Close'][sell_signals], label='Sell Signal', marker='v', color='red', s=100)

    plt.title(f'{ticker} Stock Price with 5-Day and 30-Day Moving Averages (Buy/Sell Signals)')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
