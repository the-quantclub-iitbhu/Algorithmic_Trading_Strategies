import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import time
import yfinance as yf

# Download historical stock data for AAPL (Apple) with daily intervals over 600 days
df = yf.download(tickers="AAPL", period="600d", interval="1d")

# Keep only the 'Close' price column for modeling
df = df[['Close']].copy()

# Split data into training (80%) and testing (20%) sets
n = int(len(df) * 0.8)
train = df.Close[:n]  # First 80% as training data
test = df.Close[n:]    # Remaining 20% as test data

from statsmodels.tsa.arima.model import ARIMA

# Define ARIMA model with order (p=20, d=1, q=3)
model = ARIMA(train, order=(20,1,3))

# Fit the ARIMA model to training data
result = model.fit()

# Print model summary with coefficients and statistics
print(result.summary())

# Set number of forecast steps (predict next 50 days)
step = 50
fc = result.get_forecast(steps=step)

# Get predicted values from the forecast
fc_pred = fc.predicted_mean

# Align forecasted index with test data
fc_pred.index = test[:step].index

# Get confidence interval for the forecast
conf = fc.conf_int()
lower = pd.Series(conf.iloc[:, 0])  # Lower bound
upper = pd.Series(conf.iloc[:, 1])  # Upper bound

# Plot actual vs forecasted values
plt.figure(figsize=(8,4))
plt.plot(test[:step], label="actual")  # Plot actual test data
plt.plot(fc_pred, label="forecast")  # Plot forecasted values
plt.title("Forecast vs Actual")
plt.legend(loc="upper left")
plt.show()  # Display the plot