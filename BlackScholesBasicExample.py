# Black-Scholes Model Basic Implementation

from scipy import stats
from numpy import log, exp, sqrt
from datetime import datetime
import pandas as pd
import yfinance as yf

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
Returns calculated call price for an option
'''
def call_option_price(S, E, T, rf, sigma):
    # first we have to calculate the d1 and d2 parameters
    d1 = (log(S/E)+(rf+sigma*sigma/2.0)*T)/(sigma*sqrt(T))
    d2 = d1-sigma*sqrt(T)
    print('The d1 and d2 parameters: %s, %s'% (d1, d2))
    # Use the N(x) to calculate the price of the option
    return S*stats.norm.cdf(d1)-E*exp(-rf*T)*stats.norm.cdf(d2)

'''
Returns calculated put price for an option
'''
def put_option_price(S, E, T, rf, sigma):
    # first we have to calculate the d1 and d2 parameters
    d1 = (log(S/E)+(rf+sigma*sigma/2.0)*T)/(sigma*sqrt(T))
    d2 = d1-sigma*sqrt(T)
    print('The d1 and d2 parameters: %s, %s'% (d1, d2))
    # Use the N(x) to calculate the price of the option
    return -S*stats.norm.cdf(-d1)+E*exp(-rf*T)*stats.norm.cdf(-d2)


if __name__ == '__main__':

    # Date range is just today since we want to make future predictions
    #   and only need price at time t=0 (today)
    start_date = datetime.today()
    end_date = datetime.today()
    # Using Chase Corporation Stock
    data = get_data('CCF', start_date, end_date)
    price_today = float(data['price'])

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

    print("Call option according to the Black-Scholes model: ",
          call_option_price(S0, E, T, rf, sigma))

    print("Put option according to the Black-Scholes model: ",
          put_option_price(S0, E, T, rf, sigma))
