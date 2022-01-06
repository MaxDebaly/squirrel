from utils import _simulate
import matplotlib.pyplot as plt
from numpy import random as rd
import math as math
import numpy as np

param = [-1, 0.5, -0.1, -0.2, 0.3, -0.1, -0.12, 0.21, 0]


arValue = 1
laValue = 2
npaths = 501
nbexogen = 5
xarray = rd.exponential(scale = 1, size =(npaths, nbexogen))



simulation = _simulate(parameters=param, ar=arValue, la = laValue, xseries=xarray, link = 'exp', ytransform = 'transform')
print(simulation['latent'])
plt.plot(simulation['latent'], 'b-')
plt.show()

print(simulation['yserie'])
plt.plot(simulation['yserie'], 'r-')
plt.show()


param = [1, 0.5]

simulation = _simulate(parameters=param, ar=arValue, lenpath=npaths, distribution="NB", phi = 0.5)
print(simulation['latent'])
print(simulation['yserie'])

plt.plot(simulation['yserie'], 'r-')
plt.plot(simulation['latent'], 'b-')
plt.show()