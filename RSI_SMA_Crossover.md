# RSI and SMA Crossover Trading Strategy

## Overview

The RSI and SMA Crossover Trading Strategy is a quantitative approach to making trading decisions based on the Relative Strength Index (RSI) and Simple Moving Average (SMA) crossovers. This strategy aims to capture potential trend reversals by considering both short-term and long-term moving averages along with RSI momentum.

### Entry Criteria

- **Long Position:**
  - SMA for the past week crosses over the SMA for the past month.
  - RSI is above a specified threshold (e.g., 60).

- **Short Position:**
  - SMA for the past week crosses under the SMA for the past month.
  - RSI is below a specified threshold (e.g., 40).

### Exit Criteria

- Exit trade when the SMA crossover in the opposite direction.
- Exit trade when the set Stop Loss or Take Profit has been achieved.

## Strategy Implementation

The strategy can be implemented using your preferred programming language (e.g., Python, C++, R). Here, we have shown a basic implementation in Python:
### 1. Libraries and Dependencies

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from ta import add_all_ta_features
import warnings
warnings.filterwarnings("ignore")
```

### 2. Fetch Data
```python
ticker = 'BTC-USD'  # You can change this to any valid stock symbol
start_date = '2011-01-01'
end_date = '2021-01-01'

stock_data = yf.download(ticker, start=start_date, end=end_date)
```

### 3. Calculation of Indicators.
```python
# Calculate SMAs
stock_data['SMA_5'] = stock_data['Close'].rolling(window=5).mean()
stock_data['SMA_22'] = stock_data['Close'].rolling(window=22).mean()

# Calculate RSI
stock_data['RSI'] = add_all_ta_features(stock_data, "Close", slow_rsi=14)
```

### 4. Conditions for entering long or short positions.
```python
stock_data['Long_Signal'] = np.where((stock_data['SMA_5'].shift(1) < stock_data['SMA_22'].shift(1)) & (stock_data['SMA_5'] > stock_data['SMA_22']) & (stock_data['RSI'] > 65), 1, 0)
stock_data['Short_Signal'] = np.where((stock_data['SMA_5'].shift(1) > stock_data['SMA_22'].shift(1)) & (stock_data['SMA_5'] < stock_data['SMA_22']) & (stock_data['RSI'] < 35), 1, 0)
stock_data['Long_Signal'] = np.where((stock_data['SMA_5'] > stock_data['SMA_22']) & (stock_data['RSI'] < 65), 1, 0)
stock_data['Short_Signal'] = np.where((stock_data['SMA_5'] < stock_data['SMA_22']) & (stock_data['RSI'] > 35), 1, 0)
```

Customize your code for the following components:

1. Conditions for entering long or short positions.
2. Exit conditions for both long and short positions, including Stop Loss and Take Profit.
3. Implement a system to monitor the status of trades.

## Performace
Explore the visual representation of the strategy's performance below:
![sma-rsi](https://github.com/the-quantclub-iitbhu/Algorithmic_Trading_Strategies/assets/159526866/3beda484-3403-4303-a1af-93463b2bf134)

The above visual illustrates the generated buy and sell signals, along with the SMAs, RSI, and daily Close price of BTC.
- By following these trade signals in conjunction with adjusted stop losses, this strategy demonstrates the following performance:
![sma-rsi-btc-pnl](https://github.com/the-quantclub-iitbhu/Algorithmic_Trading_Strategies/assets/159526866/78852514-9ab1-45a3-88b5-145adc2eb269)
These visuals provide insights into the strategy's effectiveness, showcasing the signals and resulting performance when applied to BTC trading.


## Additional Reference
- [RSI](https://zerodha.com/varsity/chapter/indicators-part-1/)
- [SMA](https://www.investopedia.com/terms/s/sma.asp)
- [Support and Resistance levels](https://zerodha.com/varsity/chapter/support-resistance/)
- [More Trading Strategies](https://example.com/quant-club-strategy-guide](https://www.investopedia.com/ask/answers/012915/what-are-best-technical-indicators-complement-relative-strength-index-rsi.asp)https://www.investopedia.com/ask/answers/012915/what-are-best-technical-indicators-complement-relative-strength-index-rsi.asp)
