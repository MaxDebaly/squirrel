import numpy as np
from utils import _latentProcess
from scipy.optimize import minimize 

class Ingarch:
    def __init__(self, ar, **kwargs):
        self.ar = ar
        
        if 'la' in kwargs:
            self.la = kwargs['la']
            
        if 'xlabels' in kwargs:
            self.xlabels = kwargs['xlabels']
            
        if 'ylabel' in kwargs :
            self.ylabel = kwargs['ylabel']
            

 

    def _estimate(self):
        pass 
    
    def _stderror(self): 
        pass
    
    
    def fit(self):
        pass
    
    
    def summary(self):
        pass
    
    def __str__(self):
        pass
    
    

        
        
    
    