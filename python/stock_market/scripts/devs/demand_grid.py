""" This script shows the plots that make up the demand and magnitude
probabilities.
"""


""" IMPORTS """
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

""" EXECUTION """
n = 50
x = np.arange(0, n+1)
y = 0.8 * stats.norm.cdf(x=x,
                        loc=0.5*n,
                        scale=0.2*n
                        )
plt.figure(figsize=(20,10))
plt.plot(x, y); plt.plot(x, 0.8-y)
plt.title("Probability of three events vs. Units held by an investor",
            fontsize=24)
plt.xlabel("Units held by an investor", fontsize=16)
plt.ylabel("Probability", fontsize=16)

units = 50
p = 1 - stats.powerlaw.cdf(x=np.arange(units*0.25),
                        a = 0.1,
                        loc = 0,
                        scale = units
                        )
p = np.concatenate([p, 0.0 + np.zeros(int(units*0.75))])
p /= sum(p)

plt.figure(figsize=(20,10))
plt.plot(p); plt.xlim([0, units])
plt.title("Probability of units to transact",
            fontsize=24)
plt.xlabel("Units held by an investor", fontsize=16)
plt.ylabel("Probability", fontsize=16)

np.random.choice(units, p=p)
