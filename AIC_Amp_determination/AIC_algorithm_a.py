# coding=utf-8
import numpy as np
from scipy import stats

def AIC_algorithm_a(X):
    shape, loc, scale = stats.lognorm.fit(np.exp(X))
    mu = np.log(scale)
    sigma = shape
    y = np.sum(np.log(stats.lognorm.pdf(X, shape, loc, scale)), axis = 0)
    print(shape)
    print(loc)
    print(scale)
    print('mu')
    print(mu)
    print('sigma')
    print(shape)
    print('y')
    print(y)
    
