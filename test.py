import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv("data.csv")
x = data['timestamp'].head(100)
y = data['mid_price'].head(100)

plt.plot(x, y)
plt.show()
