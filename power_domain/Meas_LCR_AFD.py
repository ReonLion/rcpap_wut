# coding=utf-8

import numpy as np

def Meas_LCR_AFD(Small_scale_fading):
    menxian_b = 2
    max_lim = np.max(10 * np.log10(Small_scale_fading), axis = 0)
    min_lim = np.min(10 * np.log10(Small_scale_fading), axis = 0)
    Max_lim = 10 ** ((max_lim + menxian_b) / 10)
    Min_lim = 10 ** ((min_lim - menxian_b) / 10)
    interval = 600
    thre_num = np.linspace(Min_lim, Max_lim, interval, endpoint = True)
    
    Threshold = []
    LCR = []
    AFD = []
    x = []
    for i in range(0, interval):
        threshold = thre_num[i]
        Threshold.append(threshold)
        aa = Small_scale_fading - threshold
        length_num = np.shape(Small_scale_fading)[0]
        if np.min(aa, axis = 0) > 0:
            LCR.append(0)
            AFD.append(0)
        elif np.max(aa, axis = 0) < 0:
            LCR.append(0)
            AFD.append(length_num)
        else:
            cishu = 0
            k = []
            for num in range(0, length_num - 1):
                if aa[num] * aa[num + 1] <= 0:
                    x1 = num + 1
                    y1 = aa[num]
                    x2 = num + 1 + 1
                    y2 = aa[num + 1]
                    k.append((y2 - y1) / (x2 - x1))
                    b = y1 - k[cishu] * x1
                    
                    if len(x) == 0:
                        x.append(-b / k[cishu])
                    elif len(x) > 0:
                        if cishu <= len(x) - 1:
                            x[cishu] = -b / k[cishu]
                        else:
                            x.append(-b / k[cishu])
                            
                    cishu += 1
            
            k = np.array(k).astype('float')
            
            LCR.append(np.where(k >= 0)[-1].shape[0])
            lim_low = np.min(np.where(k > 0)[0] + 1, axis = 0)
            lin_up = np.max(np.where(k < 0)[0] + 1, axis = 0)
            time = []
            num = lim_low.copy()
            while num + 2 <= lin_up:
                time.append(x[num + 2 -1] - x[num + 1 -1])
                num = num + 2
            time = np.array(time).astype('float')
            if k[0] > 0:
                time = np.append(x[0] - 0, time)
            else:
                time = np.append(x[1] - x[0], time)
            
            if k[np.shape(k)[-1] - 1] > 0:
                time = np.append(time, k[np.shape(k)[-1] - 1] - k[lin_up - 1])
            else:
                time = np.append(time, length_num - k[np.shape(k)[-1] - 1])
            AFD.append(np.mean(time, axis = 0))
        # else结束
    # for循环结束
    x = np.array(x).astype('float')
    
    LCR = np.array(LCR)
    AFD = np.array(AFD)
    Threshold = np.array(Threshold)
    return LCR, AFD, Threshold
