import numpy as np
import numpy.random as rd
import warnings
import  math as math




def _latentProcess(parameters, yserie, ar, la = None, xseries = None):
    yserie = yserie if isinstance(yserie, np.ndarray) else np.array(yserie)
    xseries = xseries if isinstance(xseries, np.np.ndarray) else np.array(xseries)
    latent = np.mean(yserie[:ar]) if la is None else np.ones(la)*np.mean(yserie[:ar])
    lengthT = len(yserie)
    for titer in range(ar, lengthT+1):
        nextLatent = parameters[0] + np.sum(yserie[(titer-ar):titer] * parameters[1:(ar + 1)])
        nextLatent = nextLatent + np.sum(latent[(titer-la):titer] * parameters[(ar + 1):(ar + la + 1)]) if not la is None else nextLatent
        nextLatent = nextLatent + np.sum(xseries[titer, :] * parameters[(ar + la + 1):]) if not la is None and not  xseries is  None else nextLatent
        nextLatent = nextLatent + np.sum(xseries[titer, :] * parameters[(ar + 1):]) if la is None and not xseries is None else nextLatent
        latent = np.append(latent, nextLatent)
    
    return latent  




def _simulate(parameters, ar, lenpath = None, distribution = 'Poisson', yinit = None, link = None, la = None, xseries = None, **kwargs):
    
  
    xseries = xseries if isinstance(xseries, np.ndarray) else np.array(xseries)
    
    if not lenpath and not xseries.all():
        raise ValueError("one of lenpath and xseries is required")
    
    if not lenpath and xseries.all():
        lenpath = xseries.shape[0]
        
    if  xseries.all()  and not lenpath == len(xseries):
        warnings.warn("lenpath must be equal to the number or rows of xseries, only len(xseries) is considered ")
        lenpath = len(xseries) 
         
    if 'phi' in kwargs:
        if not 1-kwargs['phi']>0:
            raise ValueError('The value of phi must be in (0,1)')
    if yinit is None:
        yinit = np.ones(ar)
    elif len(yinit) == 1:
        yinit *= np.ones(ar)
    elif len(yinit) < ar:
        yinit = np.mean(np.array(yinit)) * np.ones(ar) if not isinstance(yinit, np.ndarray) else np.mean(yinit) * np.ones(ar)
        warnings.warn("the length of yinit is less than ar : we consider constant vector of mean value of yinit")
    
    yserie = yinit
    latent = np.mean(yserie[:ar]) if la is None else np.ones(la)*np.mean(yserie[:ar])
    lengthT = 2 * lenpath
    
    parameters = np.array(parameters) if not isinstance(parameters, np.ndarray) else parameters
    
    lenParam = 1 + ar
     
    if la:
        lenParam +=  la
    
    if xseries.all():
        lenParam += xseries.shape[1]

     

    
    if not len(parameters) == lenParam :
        raise ValueError("Incorrect length of parameters vector")
    
    for titer in range(ar, lengthT+1):
        if titer == lenpath + ar    and  xseries.all() :
            break
        
        if 'ytransform' in kwargs and hasattr(np, kwargs['ytransform']):
            nextLatent = parameters[0] + np.sum(np.flip(eval(f"np.{kwargs['ytransform']}({yserie[-ar:]})")) * parameters[1:(ar + 1)]) 
        elif 'ytransform' in kwargs and not hasattr(np, kwargs['ytransform']):
            nextLatent = parameters[0] + np.sum(np.flip(eval(f"{kwargs['ytransform']}({yserie[-ar:]})")) * parameters[1:(ar + 1)]) 
        else :
            nextLatent = parameters[0] + np.sum(np.flip(yserie[-ar:]) * parameters[1:(ar + 1)])
        
        if  la  : 
            nextLatent += np.sum(np.flip(latent[-la:]) * parameters[(ar + 1):(ar + la + 1)])
        else: 
            nextLatent += 0
        if  la  and  xseries.all():
            nextLatent = nextLatent + np.sum(xseries[titer-ar, :] * parameters[(ar + la + 1):])
        else:
            nextLatent += 0  
        if not la  and  xseries.all()  :
            nextLatent = nextLatent + np.sum(xseries[titer-ar, :] * parameters[(ar + 1):])
        else: 
            nextLatent += 0
        latent = np.append(latent, nextLatent)
        
        try:
            if link is None :
                nextMean = nextLatent
            elif hasattr(np,link) :
                nextMean = eval(f"np.{link}({nextLatent})")
            else:
                nextMean = eval(f"{link}({nextLatent})")
        except ValueError:
            raise ValueError(f"Invalid value encounter in mean process, please check the values of parameters : {parameters}")
             
             
        if link is None :
            nextMean = nextLatent
        elif hasattr(np,link) :
            nextMean = eval(f"np.{link}({nextLatent})")
        else:
            nextMean = eval(f"{link}({nextLatent})")
        
        if not nextMean > 0 :
            raise ValueError("The mean process must be positive")
            
        nextY = rd.negative_binomial(nextMean * kwargs['phi']/(1-kwargs['phi']), kwargs['phi']) if distribution == "NB" and 'phi' in kwargs else rd.poisson(lam=nextMean, size=1)

        yserie = np.append(yserie, nextY)
    
    return {'latent': latent[-lenpath:], 'yserie': yserie[-lenpath:]}  



def transform(x) :
    return np.array([math.log(1+y) for y in x])

def _derivativesLatent(parameters, yinit, ar, la = None, xseries = None):
    pass 
    