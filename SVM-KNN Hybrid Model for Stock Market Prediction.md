<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# 

---

# SVM-KNN Hybrid Model for Stock Market Prediction

## Overview

The SVM-KNN hybrid model combines the classification capabilities of Support Vector Machine (SVM) with the predictive power of K-Nearest Neighbor (KNN) to forecast stock market movements. This approach is applied to historical data from stocks like Apple (AAPL), incorporating technical indicators to enhance prediction accuracy.

## Data Preparation

1. **Dataset Collection**
    - Collect historical stock data including open, high, low, close prices, and volume.
    - Example data includes:
        - Date
        - Close
        - High
        - Low
        - Open
        - Volume
        - EMA (Exponential Moving Average)
        - RSI (Relative Strength Index)
        - ATR (Average True Range)
        - Forecasted EMA
        - Forecasted RSI
        - Forecasted ATR
2. **Feature Engineering**
    - Apply technical indicators:
        - **EMA**: $$
EMA_i = EMA_{i-1} + \alpha \times (u_{ic} - EMA_{i-1})
$$
        - **RSI**: $$
RSI = 100 - \frac{100}{1 + RS}
$$, where $$
RS = \frac{Average\ Gain}{Average\ Loss}
$$
        - **ATR**: $$
ATR = \frac{1}{n} \sum_{i=1}^{n} TR_i
$$, where $$
TR_i = \max(|High_i - Low_i|, |High_i - Close_{i-1}|, |Low_i - Close_{i-1}|)
$$
3. **Normalization**
    - Scale all data points to range[^1] using min-max normalization:

$$
\tilde{u}_{ij} = \frac{u_{ij} - u_{min,j}}{u_{max,j} - u_{min,j}}
$$

## SVM Classification

1. **Classifier Training**
    - Train SVM to classify data into profit or loss scenarios.
    - Use a radial basis function (RBF) kernel for non-linear classification:

$$
K(u_i, u_j) = \exp(-\gamma ||u_i - u_j||^2)
$$
2. **Classification**
    - SVM predicts binary outcome (profit/loss):

$$
p = \text{sgn}(\sum_{i=1}^{n} y_i \alpha_i K(u_i, x) + \rho)
$$

## KNN Prediction

1. **Neighbor Selection**
    - Select k nearest neighbors with similar class labels.
    - Calculate Euclidean distance between data points:

$$
d(u_i, u_j) = \sqrt{(u_i - u_j)^2}
$$
2. **Value Prediction**
    - Compute mean change among selected neighbors:

$$
\Delta c = \frac{1}{k} \sum_{i=1}^{k} \Delta c_i
$$
    - Predict future value by adding mean change to current value:

$$
\text{Future Value} = \text{Current Value} + \Delta c
$$

## Performance Evaluation

1. **Error Metrics**
    - For closing price: Mean Absolute Percentage Error (MAPE) and Root Mean Squared Error (RMSE).
    - For volatility: Mean Squared Forecast Error (MSFE), Root Mean Squared Forecast Error (RMSFE), and Mean Absolute Forecast Error (MAFE).
2. **Key Advantages**
    - Reduced complexity compared to neural network models.
    - No complex weight updating procedures.
    - Explicit control over classifier complexity and error.
    - Better scaling to high-dimensional data.
    - Superior prediction accuracy.

## Example Use Case

This model can be applied to predict the closing prices of stocks like Apple (AAPL) by analyzing historical data and technical indicators. The output can help investors decide whether to buy, sell, or hold stocks based on predicted trends.

### Code Structure

The code follows a structured approach:

1. **Data Import and Cleaning**
2. **Feature Engineering (Technical Indicators)**
3. **SVM Training and Classification**
4. **KNN Prediction**
5. **Performance Evaluation**

Each step is crucial in building a comprehensive model that leverages both classification and regression capabilities to predict stock market movements accurately.

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/51651304/c1b10080-f755-43cc-8927-c2e4860aab08/TQC_SVM-KNN_strategy.ipynb

