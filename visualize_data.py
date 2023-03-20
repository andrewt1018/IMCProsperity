import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

symbol = 'BANANAS'

data_day0 = pd.read_csv("Data/prices_round_1_day_0.csv")
data_day_1 = pd.read_csv("Data/prices_round_1_day_-1.csv")
data_day_2 = pd.read_csv("Data/prices_round_1_day_-2.csv")


data_day0.drop(data_day0.loc[data_day0['product'] != symbol].index, inplace=True)
data_day_1.drop(data_day_1.loc[data_day_1['product'] != symbol].index, inplace=True)
data_day_2.drop(data_day_2.loc[data_day_2['product'] != symbol].index, inplace=True)
print(data_day0.head())

# Day -2 is the start of the data
x_2 = data_day_2['timestamp']
y_2 = data_day_2['mid_price']

# Recording data for day -1 // 1 day after beginning
x_1 = data_day_1['timestamp'] + 1000000  # Each new day increments the timestamp by 100
y_1 = data_day_1['mid_price']

# Recording data for day 0 // 2 days after beginning
x0 = data_day0['timestamp'] + 2 * 1000000
y0 = data_day0['mid_price']

x = pd.concat([x_2, x_1, x0])
y = pd.concat([y_2, y_1, y0])

data = pd.concat([data_day_2, data_day_1, data_day0])
data['timestamp'] = x
print(data.tail())
data.to_csv("Data/" + symbol + "_3_days.csv")

plt.plot(x, y)
plt.xlabel("Time stamp")
plt.ylabel("Mid_Price")
plt.title("Market for " + symbol)
plt.show()
