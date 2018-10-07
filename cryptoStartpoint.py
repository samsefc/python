# cryptos:

import fbprophet
import pandas


btcusd = pandas.read_csv("C:\\temp\\kdb\\btcusd.csv")
btcusd.describe()


btcusd = btcusd.rename(columns={'time': 'ds', 'close': 'y'})

btcusd_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15,daily_seasonality=True)
btcusd_prophet.fit(btcusd)

# Make a future dataframe for 2 years
btcusd_forecast = btcusd_prophet.make_future_dataframe(periods=365 * 2, freq='D')
# Make predictions
btcusd_forecast = btcusd_prophet.predict(btcusd_forecast)

btcusd_prophet.plot(btcusd_forecast, xlabel = 'Date', ylabel = 'price')
plt.title('Price Prediction BTCUSD');



