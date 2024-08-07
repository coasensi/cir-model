import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import minimize
from scipy.stats import norm
from matplotlib.backends.backend_pdf import PdfPages

################## CIR Model ##################

def fetch_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data['Adj Close']

# estimate cir model parameters
def cir_mle(params, rates):
    a, b, sigma = params
    n = len(rates)
    dt = 1
    # likelihood calculation
    likelihood = 0
    for i in range(1, n):
        rt = rates[i-1]
        drt = rates[i] - rates[i-1]
        # mean and variance of the normal distribution
        mean = a * (b - rt) * dt
        variance = sigma**2 * rt * dt
        # avoid zero variance
        if variance == 0:
            continue
        # log-likelihood
        likelihood += -0.5 * np.log(2 * np.pi * variance) - (drt - mean)**2 / (2 * variance)
    return -likelihood

# simulate cir paths
def simulate_cir(a, b, sigma, r0, T, dt, n_paths):
    n_steps = int(T / dt)
    rates = np.zeros((n_steps, n_paths))
    rates[0] = r0
    for t in range(1, n_steps):
        Z = np.random.normal(size=n_paths)
        rates[t] = rates[t-1] + a * (b - rates[t-1]) * dt + sigma * np.sqrt(rates[t-1] * dt) * Z
        rates[t] = np.maximum(rates[t], 0) 
    return rates

# pdf report
def generate_pdf(ticker, start_date, end_date):
    rates = fetch_data(ticker, start_date, end_date).dropna().values
    initial_params = [0.1, np.mean(rates), 0.1]
    # fit cir model to data
    result = minimize(cir_mle, initial_params, args=(rates,), bounds=[(0, None), (0, None), (0, None)])
    a, b, sigma = result.x
    
    # simulate interest rate paths
    r0 = rates[-1]  # start simulation from the last observed rate
    T = 1  # simulate for 1 year
    dt = 1/252  # daily steps
    n_paths = 20  # number of simulation paths
    simulated_rates = simulate_cir(a, b, sigma, r0, T, dt, n_paths)
    
    # create pdf report
    pdf_file = f"{ticker}_CIR_Model_Report.pdf"
    with PdfPages(pdf_file) as pdf:
        plt.figure(figsize=(12, 6))
        plt.plot(simulated_rates)
        plt.title(f"Simulated Interest Rate Paths Using CIR Model for {ticker}")
        plt.xlabel("Time Steps (Days)")
        plt.ylabel("Interest Rate")
        pdf.savefig()  # save the current figure into a pdf page
        plt.close()

    # uncomment the following block to display graph in the console
    # plt.figure(figsize=(12, 6))
    # plt.plot(simulated_rates)
    # plt.title("Simulated Interest Rate Paths Using CIR Model")
    # plt.xlabel("Time Steps (Days)")
    # plt.ylabel("Interest Rate")
    # plt.show()

# generate report;change the ticker variable to your yfinance ticker symbol
ticker = "^IRX"
start_date = "2020-01-01"
end_date = "2024-08-01"
generate_pdf(ticker, start_date, end_date)

