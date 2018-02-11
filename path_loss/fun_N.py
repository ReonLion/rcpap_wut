# coding=utf-8
import numpy as np

def fun_N(gama):
    if gama > 6:
        N = 1
        N_db = 0
    elif gama <= 6:
        P = np.array([-0.0480, 1.0875, 4.0782, -0.8806])
        gama_s = np.arange(0.3, 0.8 + 0.01 / 1e5, 0.01)
        Fs_dB = P[0] * gama_s ** 3 + P[1] * gama_s ** 2 + P[2] * gama_s + P[3]
        N_db_s = -0.5 + 35 * np.log10(gama_s) + Fs_dB / 2
        x2 = np.append(gama_s, 6)
        y2 = np.append(N_db_s, 0)
        Z = np.arange(0.3, 6 + 0.001/1e5, 0.001)
        interp_result = np.interp(Z, x2, y2)
        Y = np.min(np.abs(Z -gama))                                            # 找出与Z最为相近的数值因为 分度很小近似认为相等
        Index = np.where(np.abs(Z - gama) == Y)[0] + 1
        N_db = interp_result[Index - 1]
        
        return N_db
        
if __name__ == '__main__':
    x = fun_N(2)
    y = x
    x = 0
    print(x)
    print(y)
