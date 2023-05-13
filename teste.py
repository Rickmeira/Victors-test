# Import required libraries


import math
import matplotlib.pyplot as plt
import numpy as np
import pandas
from pandas_datareader import data as pdr
import yfinance as yfin
from pandas_datareader import data
import yfinance as yf
import datetime

yfin.pdr_override()
arezzo = pdr.get_data_yahoo('ONCO3.SA')

start = datetime.datetime(2022, 5, 12)
end = datetime.datetime(2023, 5, 12)

arezzo = yf.download('ONCO3.SA',start,end)

#arezzo = data.DataReader('ONCO3.SA', 'yahoo')
#arezzo.head()
arezzo
#Next, we calculate the number of days that have elapsed in our chosen time window
time_elapsed = (arezzo.index[-1] - arezzo.index[0]).days
#Current price / first record (e.g. price at beginning of 2009)
#provides us with the total growth %
total_growth = (arezzo['Adj Close'][-1] / arezzo['Adj Close'][1])

#Next, we want to annualize this percentage
#First, we convert our time elapsed to the # of years elapsed
number_of_years = time_elapsed / 365.0

#Second, we can raise the total growth to the inverse of the # of years
#(e.g. ~1/10 at time of writing) to annualize our growth rate
cagr = total_growth ** (1/number_of_years) - 1

#Now that we have the mean annual growth rate above,
#we'll also need to calculate the standard deviation of the
#daily price changes
std_dev = arezzo['Adj Close'].pct_change().std()

#Next, because there are roughy ~252 trading days in a year,
#we'll need to scale this by an annualization factor
#reference: https://www.fool.com/knowledge-center/how-to-calculate-annualized-volatility.aspx

number_of_trading_days = 252
std_dev = std_dev * math.sqrt(number_of_trading_days)

#From here, we have our two inputs needed to generate random
#values in our simulation
print ("cagr (mean returns) : ", str(round(cagr,4)))
print ("std_dev (standard deviation of return : )", str(round(std_dev,4)))
#Generate random values for 1 year's worth of trading (252 days),
#using numpy and assuming a normal distribution
daily_return_percentages = np.random.normal(cagr/number_of_trading_days, std_dev/math.sqrt(number_of_trading_days),number_of_trading_days)+1

#Now that we have created a random series of future
#daily return %s, we can simply apply these forward-looking
#to our last stock price in the window, effectively carrying forward
#a price prediction for the next year

#This distribution is known as a 'random walk'

price_series = [arezzo['Adj Close'][-1]]

for j in daily_return_percentages:
    price_series.append(price_series[-1] * j)

#Great, now we can plot of single 'random walk' of stock prices
plt.plot(price_series)
plt.show()
#Now that we've created a single random walk above,
#we can simulate this process over a large sample size to
#get a better sense of the true expected distribution
number_of_trials = 100
plt.figure(figsize=(12, 8), dpi = 150)

#set up an additional array to collect all possible
#closing prices in last day of window.
#We can toss this into a histogram
#to get a clearer sense of possible outcomes
closing_prices = []

for i in range(number_of_trials):
    #calculate randomized return percentages following our normal distribution
    #and using the mean / std dev we calculated above
    closing_prices.append(price_series[-1])
    daily_return_percentages = np.random.normal(cagr/number_of_trading_days, std_dev/math.sqrt(number_of_trading_days),
number_of_trading_days)+1
    price_series = [arezzo['Adj Close'][-1]]

    for j in daily_return_percentages:
        #extrapolate price out for next year
        price_series.append(price_series[-1] * j)

    #append closing prices in last day of window for histogram
    closing_prices.append(price_series[-1])

    #plot all random walks
    # plt.figure(figsize=(12, 8), dpi = 150)
    plt.plot(price_series)
    plt.savefig("Random_Walk.jpg")

plt.show()

#plot histogram
# plt.hist(closing_prices,bins=40)

# plt.show()
#from here, we can check the mean of all ending prices
#allowing us to arrive at the most probable ending point

mean_end_price = round(np.mean(closing_prices),2)
print("Expected price: ", str(mean_end_price), closing_prices)

plt.figure(figsize=(12, 8), dpi = 150)

#lastly, we can split the distribution into percentiles
#to help us gauge risk vs. reward

#Pull top 10% of possible outcomes
top_ten = np.percentile(closing_prices,100-10)

#Pull bottom 10% of possible outcomes
bottom_ten = np.percentile(closing_prices,10);

#create histogram again
plt.hist(closing_prices,bins=40, color="red")
#append w/ top 10% line
plt.axvline(top_ten,color='r',linestyle='dashed',linewidth=2)
#append w/ bottom 10% line
plt.axvline(bottom_ten,color='r',linestyle='dashed',linewidth=2)
#append with current price
plt.axvline(mean_end_price,color='g', linestyle='dashed',linewidth=2)

for run in range(100):
    plt.hist(closing_prices,bins=150)
             
# plt.xlabel('Days')
# plt.ylabel('Price')
# plt.title('Monte Carlo Analysis for Arezzo')
#from here, we can check the mean of all ending prices
#allowing us to arrive at the most probable ending point
mean_end_price = round(np.mean(closing_prices),2)
print("Expected price: ", str(mean_end_price))
#lastly, we can split the distribution into percentiles
#to help us gauge risk vs. reward

plt.figure(figsize=(12, 8), dpi = 150)

#Pull top 10% of possible outcomes
top_ten = np.percentile(closing_prices,100-10)

#Pull bottom 10% of possible outcomes
bottom_ten = np.percentile(closing_prices,10);

# create the histogram with different colors for each interval
plt.hist(closing_prices, bins=200, color="#00B5AD")

plt.savefig("Monte_Carlo.jpg")

#append w/ top 10% line
# plt.axvline(top_ten,color='r',linestyle='dashed',linewidth=2)
#append w/ bottom 10% line
# plt.axvline(bottom_ten,color='r',linestyle='dashed',linewidth=2)
#append with current price
# plt.axvline(round(np.mean(closing_prices),2),color='g', linestyle='dashed',linewidth=2)

plt.show()
