# Fibonacci Retracement Trading Strategy - Quant Club IIT BHU

## Overview

Welcome to the Fibonacci Retracement Trading Strategy tailored for all quant enthusiasts! This repository introduces a powerful trading strategy based on Fibonacci retracement levels. The strategy involves identifying potential price reversal points by using key Fibonacci ratios, allowing users to make informed decisions on entry and exit points.

### Disclaimer

**Important:** The information shared in this repository is for educational and research purposes only. Trading in financial markets involves significant risk, and past performance is not indicative of future results. Contributors to this repository are not financial advisors, and the strategies provided here should not be considered as financial advice. Members are encouraged to thoroughly understand and assess the risks before implementing any strategy.

## Strategy Highlights

### Key Fibonacci Ratios

- **38.2% Retracement:** Potential reversal level after a significant price movement.
- **50% Retracement:** Often considered a strong reversal level.
- **61.8% Retracement:** A key level indicating a potential continuation of the previous trend.

### Entry Criteria

- **Long Position:**
  - Price retraces to a Fibonacci support level.
  - Additional confirmation from other technical indicators.

- **Short Position:**
  - Price retraces to a Fibonacci resistance level.
  - Additional confirmation from other technical indicators.

### Exit Criteria

- Exit long position when the price reaches a Fibonacci resistance level.
- Exit short position when the price reaches a Fibonacci support level.
- Implement risk management strategies for stop-loss and take-profit levels.

## Strategy Implementation

The strategy can be implemented using your preferred trading platform or programming language (e.g., Python, R). Below is a simplified example using historical price data:

```python
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```
### Load historical price data
```python
ticker_symbol = 'BTC-USD'  # You can change this to any valid stock symbol
start_date = '2010-01-01'
end_date = '2024-01-01'

stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
```

### Calculate Fibonacci retracement levels
```python
high_price = stock_data['Close'].max()
low_price = stock_data['Close'].min()

# Fibonacci retracement levels (common levels: 38.2%, 50%, 61.8%)
fibonacci_levels = [0.382, 0.5, 0.618]

# Calculate Fibonacci levels based on the high and low prices
fibonacci_values = [low_price + level * (high_price - low_price) for level in fibonacci_levels]
```
### Implement the trading strategy
```python
# Generate Fibonacci retracement-based trading signals
stock_data['Long_Signal'] = np.where(stock_data['Close'] < fibonacci_values[0], 1, 0)  # Buy signal below 38.2% level
stock_data['Short_Signal'] = np.where(stock_data['Close'] > fibonacci_values[2], 1, 0)  # Sell signal above 61.8% level
```
### Exit signals
- Exit trade when an opposite signal is generated.
- Exit trade when the set Stop Loss or Take Profit has been achieved.

## Strategy Performance
Explore the visual representation of the strategy's performance below:
```python
plt.figure(figsize=(10, 6))
plt.plot(stock_data['Close'], label='Closing Prices', color='blue')

# Plot Buy signals
plt.scatter(stock_data.index[stock_data['Long_Signal'] == 1], 
            stock_data['Close'][stock_data['Long_Signal'] == 1], 
            marker='^', color='green', label='Buy Signal')

# Plot Sell signals
plt.scatter(stock_data.index[stock_data['Short_Signal'] == 1], 
            stock_data['Close'][stock_data['Short_Signal'] == 1], 
            marker='v', color='red', label='Sell Signal')

# Customize the plot
plt.title('Buy/Sell Signals with Fibonacci Retracement Levels')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
```
![image](https://github.com/Arin2k24/Algo_Strategies/assets/157686042/0361b6cf-5ace-485a-abc8-2bd802a804be)


The graph illustrates the Fibonacci Retracement Levels. By following the generated trade signals in conjunction with adjusted stop losses, this strategy demonstrates its effectiveness in various market conditions.
```python
# After generating a dataframe containing daily P&L 
plt.figure(figsize=(12, 6))
plt.plot(pnl.index, pnl['Net_PnL'].cumsum(), label='Net P&L', color='blue')
plt.title('Net P&L Over Time')
plt.xlabel('Date')
plt.ylabel('Net P&L Value')
plt.legend()
plt.show()
```
![image](https://github.com/Arin2k24/Algo_Strategies/assets/157686042/c848a9dd-d484-44f9-ba23-20e81184aea3)
## Additional Reference
- [StockCharts - Fibonacci Retracements](https://school.stockcharts.com/doku.php?id=chart_analysis:fibonacci_retracemen)
- [Investopedia - Fibonacci Retracement](https://www.investopedia.com/terms/f/fibonacciretracement.asp)
