import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

symbol = 'BANANAS'

data = pd.read_csv("data.csv")
print(data.head())

# Drop all of the PEARLS data
data.drop(data.loc[data['product'] != symbol].index, inplace=True)
print(data.head())

x = data['timestamp'].head(100)
y = data['mid_price'].head(100)

plt.plot(x, y)
plt.xlabel("Time stamp")
plt.ylabel("Mid_Price")
plt.title("Market for " + symbol)
plt.show()
