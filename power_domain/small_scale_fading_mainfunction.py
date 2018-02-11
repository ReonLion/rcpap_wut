# coding=utf-8
import numpy as np
from matplotlib import pyplot as plt
import timeit

from Meas_LCR_AFD import Meas_LCR_AFD

class small_scale_fading():
    def __init__(self):
        '''
        设置debug模式
        '''
        debug_mode = True
        
        ssf_paras = np.load('../params/ssf_paras.npz')
        ssf_data = np.load('../params/ssf_data.npz')
        
        '''
        测试参数录入
        '''
        fc = ssf_paras['fc'] / 1e9                                          # 载波中心频率 Hz
        c = ssf_paras['c']                                                  # 光速 m/s
        ATT = ssf_paras['ATT']
        chirp_num = ssf_paras['chirp_num']                                  # chirp 数目 3秒 1933+1933+1934 (可能会引起后面作图错误)
        window = ssf_paras['window']                                        # 窗设置 例如此处设为 20 lambda
        win_wide = ssf_paras['win_wide']
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
        NB_signal = ssf_data['NB_signal']
        PL_no_SM = ssf_data['PL_no_SM']
        Small_scale_fading = ssf_data['Small_scale_fading']
        
        '''
        取用数据设置
        '''
        beg_point = 7202
        end_point = 9300
        T = SM_time[beg_point-1 : end_point]
        Dis = SM_distance[beg_point-1 : end_point]
        RSL_all = NB_signal[beg_point-1 : end_point]
        RSL_n_ssf = PL_no_SM[beg_point-1 : end_point]
        SSF = Small_scale_fading[beg_point-1 : end_point]
        ssf1 = 10 ** (SSF / 10)
        beg_ssf_point = 1
        end_ssf_point = 9300 - 7202
        ssf = ssf1[beg_ssf_point-1 : end_ssf_point]
        data_length = np.shape(ssf)[0]
        
        '''
        运行程序开始
        '''
        '''
        LCR & AFD
        '''
        LCR_total, AFD_total, Threshold = Meas_LCR_AFD(ssf)
        com_time = data_length / win_wide
        LCR_per_second = LCR_total / com_time
        AFD = AFD_total / data_length
        Amp_NB = ssf ** 0.5
        Amp_all_NB = ssf1 ** 0.5
        Threshold = 10 * np.log10(Threshold)
        
        '''
        图形生成程序
        '''
        T = T -71
        
        '''
        绘制保存fig1
        '''
        fig = plt.figure(tight_layout = True)
        
        ax = fig.add_subplot(211)
        ax.plot(T, RSL_all, 'b')
        ax.plot(T, RSL_n_ssf, 'g')
        ax.grid(True)
        
        ax = fig.add_subplot(212)
        ax.plot(T, SSF, 'b')
        ax.grid(True)
        
        plt.show()
        
        
        if debug_mode:
            print('NB_signal')
            print(NB_signal.shape)
            print('PL_no_SM')
            print(PL_no_SM.shape)
            print('Small_scale_fading')
            print(Small_scale_fading.shape)
            print('ssf')
            print(ssf.shape)
            print(ssf[0:6])
            print(ssf[-6:])
            print('SSF')
            print(SSF.shape)
            print(SSF[0:6])
            print('LCR_per_second')
            print(LCR_per_second.shape)
            print(LCR_per_second[0:6])
            print(LCR_per_second[300:306])
            print(LCR_per_second[-6:])
            print('AFD')
            print(AFD.shape)
            print(AFD[0:6])
            print(AFD[300:306])
            print(AFD[-6:])
            print('Threshold')
            print(Threshold.shape)
            print(Threshold[0:6])
            print(Threshold[300:306])
            print(Threshold[-6:])            
            
if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    small_scale_fading()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))
