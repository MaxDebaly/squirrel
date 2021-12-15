from utils import singleLikelihoodPoisson
import numpy as np
from numpy.random import randn
from scipy.optimize import minimize 

class Ingarch:
    def __init__(self, model):
        self.ar = model.ar 
        if model.la:
            self.la = model.la
          
    
    def fit(self, y, X=None, link = None):
        self.y = y
        self.X = X
        self.link = link
         
        ##initialization
        if X:
            self.numberOfParameters = 1 + self.ar + self.la, len(X)
            thetaInit = randn(self.numberOfParameters)
        else:
            self.numberOfParameters = 1 + self.ar + self.la
            thetaInit = randn(1 + self.ar + self.la) 
            
        if link == "identity":
            thetaInit = np.abs(thetaInit)
        
        ##minimization
        # y, ar, X = None, la = None, link = None
        if not link == "identity":
            opt = minimize(singleLikelihoodPoisson, thetaInit, args = (y = self.y, self.ar, X = self.X, la = self.la, link = self.link), method = "L-BFGS-B") 
            self.parameters = opt.x 
            self.convergence = opt.success 
            self.optimization_message = opt.message
        
        
    