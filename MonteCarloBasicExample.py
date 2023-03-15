# Predicting Stock prices with Monte-Carlo Simulation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

'''
Function to get a specific stock based on started and end date
This returns a data frame containing adjusted closing prices for the specific chosen stock
'''
def get_data(stock, start, end):
    stock_data = {}
    ticker = yf.download(stock, start, end)
    # Get adjusted closing prices instead of just closing prices
    # This is better compared to just closing prices since it takes into accounts factors such as
    #   dividends, stock splits, and new stock offerings
    stock_data['price'] = ticker['Adj Close']
    data = pd.DataFrame(stock_data)
    return data

'''
Monte Carlo Simulation run and plot
'''
def stock_monte_carlo(S0, mu, sigma, simulation_iterations, N=252):

    result = []

    # number of simulations - possible S(t) realizations (of the process)
    for _ in range(simulation_iterations):
        prices = [S0]
        for _ in range(N):
            # simulate change day by day (t=1)
            stock_price = prices[-1] * np.exp((mu - 0.5 * sigma ** 2) +
                                              sigma * np.random.normal())
            prices.append(stock_price)

        result.append(prices)

    simulation_data = pd.DataFrame(result)
    # the given columns will contain the time series for a given simulation
    simulation_data = simulation_data.T

    simulation_data['mean'] = simulation_data.mean(axis=1)

    plt.plot(simulation_data)
    plt.plot(simulation_data['mean'], color='black', linewidth=2, label='mean')
    plt.legend()
    plt.title('Monte-Carlo Simulation')
    plt.ylabel('Stock Price ($)')
    plt.xlabel('Trading Day (N)')
    plt.show()

    print('Prediction for future stock price: $%.2f' % simulation_data['mean'].tail(1))


if __name__ == '__main__':

    # Date range is just today since we want to make future predictions
    #   and only need price at time t=0 (today)
    start_date = datetime.today()
    end_date = datetime.today()
    # Using Chase Corporation Stock
    data = get_data('TSLA', start_date, end_date)
    price_today = float(data['price'])

    print('Current stock price: $%.2f' % price_today)

    # Underlying stock price at t=0
    S0 = price_today

    mu = 0.0002
    sigma = 0.01
    simulation_iterations = 1000

    stock_monte_carlo(S0, mu, sigma, simulation_iterations)
