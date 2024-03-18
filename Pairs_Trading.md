# Pairs Trading Strategy

Pairs trading is a market-neutral trading strategy that aims to profit from the relative performance of two correlated assets. In this strategy, we identify pairs of stocks that exhibit high correlation and trade based on deviations from their historical relationship.

## Strategy Overview

### Objective

The objective of this pairs trading strategy is to identify highly correlated pairs of stocks, calculate trading signals based on statistical indicators, manage positions, and implement risk control measures.

### Strategy Components

1. **Data Collection**: Historical stock price data for selected stocks is collected using the Yahoo Finance API.

2. **Pair Selection**: Pairs of stocks with high correlation coefficients are identified.

3. **Spread Calculation**: The spread between the two stocks in each pair is calculated using a defined hedge ratio obtained from linear regression.

4. **Stationarity Test**: The Dickey-Fuller test is performed on the spread to determine stationarity, indicating a mean-reverting behavior suitable for pairs trading.

5. **Z-Score Calculation**: The z-score of the spread is calculated using a rolling window for mean and standard deviation.

6. **Entry and Exit Signals**: Trading signals are generated based on z-score deviations from historical means. Long and short positions are initiated when the z-score crosses predefined thresholds.

7. **MACD Indicator**: An additional trading signal is generated using the MACD indicator applied to the z-score spread.

8. **Position Management**: Positions are managed dynamically, and stop-loss measures are implemented to control risk.

9. **Performance Monitoring**: Profit and loss (PnL) are monitored over time to evaluate the effectiveness of the strategy.

## Pros and Cons

### Pros

- Market-Neutral: Pairs trading is designed to be market-neutral, meaning it can potentially generate profits regardless of market direction.
- Statistical Edge: The strategy relies on statistical analysis to identify trading opportunities based on mean-reversion principles, offering a systematic approach to trading.
- Risk Control: Stop-loss measures help control risk by limiting losses in case of adverse price movements.
- Diversification: By trading multiple pairs of stocks, the strategy can provide diversification benefits and reduce idiosyncratic risk.

### Cons

- Correlation Breakdown: Pairs trading relies on the historical correlation between assets, which may break down during periods of market stress or fundamental changes in the underlying stocks.
- Execution Challenges: Trading pairs requires simultaneous execution of buy and sell orders, which can be challenging, especially for illiquid stocks or during volatile market conditions.
- Model Risk: The strategy's performance heavily depends on the accuracy of statistical models used for spread calculation and signal generation, introducing model risk.
- Transaction Costs: Frequent trading in multiple stocks incurs transaction costs, which can erode profits, especially for smaller portfolios.

## References

- [Pairs Trading Basics](https://blog.quantinsti.com/pairs-trading-basics/)
- [MACD Indicator](https://www.investopedia.com/terms/m/macd.asp)

## Requirements

- Python 3.x
- Required libraries: `yfinance`, `pandas`, `numpy`, `seaborn`, `matplotlib`, `statsmodels`
- Access to financial data via Yahoo Finance API

## Usage

1. Install the required Python libraries.
2. Run the provided Python script to execute the pairs trading strategy.
3. Adjust parameters such as window sizes, threshold values, and stop-loss levels as needed.
4. Monitor the PnL and adjust the strategy accordingly.

## Disclaimer

- This pairs trading strategy is for educational purposes only and does not constitute financial advice.
- Past performance is not indicative of future results. Trading involves risks, and losses may occur.
- Use this strategy at your own risk, and consider consulting a financial advisor before making trading decisions.
