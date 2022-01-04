from utils import _simulate
import matplotlib.pyplot as plt
from numpy import random as rd

param = [1, 0.5, 0.1, 0.2, 0.3, 1, 1.2, 2.1, 0]


arValue = 1
laValue = 2
npaths = 501
nbexogen = 5
xarray = rd.exponential(scale = 1, size =(npaths, nbexogen))

simulation = _simulate(parameters=param, ar=arValue, la = laValue, xseries=xarray)
print(simulation['latent'])
print(simulation['yserie'])
plt.plot(simulation['yserie'], 'r-')
plt.plot(simulation['latent'], 'b-')
plt.show()


param = [1, 0.5]

simulation = _simulate(parameters=param, ar=arValue, lenpath=npaths, distribution="NB", phi = 0.5)
print(simulation['latent'])
print(simulation['yserie'])

plt.plot(simulation['yserie'], 'r-')
plt.plot(simulation['latent'], 'b-')
plt.show()