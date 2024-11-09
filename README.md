# cir-model
Cox-Ingersoll-Ross interest rates movement Model in Python

tickers:

^IRX: 13-week T-Bill

^FVX: 5y Treasury yield

^TYX: 30y Treasury yield

The CIR model assumes interest rates follow a mean-reverting process. However, the variance of rate changes differs depending on the level of rates. 

d rt = k(θ − rt) dt + σ√(rt) dZ

rt: level of rates at time t
θ: long-run mean rate

> when the rates equal the long-term mean, the drift term thus equals 0. k is the speed at which the rates revert to the mean.

σ: rates volatility
Z: Weiner process (normally distributed)

In the CIR Model, the random component also depends on the rates rt. As the rates decrease, the volatility term thus decreases, reducing the impact of downward rate fluctuations near 0 and thus preventing negative rates.
