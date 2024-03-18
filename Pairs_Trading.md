# Pairs Trading Strategy

Pairs trading presents a market-neutral approach aiming to capitalize on the relative performance of two correlated assets. This strategy identifies correlated pairs of stocks and executes trades based on deviations from their historical relationship.

## Strategy Overview

### Objective

This implementation of the pairs trading strategy focuses on:

- Identifying highly correlated pairs of stocks.
- Calculating trading signals based on statistical indicators.
- Managing positions and implementing risk control measures.

### Strategy Components

1. **Data Collection**: Fetch historical stock price data from Yahoo Finance API.
 
2. **Pair Selection**: Identify pairs of stocks with significant correlation coefficients.

3. **Spread Computation**: Calculate the spread between paired stocks using a hedge ratio derived from linear regression.

4. **Stationarity Testing**: Conduct the Dickey-Fuller test on the spread to confirm stationarity, suitable for pairs trading.

5. **Z-Score Calculation**: Compute the z-score of the spread using a rolling window for mean and standard deviation.

6. **Signal Generation**: Generate trading signals based on z-score deviations from historical means. Initiate long and short positions when z-score crosses predefined thresholds.

7. **MACD Integration**: Incorporate MACD indicator to generate additional trading signals based on z-score spread.

8. **Position Management**: Dynamically manage positions and implement stop-loss measures for risk control.

9. **Performance Monitoring**: Continuously monitor profit and loss (PnL) to evaluate strategy effectiveness.

## Pros and Cons

### Pros

- Market Neutrality: Designed to be market-neutral, potentially profiting irrespective of market direction.
- Statistical Edge: Relies on statistical analysis and mean-reversion principles, offering a systematic trading approach.
- Risk Management: Incorporates stop-loss measures to mitigate risk.
- Diversification Benefits: Trading multiple pairs of stocks can offer diversification, reducing idiosyncratic risk.

### Cons

- Correlation Dependence: Relies on historical correlation, which may break during market stress or fundamental changes.
- Execution Complexity: Executing pairs trades simultaneously can be challenging, particularly during volatile or illiquid market conditions.
- Model Risk: Performance depends heavily on the accuracy of statistical models, introducing model risk.
- Transaction Costs: Frequent trading may incur significant transaction costs, potentially eating into profits, especially for smaller portfolios.


## Strategy Implementation

The strategy can be implemented using your preferred trading platform or programming language (e.g., Python, R). Below is a simplified example using historical price data:
```python
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import warnings

warnings.filterwarnings("ignore")
```
The dictionary 'stocks' is created to store information about various stocks traded on the Indian stock market:
```python
stocks = {
    'TCS.NS': 'TCS (Tata Consultancy Services)',
    'INFY.NS': 'Infosys',
    'WIPRO.NS': 'Wipro',
    'HCLTECH.NS': 'HCL Technologies',
    'SUNPHARMA.NS': 'Sun Pharmaceutical Industries',
    'DRREDDY.NS': 'Dr. Reddy\'s Laboratories',
    'CIPLA.NS': 'Cipla',
    'LUPIN.NS': 'Lupin',
    'HDFCBANK.NS': 'HDFC Bank',
    'ICICIBANK.NS': 'ICICI Bank',
    'SBIN.NS': 'State Bank of India',
    'KOTAKBANK.NS': 'Kotak Mahindra Bank',
    'TATAMOTORS.NS': 'Tata Motors',
    'MARUTI.NS': 'Maruti Suzuki India',
    'RELIANCE.NS': 'Reliance Industries',
    'IOC.NS': 'Indian Oil Corporation',
    'LT.BO': 'Larsen & Toubro Ltd',
    'GMRINFRA.NS': 'GMR Airports Infrastructure',
    'BDL.NS': 'Bharat Dynamics Limited',
}
```

Defining a time period for retrieving historical data:
```python
start_date = (datetime.today() - timedelta(days=365*4)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')
```

