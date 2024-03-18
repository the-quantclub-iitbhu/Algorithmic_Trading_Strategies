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