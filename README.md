# cir-model
Cox-Ingersoll-Ross interest rates movement Model in Python

tickers:

^IRX: 13-week T-Bill

^FVX: 5y Treasury yield

^TYX: 30y Treasury yield

The CIR model assumes interest rates follow a mean-reverting process. However, the variance of rate changes differs depending on the level of rates.
The CIR model uses the following formula to describe the interest rate process:
dr 
t
​
 =k(θ−r 
t
​
 )dt+σ 
r 
t
​
 
​
 dZ.
