# coding=utf-8
import numpy as np
from matplotlib import pyplot as plt
import timeit

from AIC_algorithm_a import AIC_algorithm_a

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
        data_x = Amp_DATA['AIC_DATA']
        
        '''
        运行程序开始
        '''
        area_num = data_x.shape[0]
        start_p = 1
        end_p = area_num
        
        aic_logn = [''] * area_num
        aic_nak = [''] * area_num
        aic_rice = [''] * area_num
        aic_ray = [''] * area_num
        aic_weib = [''] * area_num
        key_information = []
        pdf = []
        sub_pdf = []
        
        '''
        实际运行时，请取消下一段注释
        '''
        #for i in range(0, area_num):
            #energy = ATT * np.power(data_x[i].T, 2)
            #X = np.sqrt(energy / np.mean(energy))
            #full_aic_weights, pd_information, index, sub_index, aic_logn[i], aic_nak[i], aic_rice[i], aic_ray[i], aic_weib[i] = AIC_algorithm_a(X)
            
            #key_information.append(pd_information)
            #pdf.append(index + 1)
            #sub_pdf.append(sub_index + 1)
            #aic_logn = np.array(aic_logn)
            #aic_nak = np.array(aic_nak)
            #aic_rice = np.array(aic_rice)
            #aic_ray = np.array(aic_ray)
            #aic_weib = np.array(aic_weib)
        
        #key_information = np.array(key_information).reshape(area_num, pd_information.shape[0], pd_information.shape[1], pd_information.shape[2])
        #pdf = np.array(pdf).flatten()
        #sub_pdf = np.array(sub_pdf).flatten()
        #aic = np.concatenate((aic_logn, aic_nak, aic_rice, aic_ray, aic_weib), axis = 0).reshape(-1, area_num).astype('float')
        
        #np.savez('../params/cache.npz', full_aic_weights = full_aic_weights, key_information = key_information, pdf = pdf,
                     #sub_pdf = sub_pdf, aic = aic)
        
        '''
        读取上次循环的数据，节省时间
        '''
        data = np.load('../params/cache.npz')
        full_aic_weights = data['full_aic_weights']
        key_information = data['key_information']
        pdf = data['pdf']
        sub_pdf = data['sub_pdf']
        aic = data['aic']
        
        fai = []
        for mm in range(0, area_num):
            fai = np.concatenate((fai, aic[:, mm] - np.min(aic[:, mm], axis = 0)), axis = 0)
        fai = fai.reshape(area_num, -1).T.astype('float')
        
        w = []
        for mm in range(0, area_num):
            test = np.exp(-fai[:, mm] / 2)
            w = np.concatenate((w, np.exp(-fai[:, mm] / 2) / np.sum(np.exp(-fai[:, mm] / 2), axis = 0)), axis = 0)
        w = w.reshape(area_num, -1).T
        
        max_w = np.max(w, axis = 0)
        index_w = np.argmax(w, axis = 0) + 1
        
        sub_w = w.copy()
        sub_ww = np.max(sub_w, axis = 0)
        ind_subb = np.argmax(sub_w, axis = 0) + 1
        
        for u in range(0, 125):
            sub_w[ind_subb[u] - 1, u] = 0
            
        sub_max_w = np.max(sub_w, axis = 0)
        sub_index_w = np.argmax(sub_w, axis = 0) + 1
        
        Lognormal = 100 * np.shape(np.where(index_w == 1)[0])[0] / np.shape(index_w)[0]
        Nakagami = 100 * np.shape(np.where(index_w == 2)[0])[0] / np.shape(index_w)[0]
        Rician = 100 * np.shape(np.where(index_w == 3)[0])[0] / np.shape(index_w)[0]
        Rayleigh = 100 * np.shape(np.where(index_w == 4)[0])[0] / np.shape(index_w)[0]
        Weibull = 100 * np.shape(np.where(index_w == 5)[0])[0] / np.shape(index_w)[0]
        
        num_v = np.shape(key_information)[0]
        rho = []
        sigma = []
        K = []
        mu = []
        WEI_A = []
        WEI_B = []
        for nn in range(0, num_v):
            rho.append(key_information[nn, 2, 1])
            sigma.append(key_information[nn, 2, 2])
            K.append(np.power(rho[nn], 2)/ (2 * np.power(sigma[nn], 2)))
            mu.append(key_information[nn, 1, 1])
            WEI_A.append(key_information[nn, 4, 1])
            WEI_B.append(key_information[nn, 4, 2])
        rho = np.array(rho).flatten().astype('float')
        sigma = np.array(sigma).flatten().astype('float')
        K = np.array(K).flatten().astype('float')
        mu = np.array(mu).flatten().astype('float')
        WEI_A = np.array(WEI_A).flatten().astype('float')
        WEI_B = np.array(WEI_B).flatten().astype('float')
        
        Lognormal_x = np.where(index_w == 1)[0] + 1
        
        Nakagami_x = np.where(index_w == 2)[0] + 1
        Nakagami_sub_x = []
        Nakagami_X = np.concatenate((Nakagami_x, Nakagami_sub_x), axis = 0).flatten().astype('float')
        Nakagami_X = np.sort(Nakagami_X)
        
        MU = []
        for element in Nakagami_X:
            MU.append(mu[int(element) - 1])
        MU = np.array(MU).flatten().astype('float')
        
        Rician_x = np.where(index_w == 3)[0] + 1
        Rician_sub_x = []
        Rician_X = np.concatenate((Rician_x, Rician_sub_x), axis = 0).flatten().astype('float')
        Rician_X = np.sort(Rician_X)
        
        k_factor = []
        RHO = []
        SIGMA = []
        for element in Rician_X.flat:
            k_factor.append(10 * np.log10(K[int(element) - 1]))
            RHO.append(rho[int(element) - 1])
            SIGMA.append(sigma[int(element) - 1])
        k_factor = np.array(k_factor).flatten().astype('float')
        RHO = np.array(RHO).flatten().astype('float')
        SIGMA = np.array(SIGMA).flatten().astype('float')
        
        Rayleigh_x = np.where(index_w == 4)[0] + 1
        
        Weibull_x = np.where(index_w == 5)[0] + 1
        Weibull_sub_x = []
        Weibull_X = np.concatenate((Weibull_x, Weibull_sub_x), axis = 0).flatten().astype('float')
        Weibull_X = np.sort(Weibull_X)
        
        Weibull_a = []
        Weibull_b = []
        for element in Weibull_X.flat:
            Weibull_a.append(WEI_A[int(element) - 1])
            Weibull_b.append(WEI_B[int(element) - 1])
        Weibull_a = np.array(Weibull_a).flatten().astype('float')
        Weibull_b = np.array(Weibull_b).flatten().astype('float')
        
        p_logn = w[0, :]
        p_naka = w[1, :]
        p_rice = w[2, :]
        p_ray = w[3, :]
        p_weib = w[4, :]
        
        '''
        图形生成程序
        '''
        '''
        绘制保存fig1
        '''
        # 自动控制排版
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        X = TIME
        
        ax.plot(X, p_logn, 'rs', linewidth = 1, label = 'denotes Lognormal')
        ax.plot(X, p_naka, 'b*', linewidth = 1, label = 'denotes Nakagami-m')
        ax.plot(X, p_rice, 'r.', linewidth = 1, label = 'denotes Rician')
        ax.plot(X, p_ray, 'g*', linewidth = 1, label = 'denotes Rayleigh')
        ax.plot(X, p_weib, 'kv', linewidth = 1, label = 'denotes Weibull')
        
        ax.set_xlim(np.min(X), np.max(X))
        ax.set_ylim(0, 1)
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Optimal amplitude distribution', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
        plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.5)
        
        plt.savefig('../results/power_domain/AIC_dis_deter_mainfunction_a_fig1.png')
        
        '''
        绘制保存fig2
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        X = []
        for element in Rician_X.flat:
            X.append(TIME[int(element) - 1])
        X = np.array(X).flatten().astype('float')
        
        ax.plot(X, k_factor, 'b.-', linewidth = 1)
        
        ax.set_xlim(np.min(TIME), np.max(TIME))
        ax.set_ylim(np.min(k_factor), np.max(k_factor))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('K-factor in dB', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
        
        plt.savefig('../results/power_domain/AIC_dis_deter_mainfunction_a_fig2.png')
        
        '''
        绘制保存fig3
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        X = X
        
        ax.plot(X, RHO, 'b.', linewidth = 1.5, label = 'RHO')
        ax.plot(X, SIGMA, 'r.', linewidth = 1.5, label = 'SIGMA')
        
        ax.set_xlim(np.min(TIME), np.max(TIME))
        ax.set_ylim(min(np.min(RHO), np.min(SIGMA)), max(np.max(RHO), np.max(SIGMA)))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('RHO & SIGMA', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
        plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.5)
        
        plt.savefig('../results/power_domain/AIC_dis_deter_mainfunction_a_fig3.png')
        
        '''
        绘制保存fig4
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        X = []
        for element in Nakagami_X.flat:
            X.append(TIME[int(element) - 1])
        X = np.array(X).flatten().astype('float')
        
        ax.plot(X, MU, 'b.', linewidth = 1.5)
        
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('The magnitude of m-factor', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
        
        plt.savefig('../results/power_domain/AIC_dis_deter_mainfunction_a_fig4.png')
        
        '''
        绘制保存fig5
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        X = []
        for element in Weibull_X.flat:
            X.append(TIME[int(element) - 1])
        X = np.array(X).flatten().astype('float')
        
        ax.plot(X, Weibull_a, 'ko', linewidth = 1, label = 'Scale parameter')
        ax.plot(X, Weibull_b, 'rp', linewidth = 1, label = 'Shape parameter')
        
        ax.set_xlim(np.min(TIME), np.max(TIME))
        ax.set_ylim(min(np.min(Weibull_a), np.min(Weibull_b)), max(np.max(Weibull_a), np.max(Weibull_b)))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Magnitude', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
        plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.5)
        
        plt.savefig('../results/power_domain/AIC_dis_deter_mainfunction_a_fig5.png')
        
        '''
        debug message
        '''
        if debug_mode:
            print('data_x')
            print(data_x.shape)
            print(data_x[0].shape)
            print(data_x[0])
            print(data_x[-1])
            #print('X')
            #print(X.shape)
            #print(X[0:6])
            #print(X[-6:])
            print('full_aic_weights')
            print(full_aic_weights.shape)
            print('key_information')
            print(key_information.shape)
            print(key_information[0])
            print(key_information[-1])
            print('pdf')
            print(pdf.shape)
            print(pdf)
            print('sub_pdf')
            print(sub_pdf.shape)
            print(sub_pdf)
            print('aic')
            print(aic.shape)
            print(aic[0, 0:6])
            print(aic[-1, 0:6])
            print('fai')
            print(fai.shape)
            print(fai[0, 0:6])
            print(fai[-1, 0:6])
            print('w')
            print(w.shape)
            print(w[0, 0:6])
            print(w[-1, 0:6])
            print(w[2, 58])
            print('max_w')
            print(max_w.shape)
            print(max_w)
            print('index_w')
            print(index_w.shape)
            print(index_w)
            print('sub_w')
            print(sub_w.shape)
            print(sub_w[0, 0:6])
            print(sub_w[-1, 0:6])
            print(sub_w[2, 58])
            print(sub_w[2, 64])
            print('Lognormal')
            print(Lognormal)
            print('Nakagami')
            print(Nakagami)
            print('Rician')
            print(Rician)
            print('Rayleigh')
            print(Rayleigh)
            print('Weibull')
            print(Weibull)
            print('rho')
            print(rho.shape)
            print(rho)
            print('sigma')
            print(sigma.shape)
            print(sigma)
            print('K')
            print(K.shape)
            print(K)
            print('mu')
            print(mu.shape)
            print(mu)
            print('WEI_A')
            print(WEI_A.shape)
            print(WEI_A)
            print('WEI_B')
            print(WEI_B.shape)
            print(WEI_B)
            print('Lognormal_x')
            print(Lognormal_x.shape)
            print(Lognormal_x)
            print('Nakagami_X')
            print(Nakagami_X.shape)
            print(Nakagami_X)
            print('MU')
            print(MU)
            print('Rician_X')
            print(Rician_X.shape)
            print(Rician_X)
            print('k_factor')
            print(k_factor.shape)
            print(k_factor)
            print('RHO')
            print(RHO.shape)
            print(RHO)
            print('SIGMA')
            print(SIGMA.shape)
            print(SIGMA)
            print('Rayleigh_x')
            print(Rayleigh_x.shape)
            print(Rayleigh_x)
            print('Weibull_a')
            print(Weibull_a.shape)
            print(Weibull_a)
            print('Weibull_b')
            print(Weibull_b.shape)
            print(Weibull_b)
            print('p_weib')
            print(p_weib.shape)
            print(p_weib)
            
        
        
if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    AIC_Amp_determination()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))
