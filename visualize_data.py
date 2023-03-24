import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# symbol = 'BANANAS'

data_day0 = pd.read_csv("Data/prices_round_2_day_-1.csv")
data_day_1 = pd.read_csv("Data/prices_round_2_day_0.csv")
data_day_2 = pd.read_csv("Data/prices_round_2_day_1.csv")
data_day_1['timestamp'] = data_day_1['timestamp'] + 1000000
data_day_2['timestamp'] = data_day_2['timestamp'] + 2 * 1000000
data_unfiltered = pd.concat([data_day0, data_day_1, data_day_2], ignore_index=True)
data_unfiltered.to_csv("Data/all_3_days_round2.csv")

## Getting the data for the specified symbol by finding each day's data, then concatenating
# x0 = data_day0.drop(data_day0.loc[data_day0['product'] != symbol].index)['timestamp']
# y0 = data_day0.drop(data_day0.loc[data_day0['product'] != symbol].index)['mid_price']
# x_1 = data_day_1.drop(data_day_1.loc[data_day_1['product'] != symbol].index)['timestamp']
# y_1 = data_day_1.drop(data_day_1.loc[data_day_1['product'] != symbol].index)['mid_price']
# x_2 = data_day_2.drop(data_day_2.loc[data_day_2['product'] != symbol].index)['timestamp']
# y_2 = data_day_2.drop(data_day_2.loc[data_day_2['product'] != symbol].index)['mid_price']
#
# x = pd.concat([x_2, x_1, x0])
# y = pd.concat([y_2, y_1, y0])

## Outputting data specific to each symbol
# data = pd.concat([data_day_2, data_day_1, data_day0])
# data['timestamp'] = x
# print(data.tail())
# data.to_csv("Data/" + symbol + "_3_days.csv")

# Mid price is calculate from the average of the largest bid and smallest ask prices for that timestamp
# x_pearls = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'PEARLS'].index)['timestamp']
# y_pearls = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'PEARLS'].index)['mid_price']
# # pearl_max_buy = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'PEARLS'].index)['bid_price_1']
# # pearl_min_sell = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'PEARLS'].index)['ask_price_1']
# x_bananas = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'BANANAS'].index)['timestamp']
# y_bananas = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'BANANAS'].index)['mid_price']
# bananas_max_buy = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'BANANAS'].index)['bid_price_1']
# bananas_min_sell = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'BANANAS'].index)['ask_price_1']

# x_coconuts = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'COCONUTS'].index)['timestamp']
# y_coconuts = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'COCONUTS'].index)['mid_price']
# x_pinas = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'PINA_COLADAS'].index)['timestamp']
# y_pinas = data_unfiltered.drop(data_unfiltered.loc[data_unfiltered['product'] != 'PINA_COLADAS'].index)['mid_price']
y_pinas = pd.Series

for i in range(20):
    if data_unfiltered.iloc[i]["product"] == "PINA_COLADAS":
        # print(data_unfiltered.iloc[i]["mid_price"])
        y_pinas.append([data_unfiltered.iloc[i]["mid_price"]], ignore_index=True)

## Plotting data for PEARLS and BANANAS side by side
# figure, axis = plt.subplots(1, 2)
# axis[0].plot(x_pearls, y_pearls)
# axis[0].set_xlabel("Time stamp")
# axis[0].set_ylabel("Mid_Price")
# axis[0].set_title("Market for PEARLS")
#
# axis[1].plot(x_bananas, y_bananas)
# axis[1].set_xlabel("Time stamp")
# axis[1].set_ylabel("Mid_Price")
# axis[1].set_title("Market for BANANAS")

amt = 100
# figure, axis = plt.subplots(1, 2)
# axis[0].plot(x_pinas, y_pinas)
# axis[1].plot(x_coconuts, y_coconuts)
# plt.plot(x_pinas, ratio)
# plt.plot(x_pinas, y_pinas)
# plt.plot(x_pinas, ratio)

# plt.xlabel("Time stamp")
# plt.ylabel("Mid_Price")
plt.title("Market")
# plt.show()
