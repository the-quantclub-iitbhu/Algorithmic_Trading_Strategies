# Import necessary libraries
import pandas as pd  # Data manipulation
import numpy as np  # Numerical computations
import os  # OS-related operations
import matplotlib.pyplot as plt  # Plotting library
import time  # Time handling
import yfinance as yf  # Yahoo Finance API for stock data retrieval

# -------------------------------------------
# Step 1: Download Historical Stock Data
# -------------------------------------------

# Download historical stock data for AAPL (Apple) 
# Data fetched: Daily intervals over the last 600 days
df = yf.download(tickers="AAPL", period="600d", interval="1d")

# Retain only the 'Close' price column for modeling
df = df[['Close']].copy()

# -------------------------------------------
# Step 2: Split Data into Training & Testing Sets
# -------------------------------------------

# Define training (80%) and testing (20%) split
n = int(len(df) * 0.8)
train = df.Close[:n]  # First 80% as training data
test = df.Close[n:]    # Remaining 20% as test data

# -------------------------------------------
# Step 3: Train the ARIMA Model
# -------------------------------------------

from statsmodels.tsa.arima.model import ARIMA  # Import ARIMA model for time series forecasting

# Define ARIMA model with specified order (p , d , q)
# - p (autoregressive term)
# - d (difference order)
# - q (moving average term)

p,d,q = map(int , input().split())
model = ARIMA(train, order=(p,d,q))

# Fit the ARIMA model to training data
result = model.fit()

# Print model summary containing statistical details
print(result.summary())

# -------------------------------------------
# Step 4: Forecast Future Prices
# -------------------------------------------

# Set number of forecast steps (predict the next 50 days)
step = 50
fc = result.get_forecast(steps=step)  # Generate forecast

# Extract predicted values from the forecast
fc_pred = fc.predicted_mean

# Align forecasted index with test data index (first 50 days of test set)
fc_pred.index = test[:step].index

# Extract confidence intervals for forecasted values
conf = fc.conf_int()
lower = pd.Series(conf.iloc[:, 0])  # Lower bound of confidence interval
upper = pd.Series(conf.iloc[:, 1])  # Upper bound of confidence interval

# -------------------------------------------
# Step 5: Visualize Forecast vs Actual Data
# -------------------------------------------

plt.figure(figsize=(8,4))  # Set figure size
plt.plot(test[:step], label="Actual")  # Plot actual test data
plt.plot(fc_pred, label="Forecast", linestyle="dashed")  # Plot forecasted values
plt.fill_between(fc_pred.index, lower, upper, color='gray', alpha=0.2)  # Add confidence interval shading
plt.title("AAPL Stock Price Forecast vs Actual")  # Set plot title
plt.legend(loc="upper left")  # Add legend
plt.show()  # Display the plot
