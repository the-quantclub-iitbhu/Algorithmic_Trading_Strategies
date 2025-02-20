import pandas as pd
import ta

def calculate_bollinger_bands(data, window=20, std_dev=2):
    """
    Calculate Bollinger Bands for a given dataset.

    Parameters:
    data (pd.DataFrame): DataFrame containing 'close' price data.
    window (int): Lookback period for the moving average.
    std_dev (float): Standard deviation multiplier for upper/lower bands.

    Returns:
    pd.DataFrame: DataFrame with added 'SMA', 'Upper_Band', and 'Lower_Band' columns.
    """
    data['SMA'] = data['close'].rolling(window).mean()
    data['StdDev'] = data['close'].rolling(window).std()
    data['Upper_Band'] = data['SMA'] + (std_dev * data['StdDev'])
    data['Lower_Band'] = data['SMA'] - (std_dev * data['StdDev'])
    return data

def calculate_rsi(data, period=14):
    """
    Calculate the Relative Strength Index (RSI).

    Parameters:
    data (pd.DataFrame): DataFrame containing 'close' price data.
    period (int): Lookback period for RSI calculation.

    Returns:
    pd.DataFrame: DataFrame with added 'RSI' column.
    """
    data['RSI'] = ta.momentum.RSIIndicator(data['close'], window=period).rsi()
    return data

def mean_reversion_strategy(data):
    """
    Implement a mean reversion strategy using Bollinger Bands and RSI.

    Entry Conditions:
    - Buy when price is below the lower Bollinger Band and RSI is below 30.
    - Sell when price is above the upper Bollinger Band and RSI is above 70.

    Parameters:
    data (pd.DataFrame): DataFrame containing 'close' price data.

    Returns:
    pd.DataFrame: DataFrame with added 'Signal' column (1 = Buy, -1 = Sell, 0 = No Action).
    """
    data = calculate_bollinger_bands(data)
    data = calculate_rsi(data)

    # Generate trade signals
    data['Signal'] = 0
    data.loc[(data['close'] < data['Lower_Band']) & (data['RSI'] < 30), 'Signal'] = 1  # Buy Signal
    data.loc[(data['close'] > data['Upper_Band']) & (data['RSI'] > 70), 'Signal'] = -1  # Sell Signal

    return data

# Example Usage
if __name__ == "__main__":
    df = pd.read_csv("market_data.csv")  # Ensure the CSV has 'close' column
    df = mean_reversion_strategy(df)
    print(df[['close', 'Upper_Band', 'Lower_Band', 'RSI', 'Signal']].tail())  # View last few results
