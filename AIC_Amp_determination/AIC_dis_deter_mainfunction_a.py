# coding=utf-8
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import timeit

class AIC_Amp_determination():
    def __init__(self):
        '''
        设置Debug模式
        '''
        debug_mode = True
        
        ssf_paras = np.load('../params/ssf_paras.npz')
        Amp_DATA = np.load('../params/Amp_DATA.npz')
        
        '''
        测试参数录入
        '''
        fc = ssf_paras['fc'] / 1e9                                          # 载波中心频率 Hz
        c = ssf_paras['c']                                                  # 光速 m/s
        ATT = ssf_paras['ATT']
        chirp_num = ssf_paras['chirp_num']                                  # chirp 数目 3秒 1933+1933+1934 (可能会引起后面作图错误)
        window = ssf_paras['window']                                        # 窗设置 例如此处设为 20 lambda
        beg_p = ssf_paras['beg_p']                                          # 数据起始点设置 从第二个 chirp开始 (由于第一个chirp不对所有的RSL数据都比RX位置数据多了1, 但此处也要注意) 2对应了GPS坐标1
        end_p = ssf_paras['end_p']                                          # 数据终止点设置 32对应了GPS坐标31
        beg_t_mark = ssf_paras['beg_t_mark']                                # 起始点时间序号 例如此数据共50s 因此 此时值为 0
        cable1 = ssf_paras['cable1']                                        # 线损 3dB
        cable2 = ssf_paras['cable2']                                        # 线损 3dB
        TX_power = ssf_paras['TX_power']                                    # 天线发射功率 16 dBm
        G_TX = ssf_paras['TX_Gain']                                         # 发射天线增益 2 dBi
        G_RX = ssf_paras['RX_Gain']                                         # 接收天线增益 2 dBi
        h_1 = ssf_paras['TX_heigh'] / 1000                                  # 发射天线有效高度 km
        h_2 = ssf_paras['RX_heigh'] / 1000                                  # 接收天线有效高度 km
        SM_time = ssf_paras['SM_time']
        SM_distance = ssf_paras['SM_distance']
        TIME = ssf_paras['TIME'] - 1
        data_x = Amp_DATA['AIC_DATA'].reshape((-1, 1, Amp_DATA['AIC_DATA'].shape[-1]))
        data_x_new = []
        for i in range(0, data_x.shape[0]):
            data_x_new.append(data_x[i])
        
        '''
        运行程序开始
        '''
        
        
        
        '''
        debug message
        '''
        if debug_mode:
            print('data_x')
            print(data_x.shape)
            print(data_x[0].shape)
            print(data_x[0])
            print(data_x[-1])
            
        
        
if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    AIC_Amp_determination()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))
