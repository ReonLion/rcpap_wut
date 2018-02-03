# coding=utf-8
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

def AIC_algorithm_a(X):
    shape, loc, scale = stats.lognorm.fit(X, floc = 0)
    pd_logn_mu = np.log(scale)
    pd_logn_sigma = shape
    pd_logn_y = np.sum(np.log(stats.lognorm.pdf(X, shape, loc, scale)), axis = 0)
    
    nu, loc, scale = stats.nakagami.fit(X, floc = 0)
    pd_nak_mu = nu
    pd_nak_omega = scale
    pd_nak_y = np.sum(np.log(stats.nakagami.pdf(X, nu, loc, scale)), axis = 0)
    
    b, loc, scale = stats.rice.fit(X, floc = 0)
    pd_rice_s = b * scale
    pd_rice_sigma = scale
    pd_rice_y = np.sum(np.log(stats.rice.pdf(X, b, loc, scale)), axis = 0)
    
    print(b)
    print(loc)
    print(scale)
    print('pd_logn_mu')
    print(pd_logn_mu)
    print('pd_logn_sigma')
    print(pd_logn_sigma)
    print('pd_logn_y')
    print(pd_logn_y)
    print('pd_nak_mu')
    print(pd_nak_mu)
    print('pd_nak_omega')
    print(pd_nak_omega)
    print('pd_nak_y')
    print(pd_nak_y)
    print('pd_rice_s')
    print(pd_rice_s)
    print('pd_rice_sigma')
    print(pd_rice_sigma)
    print('pd_rice_y')
    print(pd_rice_y)
    
    
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.hist(X)
    ax = fig.add_subplot(212)
    ax.plot(X, stats.rice.pdf(X, b, loc, scale))
    plt.show()
