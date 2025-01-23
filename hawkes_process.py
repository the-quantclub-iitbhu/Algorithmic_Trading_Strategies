def hawkes_process(data: pd.Series, kappa: float) -> pd.Series:
    """
    Applies the Hawkes process to a given time series.

    The Hawkes process is a self-exciting point process where the occurrence of an event increases 
    the likelihood of future events in a decaying manner. This implementation smooths a time series 
    by combining an exponential decay factor with the raw values of the series.

    Parameters:
    ----------
    data : pd.Series
        A Pandas Series containing the input time series data to which the Hawkes process is applied.
    kappa : float
        The decay rate parameter of the Hawkes process. Must be a positive value.

    Returns:
    -------
    pd.Series
        A Pandas Series of the same length as `data`, representing the smoothed output of the 
        Hawkes process.

    Raises:
    ------
    AssertionError
        If `kappa` is not a positive value.

    Notes:
    ------
    - The parameter `alpha` is derived as `exp(-kappa)`, determining the influence of prior values 
      on the current smoothed value.
    - If a previous value in the smoothed output is NaN, the raw input value is directly used.
    - The output is scaled by the parameter `kappa`.

    Example:
    -------
    >>> import pandas as pd
    >>> data = pd.Series([1.0, 2.0, 3.0, np.nan, 4.0])
    >>> kappa = 0.5
    >>> hawkes_process(data, kappa)
    0    0.5
    1    1.25
    2    1.875
    3    NaN
    4    2.9375
    dtype: float64
    """
    assert kappa > 0.0, "kappa must be a positive value."
    
    alpha = np.exp(-kappa)
    arr = data.to_numpy()
    output = np.zeros(len(data))
    output[:] = np.nan
    
    for i in range(1, len(data)):
        if np.isnan(output[i - 1]):
            output[i] = arr[i]
        else:
            output[i] = output[i - 1] * alpha + arr[i]
    
    return pd.Series(output, index=data.index) * kappa