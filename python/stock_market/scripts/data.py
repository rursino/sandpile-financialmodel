"""Analysis of data from the financial markets extension phase of the project.
"""


""" IMPORTS """
import pandas as pd
import matplotlib.pyplot as plt

""" S&P 500 """
df = pd.read_csv("./../data/sp500daily.csv",
                index_col = "Date"
                )
df
x = df.index
y1 = df.Open
y2 = df.Volume

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(x, y1)
ax1.set_ylabel('Day Open Price')

ax2 = ax1.twinx()
ax2.plot(x, y2, 'r-')
ax2.set_ylabel('Volume of Units', color='r')
