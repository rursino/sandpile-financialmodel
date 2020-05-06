import numpy as np
import matplotlib.pyplot as plt
import sandpile

from importlib import reload
reload(sandpile);


"""INPUTS"""
length = 20
width = 20
num_of_avalanches = 100


"""FUNCTIONS"""
def execute_avalanche(sp):
    no_avalanche = True
    while no_avalanche:
        if np.any(sp.grid >= 4):
            sp.avalanche()
            no_avalanche = False
        else:
            sp.drop_sand()

"""EXECUTION"""
sp = sandpile.SandPile(length, width)

for i in range(num_of_avalanches):
    execute_avalanche(sp)

fname = "./output/sandpile_test.pik"
sp.save_avalanche_stats(fname)
ob = sandpile.Observables(fname)

ob.histogram(ob.lost_mass)
plt.plot(ob.mass_history)
plt.imshow(ob.grid)
