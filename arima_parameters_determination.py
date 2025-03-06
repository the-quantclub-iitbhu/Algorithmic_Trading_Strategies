import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

"""
Fetch historical stock data for Apple (AAPL) for the past 600 days with daily interval
Ensure the interval suits your analysis
Importing large amount of data from yfinance may be considered as data scapping by yfinance

"""

data = yf.download(tickers="AAPL", period="600d", interval="1d")  

# Extract closing prices for analysis
close_prices = data[['Close']].copy()
close_prices.describe()  # Summary statistics of closing prices

from statsmodels.tsa.stattools import adfuller

# Perform Augmented Dickey-Fuller (ADF) test to check for stationarity
ad_fuller_result = adfuller(close_prices.Close.dropna())
print(f"ADF Statistic: {ad_fuller_result[0]}")  # Test statistic
print(f"p-value: {ad_fuller_result[1]}")  # p-value to determine stationarity

from statsmodels.graphics.tsaplots import plot_acf

# Plot the original closing prices and their autocorrelation function (ACF)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
ax1.plot(close_prices.Close)
ax1.set_title("Original")
plot_acf(close_prices.Close, ax=ax2)

# First-order differencing to remove trends
diff = close_prices.Close.diff().dropna()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
ax1.plot(diff)
ax1.set_title("First difference")
plot_acf(diff, ax=ax2)

from pmdarima.arima.utils import ndiffs

# Automatically determine the required number of differences to achieve stationarity
ndiffs(close_prices.Close, test="adf")

from statsmodels.graphics.tsaplots import plot_pacf

# Perform differencing again for PACF analysis
diff = close_prices.Close.diff().dropna()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
ax1.plot(diff)
ax1.set_title("First difference")
ax2.set_ylim(0, 1) 
plot_pacf(diff, ax=ax2)  # Partial autocorrelation plot to determine AR order

from statsmodels.tsa.arima.model import ARIMA

# Fit an ARIMA model (p=3, d=1, q=0) based on ACF and PACF insights
model = ARIMA(close_prices.Close, order=(3, 1, 0))
result = model.fit()

# Display model summary statistics
print(result.summary())

# Plot residuals to assess error distribution
residuals = pd.DataFrame(result.resid)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
ax1.plot(residuals)  # Residual time series plot
ax1.set_title("Residual time series plot")
ax2.hist(residuals, density=True)  # Histogram of residuals
ax2.set_title("Histogram of residuals")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
ax1.plot(close_prices.Close)
ax1.set_title("Original")
plot_acf(close_prices.Close, ax=ax2)

from statsmodels.graphics.tsaplots import plot_predict

# Forecast future values and overlay predictions on the original series
plot_predict(result, start=1, end=500, ax=ax1);