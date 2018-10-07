import quandl
import pandas as pd

quandl.ApiConfig.api_key = 'PByrNQUSDzfyx-ncojkB'
# Retrieve the GM data from Quandl
gm = quandl.get('WIKI/BAC')
gm.head(5)

print(gm.describe())

import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

# The adjusted close accounts for stock splits, so that is what we should graph
plt.plot(gm.index, gm['Adj. Close'])
plt.title('GM Stock Price')
plt.ylabel('Price ($)');
plt.show()

gm['Year'] = gm.index.year
# Take Dates from index and move to Date column
gm.reset_index(level=0, inplace=True)

import fbprophet

# Prophet requires columns ds (Date) and y (value)
gm = gm.rename(columns={'Date': 'ds', 'Close': 'y'})
# Put market cap in billions
#gm['y'] = gm['y'] / 1e9
# Make the prophet model and fit on the data
gm_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15,daily_seasonality=True)
gm_prophet.fit(gm)

# Make a future dataframe for 2 years
gm_forecast = gm_prophet.make_future_dataframe(periods=365 * 2, freq='D')
# Make predictions
gm_forecast = gm_prophet.predict(gm_forecast)

gm_prophet.plot(gm_forecast, xlabel = 'Date', ylabel = 'price')
plt.title('Price of BOA');