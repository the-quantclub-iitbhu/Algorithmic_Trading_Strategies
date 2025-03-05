
This paper by L. J. Cao and Francis E. H. Tay introduces a novel approach to financial time series forecasting using Support Vector Machines (SVM) with adaptive parameters. The research addresses the inherent challenges of financial forecasting by incorporating the non-stationary nature of financial data into the SVM framework, resulting in improved prediction accuracy and more efficient model representation.

## Theoretical Foundation and Methodology

Financial time series forecasting presents unique challenges due to the inherent noise and non-stationarity of financial data. The distribution of financial time series changes over time, leading to gradual shifts in the dependency between input and output variables. Traditional SVM applies uniform parameters across all training data points, which may not be optimal for non-stationary financial data.

The standard SVM for regression approximates a function using the following form:

$$
f(x)=w \cdot \phi(x)+b
$$

Where $$
\phi(x)
$$ represents the high-dimensional feature spaces nonlinearly mapped from the input space. The coefficients $$
w
$$ and $$
b
$$ are estimated by minimizing the regularized risk function:

$$
\text{minimize} \frac{1}{2}\|w\|^{2}+C \frac{1}{l} \sum_{i=1}^{l} L_{\varepsilon}\left(y_{i}, f\left(x_{i}\right)\right)
$$

With the ε-insensitive loss function:

$$
L_{\varepsilon}\left(y_{i}, f\left(x_{i}\right)\right)= \begin{cases}\left|y_{i}-f\left(x_{i}\right)\right|-\varepsilon, & \left|y_{i}-f\left(x_{i}\right)\right| \geq \varepsilon \\0, & \text{otherwise}\end{cases}
$$

The decision function has the explicit form:

$$
f(x)=\sum_{i=1}^{l}\left(a_{i}-a_{i}^{*}\right) K\left(x_{i}, x\right)+b
$$

Where $$
a_{i}^{(*)}
$$ are the Lagrange multipliers, and $$
K(x_i, x)
$$ is the kernel function.

## The Innovative ASVM Approach

The key innovation presented in this paper is the Support Vector Machine with Adaptive Parameters (ASVM). This approach incorporates the non-stationary characteristic of financial time series by introducing two adaptive parameters:

1. Ascending Regularization Constant: Instead of using a fixed regularization constant $$
C
$$, ASVM employs an ascending function that assigns different weights to training data points based on their recency:

$$
C_{i} = C \frac{2}{1+\exp\left(a-2a \times \frac{i}{l}\right)}
$$

Where $$
i
$$ represents the data sequence ($$
i=l
$$ is the most recent point), and $$
a
$$ controls the ascending rate. This modification places more weight on recent data points and less weight on distant ones.

2. Descending Tube Size: ASVM implements a tube size that decreases from distant to recent training data points:

$$
\varepsilon_{i}=\varepsilon \frac{1+\exp(b-2b \times i/l)}{2}
$$

Where $$
b
$$ controls the descending rate. This adaptive tube size makes the solution sparser and further emphasizes recent data by making the approximation accuracy higher for recent points than for distant ones.

These modifications transform the standard SVM regularized risk function to:

$$
\text{minimize} \frac{1}{2}\|w\|^{2}+\sum_{i=1}^{l} C_{i}\left(\xi_{i}+\xi_{i}^{*}\right)
$$

Subject to:

$$
y_{i}-w \cdot \phi\left(x_{i}\right)-b \leq \varepsilon_{i}+\xi_{i}
$$

$$
w \cdot \phi\left(x_{i}\right)+b-y_{i} \leq \varepsilon_{i}+\xi_{i}^{*}
$$

$$
\xi^{(*)} \geq 0
$$

## Experimental Design and Data Processing

The researchers examined five futures contracts from the Chicago Mercantile Market:

- Standard \& Poor 500 stock index futures (CME-SP)
- United States 30-year government bond (CBOT-US)
- United States 10-year government bond (CBOT-BO)
- German 10-year government bond (EUREX-BUND)
- French government stock index futures (MATIF-CAC40)


### Input and Output Variables

The research utilized five input variables:

- Four lagged Relative Difference in Percentage of price (RDP) values:
    * RDP-5: $$
(p(i)-p(i-5))/p(i-5) \times 100
$$
    * RDP-10: $$
(p(i-5)-p(i-10))/p(i-10) \times 100
$$
    * RDP-15: $$
