import numpy as np
from scipy import stats

from err_info_dic import err_info

def AIC_ruisi_a(*varargin):
    if len(varargin) > 6:
        print(err_info[0x01])
        raise
    
    if len(varargin) == 5:
        K = 2
        if varargin[0] == 'lognorm':
            y = np.sum(np.log(stats.lognorm.pdf(varargin[1], varargin[2], varargin[3], varargin[4])), axis = 0)
        elif varargin[0] == 'nakagami':
            y = np.sum(np.log(stats.nakagami.pdf(varargin[1], varargin[2], varargin[3], varargin[4])), axis = 0)
        elif varargin[0] == 'rice':
            y = np.sum(np.log(stats.rice.pdf(varargin[1], varargin[2], varargin[3], varargin[4])), axis = 0)
        elif varargin[0] == 'weibull':
            y = np.sum(np.log(stats.weibull_min.pdf(varargin[1], varargin[2], varargin[3], varargin[4])), axis = 0)
    elif len(varargin) == 4:
        K = 1
        if varargin[0] == 'rayleigh':
            y = np.sum(np.log(stats.rayleigh.pdf(varargin[1], varargin[2], varargin[3])), axis = 0)
    else:
        K = 3 
        print(err_info[0x02])
        raise
    
    # Now compute the AICc
    n = np.shape(varargin[1])[0]
    AICc = -2 * ( y ) + 2 * K + ( 2 * K * ( K + 1 ) ) / ( n - K - 1);
    
    # This may happen when rician or twdp mle doesn't converge, in this case make AICc
    # arbitarily large
    if np.isnan(AICc):
        AICc = 1000000
        
    return AICc
    
    
if __name__ == '__main__':
    try:
        AIC_ruisi_a(1, 2, 3, 4, 5, 6)
    except:
        print('raise success')
    