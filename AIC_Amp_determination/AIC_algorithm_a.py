# coding=utf-8
import numpy as np
from scipy import stats

from AIC_ruisi_a import AIC_ruisi_a

def AIC_algorithm_a(X):
    try:
        shape, loc, scale = stats.lognorm.fit(X, floc = 0)
        pd_logn_mu = np.log(scale)
        pd_logn_sigma = shape
        aic_logn = AIC_ruisi_a('lognorm', X, shape, loc, scale)
        pd1 = np.array([1, pd_logn_mu, pd_logn_sigma, 0]).reshape(4, 1)
    except:
        aic_logn = 1e9
        pd1 = np.array([1, 0, 0, 0]).reshape(4, 1)
        
    try:
        nu, loc, scale = stats.nakagami.fit(X, floc = 0)
        pd_nak_mu = nu
        pd_nak_omega = scale
        aic_nak = AIC_ruisi_a('nakagami', X, nu, loc, scale)
        pd2 = np.array([2, pd_nak_mu, pd_nak_omega, 0]).reshape(4, 1)
    except:
        aic_nak = 1e9
        pd2 = np.array([2, 0, 0, 0]).reshape(4, 1).reshape(4, 1)
        
    try:
        b, loc, scale = stats.rice.fit(X, floc = 0)
        pd_rice_s = b * scale
        pd_rice_sigma = scale
        aic_rice = AIC_ruisi_a('rice', X, b, loc, scale)
        pd3 = np.array([3, pd_rice_s, pd_rice_sigma, 0]).reshape(4, 1)
    except:
        aic_rice = 1e9
        pd3 = np.array([3, 0, 0, 0]).reshape(4, 1).reshape(4, 1)
        
    try:
        loc, scale = stats.rayleigh.fit(X, floc = 0)
        pd_ray_B = scale
        aic_ray = AIC_ruisi_a('rayleigh', X, loc, scale)
        pd4 = np.array([4, pd_ray_B, 0, 0]).reshape(4, 1)
    except:
        aic_ray = 1e9
        pd4 = np.array([4, 0, 0, 0]).reshape(4, 1)
        
    try:
        c, loc, scale = stats.weibull_min.fit(X, floc = 0)
        pd_weib_A = scale
        pd_weib_B = c
        aic_weib = AIC_ruisi_a('weibull', X, c, loc, scale)
        pd5 = np.array([5, pd_weib_A, pd_weib_B, 0]).reshape(4, 1)
    except:
        aic_weib = 1e9
        pd5 = np.array([5, 0, 0, 0]).reshape(4, 1)
        
    full_aic_weights = np.array([aic_logn, aic_nak, aic_rice, aic_ray, aic_weib]).flatten()
    sub_weights = full_aic_weights[:]
    value = np.min(full_aic_weights)
    index = np.where(full_aic_weights == value)[0]
    sub_weights[index] = np.max(full_aic_weights)
    sub_value = np.min(sub_weights)
    sub_index = np.where(sub_weights == sub_value)[0]
    pd_information = np.array([pd1, pd2, pd3, pd4, pd5])
    
    if index + 1 == 1:
        print('Best distribution Fit is: Lognormal distribution')
        pd = pd1
    elif index + 1 == 2:
        print('Best distribution Fit is: Nakagami distribution')
        pd = pd2
    elif index + 1 == 3:
        print('Best distribution Fit is: Rician distribution')
        pd = pd3
    elif index + 1 == 4:
        print('Best distribution Fit is: Rayleigh distribution')
        pd = pd4
    elif index + 1 == 5:
        print('Best distribution Fit is : Weibull distribution')
        pd = pd5
        
    if sub_index + 1 == 1:
        print('Best distribution Fit is: Lognormal distribution')
    elif sub_index + 1 == 2:
        print('Best distribution Fit is: Nakagami distribution')
    elif sub_index + 1 == 3:
        print('Best distribution Fit is: Rician distribution')
    elif sub_index + 1 == 4:
        print('Best distribution Fit is: Rayleigh distribution')
    elif sub_index + 1 == 5:
        print('Best distribution Fit is : Weibull distribution')
        
    return full_aic_weights,pd_information,index,sub_index,aic_logn,aic_nak,aic_rice,aic_ray,aic_weib
    
    #shape, loc, scale = stats.lognorm.fit(X, floc = 0)
    #pd_logn_mu = np.log(scale)
    #pd_logn_sigma = shape
    #pd_logn_y = np.sum(np.log(stats.lognorm.pdf(X, shape, loc, scale)), axis = 0)
    #AIC_ruisi_a('lognorm', X, shape, loc, scale)
    
    
    #nu, loc, scale = stats.nakagami.fit(X, floc = 0)
    #pd_nak_mu = nu
    #pd_nak_omega = scale
    #pd_nak_y = np.sum(np.log(stats.nakagami.pdf(X, nu, loc, scale)), axis = 0)
    #AIC_ruisi_a('nakagami', X, nu, loc, scale)
    
    #b, loc, scale = stats.rice.fit(X, floc = 0)
    #pd_rice_s = b * scale
    #pd_rice_sigma = scale
    #pd_rice_y = np.sum(np.log(stats.rice.pdf(X, b, loc, scale)), axis = 0)
    #AIC_ruisi_a('rice', X, b, loc, scale)
    
    #loc, scale = stats.rayleigh.fit(X, floc = 0)
    #pd_ray_B = scale
    #pd_ray_y = np.sum(np.log(stats.rayleigh.pdf(X, loc, scale)), axis = 0)
    #AIC_ruisi_a('rayleigh', X, loc, scale)
    
    #c, loc, scale = stats.weibull_min.fit(X, floc = 0)
    #pd_weib_A = scale
    #pd_weib_B = c
    #pd_weib_y = np.sum(np.log(stats.weibull_min.pdf(X, c, loc, scale)), axis = 0)
    #AIC_ruisi_a('weibull', X, c, loc, scale)
    
    #print('pd_logn_mu')
    #print(pd_logn_mu)
    #print('pd_logn_sigma')
    #print(pd_logn_sigma)
    #print('aic_logn')
    #print(aic_logn)
    #print('pd_nak_mu')
    #print(pd_nak_mu)
    #print('pd_nak_omega')
    #print(pd_nak_omega)
    #print('aic_nak')
    #print(aic_nak)
    #print('pd_rice_s')
    #print(pd_rice_s)
    #print('pd_rice_sigma')
    #print(pd_rice_sigma)
    #print('aic_rice')
    #print(aic_rice)
    #print('pd_ray_B')
    #print(pd_ray_B)
    #print('aic_ray')
    #print(aic_ray)
    #print('pd_weib_A')
    #print(pd_weib_A)
    #print('pd_weib_B')
    #print(pd_weib_B)
    #print('aic_weib')
    #print(aic_weib)
    #print('full_aic_weights')
    #print(full_aic_weights.shape)
    #print(full_aic_weights)
    #print('pd_information')
    #print(pd_information.shape)
    #print(pd_information)
