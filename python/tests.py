import numpy as np
import matplotlib.pyplot as plt
import sandpile

from importlib import reload
reload(sandpile);

a = sandpile.SandPile(20,20)

num_of_iters = 100
for _ in range(num_of_iters):
    n = np.random.randint(1,3)
    a.drop_sand(n)
# a.visualise()

a.avalanche("fail")

a.avalanche_stats