(p(i-10)-p(i-15))/p(i-15) \times 100
$$
    * RDP-20: $$
(p(i-15)-p(i-20))/p(i-20) \times 100
$$
- One transformed closing price (EMA100): obtained by subtracting a 100-day exponential moving average from the closing price to eliminate trends

The output variable was:

- RDP+5: $$
(\overline{p(i+5)}-\overline{p(i)})/\overline{p(i)} \times 100
$$, where $$
\overline{p(i)}
$$ is the three-day exponential moving average of the price


### Performance Metrics

The models were evaluated using three performance metrics:

1. Normalized Mean Squared Error (NMSE): $$
\frac{1}{\sigma^{2} n} \sum_{i=1}^{n}\left(y_{i}-\hat{y}_{i}\right)^{2}
$$
2. Mean Absolute Error (MAE): $$
\frac{1}{n} \sum_{i=1}^{n}\left|y_{i}-\hat{y}_{i}\right|
$$
3. Directional Symmetry (DS): $$
\frac{100}{n} \sum_{i=1}^{n} d_{i}
$$, where $$
d_{i}= \begin{cases}1 & \left(y_{i}-y_{i-1}\right)\left(\hat{y}_{i}-\hat{y}_{i-1}\right) \geq 0 \\0 & \text{otherwise}\end{cases}
$$

## Comparative Performance Analysis

The ASVM model was compared with standard SVM, back-propagation (BP) neural networks, weighted BP neural networks, and regularized radial basis function (RBF) neural networks. The experiments yielded several significant findings:

1. ASVM consistently outperformed standard SVM across all five futures contracts, achieving lower NMSE and MAE values and higher DS scores. Statistical analysis confirmed ASVM's superiority at a 2.5% significance level.
2. ASVM produced fewer support vectors than standard SVM, resulting in a sparser and more computationally efficient solution. This is evidenced by the comparison of converged support vectors:
    - CME-SP: 784 (ASVM) vs. 903 (SVM)
    - CBOT-US: 772 (ASVM) vs. 911 (SVM)
    - CBOT-BO: 789 (ASVM) vs. 911 (SVM)
    - EUREX-BUND: 789 (ASVM) vs. 909 (SVM)
    - MATIF-CAC40: 752 (ASVM) vs. 923 (SVM)
3. When compared to BP neural networks, SVM demonstrated superior performance in most futures contracts. The ASVM also outperformed weighted BP neural networks with a 5% significance level in statistical tests.
4. SVM and regularized RBF neural networks showed comparable performance, attributed to their similar approach of minimizing regularized risk functions rather than just empirical risk.

## Advantages of the ASVM Approach

The ASVM approach offers several advantages over other forecasting models:

1. Implementation of Structural Risk Minimization (SRM): Unlike BP neural networks that implement Empirical Risk Minimization (ERM), SVM and ASVM minimize an upper bound of generalization error, leading to better prediction performance.
2. Global Optimization: Training SVM is equivalent to solving a linearly constrained quadratic programming problem, ensuring a unique and globally optimal solution. In contrast, BP neural networks can get stuck in local minima.
3. Domain Knowledge Integration: ASVM effectively incorporates financial domain knowledge by assigning more weight to recent data points, aligning with the understanding that recent information is more valuable in predicting non-stationary financial time series.
4. Solution Sparsity: The adaptive parameters in ASVM result in fewer support vectors compared to standard SVM, leading to a more efficient model representation without sacrificing performance.
5. Robust Parameter Sensitivity: ASVM's adaptive approach helps mitigate the sensitivity to parameter selection that affects standard SVM, where improper selection of kernel parameters can cause overfitting or underfitting.

## Conclusion

The research convincingly demonstrates that SVM with adaptive parameters provides a powerful approach for financial time series forecasting. By incorporating the non-stationary characteristic of financial data through ascending regularization constants and descending tube sizes, ASVM achieves superior prediction accuracy with more efficient model representation compared to standard SVM and neural network approaches.

The study highlights how domain-specific knowledge can be effectively integrated into machine learning algorithms to enhance performance. The ASVM approach not only addresses the theoretical challenges of financial forecasting but also offers practical advantages in terms of prediction accuracy and computational efficiency, making it a valuable tool for financial forecasting applications.

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/51651304/621d8fbb-46b9-45c2-b259-2535bd68f6d1/Support_vector_machine_with_adaptive_parameters_in_financial_time_series_forecasting.pdf

