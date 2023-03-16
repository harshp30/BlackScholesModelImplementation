# Options Pricing using Black-Scholes Model with Monte Carlo Simulation

from datetime import datetime
import pandas as pd
import yfinance as yf
import numpy as np

'''
Function to get a specific stock based on started and end date
This returns a data frame containing adjusted closing prices for the specific chosen stock
'''
def get_data(stock, start, end):
    stock_data = {}
    ticker = yf.download(stock, start, end)
    stock_data['price'] = ticker['Adj Close']
    data = pd.DataFrame(stock_data)
    return data


class OptionPricing:

    def __init__(self, S0, E, T, rf, sigma, iterations):
        self.S0 = S0
        self.E = E
        self.T = T
        self.rf = rf
        self.sigma = sigma
        self.iterations = iterations


    '''
    Returns calculated mean call price for an option with the monte carlo simulation
    '''
    def call_option_simulation(self):
        # We have 2 columns: first with 0s the second column will store the payoff
        # we need the first column of 0s: payoff function is max(0,S-E) for call option
        option_data = np.zeros([self.iterations, 2])

        # dimensions: 1 dimensional array with as many items as the iterations
        rand = np.random.normal(0, 1, [1, self.iterations])

        # equation for the S(t) stock price at T
        stock_price = self.S0 * np.exp(self.T * (self.rf - 0.5 * self.sigma ** 2)
                                       + self.sigma * np.sqrt(self.T) * rand)

        # we need S-E because we have to calculate the max(0,S-E)
        option_data[:, 1] = stock_price - self.E

        # calculate average for the Monte-Carlo Simulation
        # max() returns the max(0,S-E) according to the formula
        # THIS IS THE AVERAGE VALUE!
        average = np.sum(np.amax(option_data, axis=1)) / float(self.iterations)

        # have to use the exp(-rT) discount factor [Zero-Coupon Bonds)
        return np.exp(-1.0*self.rf*self.T)*average

    '''
    Returns calculated mean put price for an option with the monte carlo simulation
    '''
    def put_option_simulation(self):
        # We have 2 columns: first with 0s the second column will store the payoff
        # we need the first column of 0s: payoff function is max(0,E-S) for call option
        option_data = np.zeros([self.iterations, 2])

        # dimensions: 1 dimensional array with as many items as the iterations
        rand = np.random.normal(0, 1, [1, self.iterations])

        # equation for the S(t) stock price at T
        stock_price = self.S0 * np.exp(self.T * (self.rf - 0.5 * self.sigma ** 2)
                                       + self.sigma * np.sqrt(self.T) * rand)

        # we need S-E because we have to calculate the max(0,E-S)
        option_data[:, 1] = self.E - stock_price

        # calculate average for the Monte-Carlo Simulation
        # max() returns the max(0,E-S) according to the formula
        # THIS IS THE AVERAGE VALUE!
        average = np.sum(np.amax(option_data, axis=1)) / float(self.iterations)

        # have to use the exp(-rT) discount factor [Zero-Coupon Bonds)
        return np.exp(-1.0*self.rf*self.T)*average


if __name__ == '__main__':
    # Date range is just today since we want to make future predictions
    #   and only need price at time t=0 (today)
    start_date = datetime.today()
    end_date = datetime.today()
    # Using Chase Corporation Stock
    data = get_data('CCF', start_date, end_date)
    price_today = float(data['price'])
    print('The price today is: $%.2f' % price_today)
    # Underlying stock price at t=0
    S0 = price_today
    # Strike price (the price at which a put or call option can be exercised)
    strike_price = float(input('Select the Strike Price: $'))
    E = strike_price
    # Expiry 1 year = 365 days
    T = 1
    # risk-free rate (as of today in USA)
    rf = 0.0355
    # volatility of the underlying stock (a standard deviation of log returns)
    sigma = 0.2
    # Iteration amount for monte carlo simulation
    iterations = int(input('How many iterations would you like to run the simulation for? '))

    model = OptionPricing(S0, E, T, rf, sigma, iterations)
    print('Value of call option: $%.2f' % model.call_option_simulation())
    print('Value of put option: $%.2f' % model.put_option_simulation())