Fetching historical stock price data for each stock symbol listed in the stocks dictionary and aggregating it for further steps:
```python
# Create an empty DataFrame to store the data
stock_data = pd.DataFrame()

# Download data for each ticker and append it to the DataFrame
for ticker, company in stocks.items():
    data = yf.download(ticker, start=start_date, end=end_date)
    close_prices = data['Close']
    close_prices.rename(company, inplace=True)
    stock_data = pd.concat([stock_data, close_prices], axis=1)

# Reset index
stock_data.reset_index(inplace=True)
```
Correlation Matrix
```python
# Calculate correlation matrix
correlation_matrix = stock_data.corr()

# Plot correlation matrix as a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Stocks Correlation Matrix')
plt.show()
```
![image](https://github.com/the-quantclub-iitbhu/Algorithmic_Trading_Strategies/assets/159526866/b01f3a2c-9f28-4478-bd37-71e69f22b6e9)

```python
# Plot correlation matrix with only pairs that we will use for our trading strategy
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap=sns.diverging_palette(220, 20, as_cmap=True),
            fmt=".2f", linewidths=0.5, mask=~((correlation_matrix > 0.95) & (correlation_matrix != 1)))

plt.title('Stocks Correlation Matrix')
plt.show()
```
![image](https://github.com/the-quantclub-iitbhu/Algorithmic_Trading_Strategies/assets/159526866/404c225b-9bbd-41e1-a0c3-2d0520245f1d)

```python
# Initialize an empty dictionary to store pairs
high_correlation_pairs = {}

# Iterate through the correlation matrix to find pairs with correlation > 0.9 (or < -0.9) and not the same coin
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        if (correlation_matrix.iloc[i, j] > 0.95) and \
                correlation_matrix.columns[i] != correlation_matrix.columns[j]:
            pair = (correlation_matrix.columns[i], correlation_matrix.columns[j])
            high_correlation_pairs[pair] = correlation_matrix.iloc[i, j]

# Display the dictionary of pairs
print(high_correlation_pairs)
```
```python
# Function to calculate spread
def calculate_spread(a, b, hedge_ratio):
    spread = np.log(a) - hedge_ratio * np.log(b)
    return spread

# Dictionary to store hedge ratios for each pair
hedge_ratios = {}

# Calculate hedge ratios using regression for each pair
for pair in high_correlation_pairs:
    # Preprocess data to handle missing or infinite values
    df = stock_data[[pair[0], pair[1]]].dropna()
    x = np.log(df[pair[0]])
    y = np.log(df[pair[1]])

    # Perform OLS regression
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()

    # Store hedge ratio if regression is successful
    if not model.params.empty:
        hedge_ratios[pair] = model.params[1]
    else:
        print(f"Regression failed for pair: {pair}")

# Print hedge ratios for each pair
print("Hedge Ratios:")
for pair, ratio in hedge_ratios.items():
    print(f"{pair}: {ratio}")
```
```python
# Calculate and print spreads for each pair using the calculated hedge ratio
print("\nSpreads:")
for pair, ratio in hedge_ratios.items():
    spread = calculate_spread(stock_data[pair[0]], stock_data[pair[1]], ratio)
    print(f"{pair}: Spread mean: {spread.mean()}, Spread std dev: {spread.std()}")
```

```python
# Dictionary to store acceptable pairs
acceptable_pairs = {}

# Run Dickey Fuller test on the spread values
for pair, ratio in hedge_ratios.items():
    # Preprocess data to handle missing or infinite values
    df = pd.concat([stock_data[pair[0]], stock_data[pair[1]]], axis=1).dropna()
    spread = calculate_spread(df[pair[0]], df[pair[1]], ratio)
    result = adfuller(spread)

    # Check if p-value is less than 0.05
    if result[1] < 0.05:
        acceptable_pairs[pair] = hedge_ratios[pair]

    print(f"\nDickey-Fuller Test Results for {pair}:")
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print(f'   {key}: {value}')
```

```python
# Function to calculate z-score
def calculate_zscore(spread, window):
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()
    zscore = (spread - rolling_mean) / rolling_std
    return zscore
```

```python
# Entry and exit points
window = 20  # Window size for rolling mean and std deviation
threshold_upper = 2  # Upper threshold for z-score entry
threshold_lower = -2  # Lower threshold for z-score entry

# Entry and exit points for each pair
entry_long_points_dict = {}
entry_short_points_dict = {}
exit_points_dict = {}

for pair, ratio in acceptable_pairs.items():
    spread = calculate_spread(stock_data[pair[0]], stock_data[pair[1]], ratio)
    zscore = calculate_zscore(spread, window)
    open_trade = False

    # Initialize lists to store entry and exit points for this pair
    entry_long_points = []
    entry_short_points = []
    exit_points = []

    # Find entry and exit points
    for i in range(len(zscore)):
        if not open_trade:
            if zscore[i] <= threshold_lower:  # Entry Long
                entry_long_points.append((stock_data['index'][i], zscore[i]))
                open_trade = True
            elif zscore[i] >= threshold_upper:  # Entry Short
                entry_short_points.append((stock_data['index'][i], zscore[i]))
                open_trade = True
        elif open_trade:
            if (zscore[i] > 0 and zscore[i-1] <= 0) or (zscore[i] < 0 and zscore[i-1] >= 0):  # Exit Long or Short
                exit_points.append((stock_data['index'][i], zscore[i]))
                open_trade = False

    # Store entry and exit points for this pair in the dictionaries
    entry_long_points_dict[pair] = entry_long_points
    entry_short_points_dict[pair] = entry_short_points
    exit_points_dict[pair] = exit_points
```

```python
# Plot spread and z-score for each pair with entry and exit points
for pair, ratio in acceptable_pairs.items():
    spread = calculate_spread(stock_data[pair[0]], stock_data[pair[1]], ratio)
    zscore = calculate_zscore(spread, window)

    # Plot spread and z-score
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['index'], spread, label='Spread')
    plt.axhline(threshold_upper, color='r', linestyle='--', label='Upper Threshold')
    plt.axhline(threshold_lower, color='g', linestyle='--', label='Lower Threshold')
    plt.plot(stock_data['index'], zscore, label='Z-Score', color='orange')

    # Plot entry and exit points
    entry_long_points = entry_long_points_dict.get(pair, [])
    entry_short_points = entry_short_points_dict.get(pair, [])
    exit_points = exit_points_dict.get(pair, [])

    for point in entry_long_points:
        plt.scatter(point[0], point[1], color='green', marker='^')
    for point in entry_short_points:
        plt.scatter(point[0], point[1], color='red', marker='v')
    for point in exit_points:
        plt.scatter(point[0], point[1], color='blue', marker='o')

    # Add legend
    legend_entries = {'Entry Long': 'green', 'Entry Short': 'red', 'Exit Trade': 'blue'}
    plt.legend(labels=legend_entries.keys(), handles=[plt.Line2D([0], [0], marker='^', color='w', markerfacecolor=color, markersize=10) for color in legend_entries.values()], loc='best')

    plt.title(f"Spread and Z-Score for {pair[0]} and {pair[1]}")
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()
```
![image](https://github.com/the-quantclub-iitbhu/Algorithmic_Trading_Strategies/assets/159526866/d28a30b6-331b-46f1-89b3-3d9f664a4e8b)

```python
# Calculate MACD
short_ema = zscore.ewm(span=12, adjust=False).mean()
long_ema = zscore.ewm(span=26, adjust=False).mean()
macd_line = short_ema - long_ema
signal_line = macd_line.ewm(span=9, adjust=False).mean()
macd_histogram = macd_line - signal_line

# Plot MACD
plt.figure(figsize=(12, 6))
plt.plot(stock_data['index'], macd_line, label='MACD Line', color='blue')
plt.plot(stock_data['index'], signal_line, label='Signal Line', color='red')
plt.bar(stock_data['index'], macd_histogram, label='MACD Histogram', color='green')
plt.title('MACD Indicator for Z-Score Spread')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()
```
![image](https://github.com/the-quantclub-iitbhu/Algorithmic_Trading_Strategies/assets/159526866/cbd81f4e-0993-4071-8f4c-487280b2ae1d)

```python
# Trading signals based on MACD
entry_long = (macd_line > signal_line)
entry_short = (macd_line < signal_line)

total_capital = 2000000

# Distribute capital equally for both pairs
capital_per_pair = total_capital / 2

# Initialize variables to track positions and PnL
positions = {pair[0]: {'position': 0, 'unrealized_pnl': 0}, pair[1]: {'position': 0, 'unrealized_pnl': 0}}  # Track positions and unrealized PnL for each stock
prev_entry_long = False  # Track previous long entry signal
prev_entry_short = False  # Track previous short entry signal
stop_loss = 0.015  # Stop loss threshold
pnl = 0  # Total PnL
pnl_values = []  # List to store PnL values over time

# Iterate over each day to generate signals and calculate PnL
for i in range(len(stock_data)):
    # Check for long entry signal
    if entry_long.iloc[i] and not prev_entry_long:
        # Place buy order for pair[0] and sell order for pair[1] with determined position size
        positions[pair[0]]['position'] -= capital_per_pair / stock_data[pair[0]].iloc[i]
        positions[pair[1]]['position'] += capital_per_pair / stock_data[pair[1]].iloc[i]
    # Check for short entry signal
    elif entry_short.iloc[i] and not prev_entry_short:
        # Place sell order for pair[0] and buy order for pair[1] with determined position size
        positions[pair[0]]['position'] += capital_per_pair / stock_data[pair[0]].iloc[i]
        positions[pair[1]]['position'] -= capital_per_pair / stock_data[pair[1]].iloc[i]

    # Update previous entry signals
    prev_entry_long = entry_long.iloc[i]
    prev_entry_short = entry_short.iloc[i]

    # Calculate PnL for each stock based on price change and update unrealized PnL
    for stock in positions:
        positions[stock]['unrealized_pnl'] = positions[stock]['position'] * (stock_data[stock].iloc[i] - stock_data[stock].iloc[i - 1])

        # Check if stop loss is triggered
        if positions[stock]['unrealized_pnl'] / stock_data[stock].iloc[i] >= stop_loss:
            # Exit position
            pnl += positions[stock]['unrealized_pnl']
            positions[stock]['position'] = 0
            positions[stock]['unrealized_pnl'] = 0

    # Calculate total PnL
    total_pnl = sum(positions[stock]['unrealized_pnl'] for stock in positions)
    pnl_values.append(pnl + total_pnl)

# Plot PnL
plt.figure(figsize=(12, 6))
plt.plot(stock_data['index'], pnl_values, label='PnL', color='blue')
plt.title('PnL Over Time with Stop Loss')
plt.xlabel('Date')
plt.ylabel('PnL')
plt.legend()
plt.show()
```
![image](https://github.com/the-quantclub-iitbhu/Algorithmic_Trading_Strategies/assets/159526866/3192f350-22d6-46e6-bf17-5c5678286a45)

    



## References

- [Pairs Trading Basics](https://blog.quantinsti.com/pairs-trading-basics/)
- [MACD Indicator](https://www.investopedia.com/terms/m/macd.asp)

## Requirements

- Python 3.x
- Required libraries: `yfinance`, `pandas`, `numpy`, `seaborn`, `matplotlib`, `statsmodels`
- Access to financial data via Yahoo Finance API

## Usage

1. Install necessary Python libraries.
2. Execute the provided Python script to implement the pairs trading strategy.
3. Adjust parameters such as window sizes, threshold values, and stop-loss levels according to preference.
4. Monitor PnL and tweak the strategy as necessary.


## Disclaimer

- This pairs trading strategy is for educational purposes only and does not constitute financial advice.
- Past performance is not indicative of future results. Trading involves risks, and losses may occur.
- Use this strategy at your own risk, and consider consulting a financial advisor before making trading decisions.
