# coding=utf-8
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

def AIC_algorithm_a(X):
    shape, loc, scale = stats.lognorm.fit(X, floc=0)
    mu = np.log(scale)
    sigma = shape
    y = np.sum(np.log(stats.lognorm.pdf(X, shape, loc, scale)), axis = 0)
    
    print(shape)
    print(loc)
    print(scale)
    print('mu')
    print(mu)
    print('sigma')
    print(sigma)
    print('y')
    print(y)
    
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.hist(X)
    ax = fig.add_subplot(212)
    ax.plot(X, stats.lognorm.pdf(X, shape, loc, scale))
    plt.show()
