# coding=utf-8
import numpy as np
import timeit

from txt_read import txt_read
from xls_read import tx_xls_read, rx_xls_read
from Att_mark import Att_mark
from GPS_2_distance import GPS_2_distance
from signal_window import signal_window
from CIR_window import CIR_window
from distance_match import distance_match
from time_match import time_match
from speed_match import speed_match
from MakeChirp import MakeChirp

class main_doppler():
    def __init__(self):
        '''
        设置t_start和t_stop
        '''
        t_start = 64                                                   # 读取excel的开始时间，第几行，包括这一行
        t_stop = 69                                                    # 读取excel的结束时间，第几行，包括这一行
        
        '''
        读取txt, xls的信息
        '''
        txt_info = txt_read('txt')
        tx_xls = tx_xls_read('excel/81_out_tx.xls', t_start, t_stop)
        rx_xls = rx_xls_read('excel/81_out_rx.xls', t_start, t_stop)
        
        signal_CIR = txt_info.signal_CIR                               # signal_CIR为一个(txt文件数目)大小的列表
        GPS_rx = rx_xls.GPS_rx
        GPS_tx = tx_xls.GPS_tx
        v_tx = tx_xls.v_tx
        v_rx = rx_xls.v_rx
        rel_speed = np.maximum(v_tx, v_rx)
        
        '''
        测试参数设置
        '''
        beg_p = 1                                                      # 数据起始点设置，从第二个chirp开始(由于第一个chirp不对所有的RSL数据都比RX位置数据多了1, 但此处也要注意)2对应了GPS坐标1
        end_p = 6                                                      # 数据终止点设置，32对应了GPS坐标31
        window = 10                                                    # 窗设置，例如此处设为 20 lambda
        beg_t_mark = 0                                                 # 起始点时间序号，例如此数据共50s，因此，此时值为 0
        t_res = 10                                                     # unit:ns,esolution
        
        '''
        天线参数设置
        '''
        TX_power = 16                                                  # 天线发射功率 16 dBm
        TX_Gain = 2                                                    # 发射天线增益 2 dBi
        RX_Gain = 10                                                   # 接收天线增益 2 dBi
        TX_heigh = 1.57                                                # 发射天线有效高度 m
        RX_heigh = 1.78                                                # 接收天线有效高度 m
        
        '''
        瞬时多普勒频移需要的参数
        '''
        T_doppler = 2                                                  # 第 20 秒的多普勒频移
        num_file = 2                                                   # 选择多少个窗作多普勒频移
        
        '''
        设备参数设置
        '''
        fc = 5.9e9                                                     # 载波中心频率 Hz
        c = 3e8                                                        # 光速 m/s
        ATT_mark = 23                                                  # 衰减系数ATT为8
        ATT = Att_mark(ATT_mark)
        chirp_num = (1933+1933+1934)/3                                 # chirp数目3秒1933+1933+1934(可能会引起后面作图错误)
        cable1 = 3                                                     # 线损3dB
        cable2 = 3                                                     # 线损3dB
        
        '''
        测试数据读取
        '''
        ave_speed =np.mean(rel_speed)                                  # 平均相对速度 m/s
        max_speed = np.max(rel_speed)                                  # 最大相对速度 m/s
        
        '''
        数据生成程序
        '''
        data = []
        cir = []
        data_pdp = [0] * (end_p - beg_p + 1)
        CIR_1 = [0] * (end_p - beg_p + 1)
        for n in range(beg_p - 1, end_p):
            data_pdp[n] = ATT * np.power(np.absolute(signal_CIR[n]), 2)
            data_pdp[n][:, 0] = data_pdp[n][:, 1]                                                       # 去掉起始点的突起
            CIR_1[n] = signal_CIR[n][:]                                                                 # 原始 CIR 信号 cell
            CIR_1[n][:, 0] = CIR_1[n][:, 1] - np.random.rand(1, 1) / 1e4                                # 去掉起始点的突起 rand是为了防止出现多普勒频移处找点重合的问题
        
        signal_CIR = []                                                                                 # 清除缓存数据
        T = rx_xls.T                                                                                    # 注意：若第一个文件是有效的那要把1改为其它对应时间
        d = GPS_2_distance(GPS_rx, GPS_tx)                                                              # d units: km
        Dis = d * 1000                                                                                  # Dis units: m
        max_v = max_speed                                                                               # 最大相对速度用于取窗
        win_wide = np.floor(window * (chirp_num * (c / fc)) / max_v)                                    # 窗宽 units: chirp
        after_window = signal_window(win_wide, data_pdp)
        after_window_cir = CIR_window(win_wide, CIR_1)
        distance = distance_match(after_window, Dis)
        time = time_match(after_window, T)
        V_rel = speed_match(after_window, rel_speed)
        num_a = np.shape(distance)[0]
        pdp_window = after_window[0]
        D_window = distance[0]
        TIME = time[0]
        V_Rel = V_rel[0]
        for i in range(0, num_a - 1):
            pdp_window = np.row_stack((pdp_window, after_window[i + 1]))
            D_window = np.concatenate((D_window, distance[i + 1]), axis = 0)
            TIME = np.concatenate((TIME, time[i + 1]), axis = 0)
            V_Rel = np.concatenate((V_Rel, V_rel[i + 1]), axis = 0)
        CIR_window_doppler = after_window_cir[0 : np.shape(TIME)[0]]
        after_window_cir = []
        CIR_1 = []
        
        '''
        获取振幅分布数据
        '''
        AIC_data = CIR_window_doppler[:]
        NA = len(AIC_data)                                                                              # 按照分段获取数组范围( 20*lambda )
        Chirp_t = MakeChirp(SampFreqDec = 1 / 8.125e-9, ChirpBandw = 100e6, NchirpDec = np.shape(AIC_data[0])[-1])           # 产生模拟标准chirp信号
        Chirp_f = np.fft.fftshift(np.fft.fft(np.conj(np.flipud(Chirp_t))))                              # 为除去卷积chirp信号做准备
        
        
        '''
        debug message
        '''
        print('GPS_rx')
        print(GPS_rx)
        print('GPS_tx')
        print(GPS_tx)
        print('v_rx')
        print(v_rx)
        print('v_tx')
        print(v_tx)
        print('rel_speed')
        print(rel_speed)
        print('ATT')
        print(ATT)
        print('data_pdp')
        for data in data_pdp:
            print(data.shape)
            print(data[0][0:6])
        print('CIR_1')
        for data in CIR_1:
            print(data.shape)
            print(data[0][0:6])
        print('T')
        print(T)
        print('d')
        print(d)
        print('win_wide')
        print(win_wide)
        print('after_window')
        for after_window_i in after_window:
            print(after_window_i.shape)
            print(after_window_i[0][0:6])
        print('after_window_cir')
        print(len(after_window_cir))
        for after_window_cir_i in after_window_cir:
            print(after_window_cir_i.shape)
            print(after_window_cir_i[0][0:6])
        print('distance')
        for distance_i in distance:
            print(distance_i.shape)
            print(distance_i[0:6])
        print('time')
        for time_i in time:
            print(time_i.shape)
            print(time_i[0:6])
        print('V_rel')
        for V_rel_i in V_rel:
            print(V_rel_i.shape)
            print(V_rel_i[0:6])
        print('pdp_window')
        print(pdp_window.shape)
        print(pdp_window[-1][0:6])
        print('D_window')
        print(D_window.shape)
        print(D_window[20:26])
        print('TIME')
        print(TIME.shape)
        print(TIME[20:26])
        print('V_Rel')
        print(V_Rel.shape)
        print(V_Rel[20:26])
        print('CIR_window_doppler')
        print(len(CIR_window_doppler))
        for CIR_window_doppler_i in CIR_window_doppler:
            print(CIR_window_doppler_i.shape)
            print(CIR_window_doppler_i[0][0:6])
        print('Chirp_t')
        print(Chirp_t.shape)
        print(Chirp_t[0:6])
        print('Chirp_f')
        print(Chirp_f.shape)
        print(Chirp_f[0:6])
        

if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    '''
    主程序
    '''
    main_doppler()
    
    end_time = timeit.default_timer()
    print(str(end_time - begin_time))    