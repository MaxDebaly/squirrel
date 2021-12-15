import numpy as np 

 
def splitParameters(theta, ar, la = None, X = None):
    if not type(theta).__module__ == np.__name__ :
        theta = np.array(theta)
    ## parameters   
    omega = theta[0]
    alpha = theta[1:(ar+1)] ## first element corresponds to the oldest observation
    
    if la and X:
        latentInitiated =  np.ones(la)
        beta = theta[(ar+1):(ar + la + 1)] ## first element corresponds to the oldest lattent process value
        gamma = theta[(ar + la + 1):]
        
        return omega, alpha, beta, gamma, latentInitiated
        
    elif la and not X:
        beta = theta[(ar+1):] ## first element corresponds to the oldest lattent process value
        latentInitiated =   np.ones(la)
        
        if not len(theta) == (ar+la+1):
            raise ValueError("Incorrect number of parameter : length of theta must be equal ar + la + 1")
       
        return omega, alpha, beta, latentInitiated
    
    elif not la and X:
        gamma = theta[(ar+1):]
        return omega, alpha, gamma
    
    
    if not len(theta) == (ar+1):
        raise ValueError("Incorrect number of parameter : length of theta must be equal ar + 1")
    return omega, alpha
        
    
    

def singleLikelihoodPoisson(theta, y, ar, X = None, la = None, link = None):
    lengthT =  len(y) # length of path
    ## value
    likelihood = 0
    parameters = splitParameters(theta, ar = ar, la = la)
    
    
    if len(parameters) == 2 :
        omega, alpha = parameters
    
    elif len(parameters) == 3:
        omega, alpha, gamma = parameters
    
    elif len(parameters) == 4 :
        omega, alpha, beta, latentInitiated = parameters
    
    elif len(parameters) == 5 :
        omega, alpha, beta, gamma, latentInitiated = parameters
        
    
    
      
    for tval in range(ar, lengthT+1):
        lattent = omega + np.sum(alpha * y[(tval-ar):tval])
        
        if la and X:
            lattent +=  np.sum(beta * latentInitiated) + np.sum(gamma * X)
            latentInitiated = np.append(latentInitiated[1:], lattent)
        
        elif la and not X:
            lattent += np.sum(beta * latentInitiated)
            latentInitiated = np.append(latentInitiated[1:], lattent)
            
        elif not la and X:
            lattent += np.sum(gamma * X)
        
        
        if not link or link == "log":
            likelihood += np.exp(lattent) - y[tval] * lattent
        
        elif link == "identity":
            likelihood += lattent -  y[tval] * np.log(lattent)
    
    return likelihood
            
         
        
              
