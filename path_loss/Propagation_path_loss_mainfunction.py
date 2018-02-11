# coding=utf-8

import numpy as np
from scipy.special import erfc
from matplotlib import pyplot as plt
import timeit

from fun_N import fun_N
from GRG_MAPE import GRG_MAPE_AVRG, GRG_MAPE_delta, GRG_MAPE_R, GRG_MAPE_r1, pearson_fun

class Propagation_path_loss():
    def __init__(self):
        '''
        设置Debug模式
        '''
        debug_mode = True
        
        PL_paras = np.load('../params/PL_paras.npz')
        PL_data = np.load('../params/PL_data.npz')
        
        fc = PL_paras['fc'] / 1e9
        c = PL_paras['c']
        ATT = PL_paras['ATT']
        chirp_num = PL_paras['chirp_num']
        window = PL_paras['window']
        beg_p = PL_paras['beg_p']
        end_p = PL_paras['end_p']
        beg_t_mark = PL_paras['beg_t_mark']
        cable1 = PL_paras['cable1']
        cable2 = PL_paras['cable2']
        TX_power = PL_paras['TX_power']
        G_TX = PL_paras['TX_Gain']
        G_RX = PL_paras['RX_Gain']
        h_1 = PL_paras['TX_heigh'] / 1000
        h_2 = PL_paras['RX_heigh'] / 1000
        TIME = PL_paras['TIME']
        D_window = PL_paras['D_window'] / 1000
        rsl = PL_data['RSL']
        
        '''
        取用数据设置
        '''
        polar = 3
        beg_point = 1
        end_point = np.shape(rsl)[0]
        distance = D_window[beg_point - 1 : end_point]
        time = TIME[beg_point - 1 : end_point]
        RSL_dBm = rsl[beg_point - 1 : end_point]
        Yxin_a = 2e-6
        Yxin_b = 7e-5
        r_e = 6371
        daierta = 0.001
        dielectric = 3
        
        '''
        运行程序开始
        '''
        lanmuda = c / (fc * 1e9) / 1000
        k = 2 * np.pi / lanmuda
        PL = G_TX + G_RX + TX_power - RSL_dBm - cable1 - cable2
        
        '''
        第一菲涅尔区参数数据
        '''
        D_f = 0.0000389 * (fc * 1000) * (h_1 * 1000) * (h_2 * 1000)
        D_h = 4.1 * (np.sqrt( h_1 * 1000) + np.sqrt(h_2 * 1000))
        D_06 = (D_f * D_h) / (D_h + D_f)
        ke = 1
        D1 = np.sqrt(2 * ke * r_e * h_1)
        D2 = np.sqrt(2 * ke * r_e * h_2)
        
        alpha1 = 48.29
        beita1 = 3.042
        
        sum_reflection = []
        d_los = []
        dif = []
        h_1_1 = []
        h_2_2 = []
        D33 = []
        
        R = []
        R_roughness_25 = []
        R_roughness_5 = []
        R_roughness_1 = []
        R_roughness_2 =[]
        Divergency = []
        ceita_e = []
        S_fun_1 = []
        S_fun_2 = []
        S_fun_3 = []
        A_1 = []
        A_2 = []
        A_3 = []
        
        yipuxilong_1111 = []
        yipuxilong_2222 = []
        yipuxilong_3333 = []
        L33 = []
        diffraction_loss = []
        yita = []
        REL = []
        R_VAR = []
        R_H = []
        R = []
        Free_space = []
        
        for i in range(0, np.shape(distance)[0]):
            '''
            alpha & beita 几何角度运算 (见REL几何模型图)
            '''
            d_1 = distance[i]
            if d_1 < 0.5:
                D_2 = (d_1 * h_2) / (h_1 + h_2)
                D_1 = d_1 - D_2
                reflection_X1 = np.sqrt(np.power(h_1, 2) + np.power(D_1, 2))
                reflection_X2 = np.sqrt(np.power(h_2, 2) + np.power(D_2, 2))
                d_curve = d_1
                D3 = d_curve - D1 - D2
                D33.append(d_curve - D1 - D2)
                D3 = np.abs(D3)
                sum_reflection.append(reflection_X1 + reflection_X2)
                D_LOS = np.sqrt(np.power(h_1 - h_2, 2) + np.power(d_1, 2))
                d_los.append(D_LOS)
                D_diff = sum_reflection[i] - D_LOS
                dif.append(D_diff)
                h_1_1.append(h_1)
                h_2_2.append(h_2)
            else:
                araph = np.linspace(Yxin_a, Yxin_a, np.shape(distance)[0], endpoint = True)
                beita = np.linspace(Yxin_b, Yxin_b, np.shape(distance)[0], endpoint = True)
                
                if i == 0:
                    x2 = fsolve(self.f, [araph[0], beita[0]], args = (h_1, h_2, r_e, d_1), factor = 1.0)
                    araph[i] = x2[0]
                    beita[i] = x2[1]
                else:
                    x2 = fsolve(self.f, [araph[i - 1], beita[i - 1]], args = (h_1, h_2, r_e, d_1), factor = 1.0)
                    araph[i] = x2[0]
                    beita[i] = x2[1]
                '''
                各REL模型几何初始变量计算
                '''
                reflection_X1 = (((h_1 + r_e) ** 2 + (r_e ** 2) - (2 * (h_1 + r_e) * r_e * np.cos(araph[i]))) ** 0.5)
                reflection_X2 = (((h_2 + r_e) ** 2 + (r_e ** 2) - (2 * (h_2 + r_e) * r_e * np.cos(beita[i]))) ** 0.5)
                D_1 = r_e * araph[i]
                D_2 = r_e * beita[i]
                d_curve = d_1
                D3 = d_curve - D1 - D2
                D33[i] = d_curve - D1 - D2
                D3 = np.abs(D3)
                sum_reflection[i] = reflection_X1 + reflection_X2
                kexi = 2 * (h_1 + r_e) * (h_2 + r_e) * np.cos(d_1 / r_e)
                D_LOS = np.sqrt((h_1 + r_e) ** 2 + (h_2 + r_e) ** 2 - kexi)
                d_los[i] = D_LOS
                D_diff = sum_reflection[i] - D_LOS
                dif[i] = D_diff
                D_diff1 = 2 * h_1 * h_2 / d_1
                h_1_1[i] = h_1 - 0.5 * r_e * araph[i] ** 2
                h_2_2[i] = h_2 - 0.5 * r_e * beita[i] ** 2
            
            '''
            REL model构建
            '''
            if h_1_1[i] < 0 or h_2_2[i] < 0:
                R.append(-1)
                R_roughness_25.append(R[i])
                R_roughness_5.append(R[i])
                R_roughness_1.append(R[i])
                R_roughness_2.append(R[i])
                
                # divergency modify
                Divergency.append(0)
                fai = 0
                ceita_e.append(np.rad2deg(fai))
                
                # shadowing effect
                if np.rad2deg(pi / 2 - fai) >= 90.0:
                    S_fun_1.append(0)
                    S_fun_2.append(0)
                    S_fun_3.append(0)
                else:
                    tan_incident_angle = 1 / np.tan(np.pi / 2 - fai)
                    
                    beita_0_1 = 0.008
                    beita_0_2 = 0.02
                    beita_0_3 = 0.04
                    
                    error_function_1 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_1))
                    A_1.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_1 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_1 ** 2))) - error_function_1))
                    S_fun_1.append((1 - 0.5 * error_function_1) / (A_1[i] + 1))
                    
                    error_function_2 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_2))
                    A_2.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_2 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_2 ** 2))) - error_function_2))
                    S_fun_2.append((1 - 0.5 * error_function_2) / (A_2[i] + 1))
                    
                    error_function_3 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_3))
                    A_3.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_3 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_3 ** 2))) - error_function_3))
                    S_fun_3.append((1 - 0.5 * error_function_3) / (A_3[i] + 1))
                
                '''
                地球曲率衍射影响
                '''
                yipuxilong_1 = (2 * np.pi * D1 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                yipuxilong_1111.append(yipuxilong_1)
                yipuxilong_2 = (2 * np.pi * D2 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                yipuxilong_2222.append(yipuxilong_2)
                yipuxilong_3 = (2 * np.pi * D3 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                yipuxilong_3333.append(yipuxilong_3)
                
                N_n_1 = fun_N(yipuxilong_1)
                N_n_2 = fun_N(yipuxilong_2)
                L1 = N_n_1 - 20 * np.log10((np.sqrt( 5.656 * np.pi * yipuxilong_1)))
                L2 = N_n_2.copy()
                L3 = 0.0086 * yipuxilong_3 ** 3 + 0.2063 * yipuxilong_3 ** 2 + 11.0997 * yipuxilong_3 - 0.8934
                L33.append(L3)
                
                if d_curve >= (D1 + D2):
                    diffraction_loss.append(L1 + L2 - np.abs(L3))
                elif d_curve < (D1 + D2) and d_curve > D_06:
                    if L1 + L2 + L3 >= 0:
                        index_energy = i + 1
                        diffraction_loss.append(0)
                    else:
                        diffraction_loss.append(L1 + L2 + np.abs(L3))
                elif d_curve <= D_06:
                    if L1 + L2 + L3 >= 0:
                        index_energy = i + 1
                    index_start = i + 1
                    diffraction_loss.append(0)
                    
                yita.append(np.abs( 1 + Divergency[i] * S_fun_1[i] * R_roughness_25[i] * np.exp(k * (D_diff) * 1j)))
                REL.append(20 * np.log10(lanmuda / (4 * np.pi * D_LOS)) + 20 * np.log10(yita[i]) + diffraction_loss[i])
                
            else:
                '''
                开始四次大的筛选
                CtrlC + CtrlV
                '''
                if polar == 1:
                    # Effective Reflection modify 
                    percent_h = 0.5
                    percent_v = 0.5
                    fai = np.arcsin(h_1_1[i] / reflection_X1)
                    ceita_e.append(np.rad2deg(fai))
                    A_T = dielectric - (18 * daierta / fc) * (i + 1)
                    R_VAR.append((np.sin(fai) - np.sqrt(A_T - (np.cos(fai) ** 2))) / (np.sin(fai) + np.sqrt(A_T - (np.cos(fai) ** 2))))
                    R_H.append((A_T * np.sin(fai) - np.sqrt(A_T - (np.cos(fai) ** 2))) / (A_T * np.sin(fai) + np.sqrt(A_T - (np.cos(fai) ** 2))))
                    R.append(percent_v * R_VAR[i] + percent_h * R_H[i])
                    h_stand_de_1 = 0.25/1000
                    h_stand_de_2 = 0.5/1000
                    h_stand_de_3 = 1/1000
                    h_stand_de_4 = 2/1000
                    R_roughness_25.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_1 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    R_roughness_5.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_2 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    R_roughness_1.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_3 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    R_roughness_2.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_4 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    # Divergency modify
                    Divergency.append(1 / np.sqrt(1 + ((2 * D_1 * D_2) / (r_e * (h_1_1[i]+h_2_2[i])))))
                    # shadowing effect
                    if np.rad2deg(np.pi / 2 - fai) >= 90.0:
                        S_fun_1.append(0)
                        S_fun_2.append(0)
                        S_fun_3.append(0)
                    else:
                        tan_incident_angle = 1 / np.tan(np.pi / 2 - fai)
                        beita_0_1 = 0.003
                        beita_0_2 = 0.08
                        beita_0_3 = 0.02
                        error_function_1 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_1))
                        A_1.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_1 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_1 ** 2))) - error_function_1))
                        S_fun_1.append((1 - 0.5 * error_function_1) / (A_1[i] + 1))
                        error_function_2 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_2))
                        A_2.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_2 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_2 ** 2))) - error_function_2))
                        S_fun_2.append((1 - 0.5 * error_function_2) / (A_2[i] + 1))
                        error_function_3 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_3))
                        A_3.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_3 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_3 ** 2))) - error_function_3))
                        S_fun_3.append((1 - 0.5 * error_function_3) / (A_3[i] + 1))
                    # 地球曲率衍射影响
                    yipuxilong_1 = (2 * np.pi * D1 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                    yipuxilong_1111.append(yipuxilong_1)
                    yipuxilong_2 = (2 * np.pi * D2 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                    yipuxilong_2222.append(yipuxilong_2)
                    yipuxilong_3 = (2 * np.pi * D3 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                    yipuxilong_3333.append(yipuxilong_3)
                    N_n_1 = fun_N(yipuxilong_1)
                    N_n_2 = fun_N(yipuxilong_2)
                    L1 = N_n_1 - 20 * np.log10((np.sqrt( 5.656 * np.pi * yipuxilong_1)))
                    L2 = N_n_2.copy()
                    L3 = 0.0086 * yipuxilong_3 ** 3 + 0.2063 * yipuxilong_3 ** 2 + 11.0997 * yipuxilong_3 - 0.8934
                    L33.append(L3)
                    if d_curve >= (D1 + D2):
                        diffraction_loss.append(L1 + L2 - np.abs(L3))
                    elif d_curve < (D1 + D2) and d_curve > D_06:
                        if L1 + L2 + L3 >= 0:
                            index_energy = i + 1
                            diffraction_loss.append(0)
                        else:
                            diffraction_loss.append(L1 + L2 + np.abs(L3))
                    elif d_curve <= D_06:
                        if L1 + L2 + L3 >= 0:
                            index_energy = i + 1
                        index_start = i + 1
                        diffraction_loss.append(0)
                    yita.append(np.abs( 1 + Divergency[i] * S_fun_1[i] * R_roughness_25[i] * np.exp(k * (D_diff) * 1j)))
                    REL.append(-1 * (alpha1 + 10 * beita1 * np.log10(distance[i] * 1000)) + 20 * np.log10(yita[i])+diffraction_loss[i])
                elif polar == 2:
                    # Effective Reflection modify 
                    percent_h = 1.0
                    percent_v = 0
                    fai = np.arcsin(h_1_1[i] / reflection_X1)
                    ceita_e.append(np.rad2deg(fai))
                    A_T = dielectric - (18 * daierta / fc) * (i + 1)
                    R_VAR.append((np.sin(fai) - np.sqrt(A_T - (np.cos(fai) ** 2))) / (np.sin(fai) + np.sqrt(A_T - (np.cos(fai) ** 2))))
                    R_H.append((A_T * np.sin(fai) - np.sqrt(A_T - (np.cos(fai) ** 2))) / (A_T * np.sin(fai) + np.sqrt(A_T - (np.cos(fai) ** 2))))
                    R.append(percent_v * R_VAR[i] + percent_h * R_H[i])
                    h_stand_de_1 = 0.25/1000
                    h_stand_de_2 = 0.5/1000
                    h_stand_de_3 = 1/1000
                    h_stand_de_4 = 2/1000
                    R_roughness_25.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_1 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    R_roughness_5.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_2 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    R_roughness_1.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_3 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    R_roughness_2.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_4 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    # Divergency modify
                    Divergency.append(1 / np.sqrt(1 + ((2 * D_1 * D_2) / (r_e * (h_1_1[i]+h_2_2[i])))))
                    # shadowing effect
                    if np.rad2deg(np.pi / 2 - fai) >= 90.0:
                        S_fun_1.append(0)
                        S_fun_2.append(0)
                        S_fun_3.append(0)
                    else:
                        tan_incident_angle = 1 / np.tan(np.pi / 2 - fai)
                        beita_0_1 = 0.003
                        beita_0_2 = 0.08
                        beita_0_3 = 0.02
                        error_function_1 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_1))
                        A_1.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_1 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_1 ** 2))) - error_function_1))
                        S_fun_1.append((1 - 0.5 * error_function_1) / (A_1[i] + 1))
                        error_function_2 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_2))
                        A_2.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_2 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_2 ** 2))) - error_function_2))
                        S_fun_2.append((1 - 0.5 * error_function_2) / (A_2[i] + 1))
                        error_function_3 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_3))
                        A_3.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_3 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_3 ** 2))) - error_function_3))
                        S_fun_3.append((1 - 0.5 * error_function_3) / (A_3[i] + 1))
                    # 地球曲率衍射影响
                    yipuxilong_1 = (2 * np.pi * D1 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                    yipuxilong_1111.append(yipuxilong_1)
                    yipuxilong_2 = (2 * np.pi * D2 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                    yipuxilong_2222.append(yipuxilong_2)
                    yipuxilong_3 = (2 * np.pi * D3 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                    yipuxilong_3333.append(yipuxilong_3)
                    N_n_1 = fun_N(yipuxilong_1)
                    N_n_2 = fun_N(yipuxilong_2)
                    L1 = N_n_1 - 20 * np.log10((np.sqrt( 5.656 * np.pi * yipuxilong_1)))
                    L2 = N_n_2.copy()
                    L3 = 0.0086 * yipuxilong_3 ** 3 + 0.2063 * yipuxilong_3 ** 2 + 11.0997 * yipuxilong_3 - 0.8934
                    L33.append(L3)
                    if d_curve >= (D1 + D2):
                        diffraction_loss.append(L1 + L2 - np.abs(L3))
                    elif d_curve < (D1 + D2) and d_curve > D_06:
                        if L1 + L2 + L3 >= 0:
                            index_energy = i + 1
                            diffraction_loss.append(0)
                        else:
                            diffraction_loss.append(L1 + L2 + np.abs(L3))
                    elif d_curve <= D_06:
                        if L1 + L2 + L3 >= 0:
                            index_energy = i + 1
                        index_start = i + 1
                        diffraction_loss.append(0)
                    yita.append(np.abs( 1 + Divergency[i] * S_fun_1[i] * R_roughness_25[i] * np.exp(k * (D_diff) * 1j)))
                    REL.append(-1 * (alpha1 + 10 * beita1 * np.log10(distance[i] * 1000)) + 20 * np.log10(yita[i])+diffraction_loss[i])
                elif polar == 3:
                    # Effective Reflection modify 
                    percent_h = 0
                    percent_v = 1.0
                    fai = np.arcsin(h_1_1[i] / reflection_X1)
                    ceita_e.append(np.rad2deg(fai))
                    A_T = dielectric - (18 * daierta / fc) * (i + 1)
                    R_VAR.append((np.sin(fai) - np.sqrt(A_T - (np.cos(fai) ** 2))) / (np.sin(fai) + np.sqrt(A_T - (np.cos(fai) ** 2))))
                    R_H.append((A_T * np.sin(fai) - np.sqrt(A_T - (np.cos(fai) ** 2))) / (A_T * np.sin(fai) + np.sqrt(A_T - (np.cos(fai) ** 2))))
                    R.append(percent_v * R_VAR[i] + percent_h * R_H[i])
                    h_stand_de_1 = 0.15/1000
                    h_stand_de_2 = 0.15/1000
                    h_stand_de_3 = 1/1000
                    h_stand_de_4 = 2/1000
                    R_roughness_25.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_1 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    R_roughness_5.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_2 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    R_roughness_1.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_3 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    R_roughness_2.append(R[i] * np.exp(-2 * ((2 * np.pi * h_stand_de_4 * h_1_1[i] / (reflection_X1 * lanmuda)) ** 2)))
                    # Divergency modify
                    Divergency.append(1 / np.sqrt(1 + ((2 * D_1 * D_2) / (r_e * (h_1_1[i]+h_2_2[i])))))
                    # shadowing effect
                    if np.rad2deg(np.pi / 2 - fai) >= 90.0:
                        S_fun_1.append(0)
                        S_fun_2.append(0)
                        S_fun_3.append(0)
                    else:
                        tan_incident_angle = 1 / np.tan(np.pi / 2 - fai)
                        beita_0_1 = 0.003
                        beita_0_2 = 0.08
                        beita_0_3 = 0.02
                        error_function_1 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_1))
                        A_1.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_1 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_1 ** 2))) - error_function_1))
                        S_fun_1.append((1 - 0.5 * error_function_1) / (A_1[i] + 1))
                        error_function_2 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_2))
                        A_2.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_2 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_2 ** 2))) - error_function_2))
                        S_fun_2.append((1 - 0.5 * error_function_2) / (A_2[i] + 1))
                        error_function_3 = erfc(tan_incident_angle / (np.sqrt(2) * beita_0_3))
                        A_3.append(0.5 * (np.sqrt(2 / np.pi) * (beita_0_3 / tan_incident_angle) * np.exp(-1 * (tan_incident_angle ** 2) / (2 * (beita_0_3 ** 2))) - error_function_3))
                        S_fun_3.append((1 - 0.5 * error_function_3) / (A_3[i] + 1))
                    # 地球曲率衍射影响
                    yipuxilong_1 = (2 * np.pi * D1 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                    yipuxilong_1111.append(yipuxilong_1)
                    yipuxilong_2 = (2 * np.pi * D2 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                    yipuxilong_2222.append(yipuxilong_2)
                    yipuxilong_3 = (2 * np.pi * D3 / lanmuda) / ((2 * np.pi * ke * r_e / lanmuda) ** (2/3))
                    yipuxilong_3333.append(yipuxilong_3)
                    N_n_1 = fun_N(yipuxilong_1)
                    N_n_2 = fun_N(yipuxilong_2)
                    L1 = N_n_1 - 20 * np.log10((np.sqrt( 5.656 * np.pi * yipuxilong_1)))
                    L2 = N_n_2.copy()
                    L3 = 0.0086 * yipuxilong_3 ** 3 + 0.2063 * yipuxilong_3 ** 2 + 11.0997 * yipuxilong_3 - 0.8934
                    L33.append(L3)
                    if d_curve >= (D1 + D2):
                        diffraction_loss.append(L1 + L2 - np.abs(L3))
                    elif d_curve < (D1 + D2) and d_curve > D_06:
                        if L1 + L2 + L3 >= 0:
                            index_energy = i + 1
                            diffraction_loss.append(0)
                        else:
                            diffraction_loss.append(L1 + L2 + np.abs(L3))
                    elif d_curve <= D_06:
                        if L1 + L2 + L3 >= 0:
                            index_energy = i + 1
                        index_start = i + 1
                        diffraction_loss.append(0)
                    yita.append(np.abs( 1 + Divergency[i] * S_fun_1[i] * R_roughness_25[i] * np.exp(k * (D_diff) * 1j)))
                    REL.append(-1 * (alpha1 + 10 * beita1 * np.log10(distance[i] * 1000)) + 20 * np.log10(yita[i])+diffraction_loss[i])
                    Free_space.append(20 * np.log10(lanmuda / (4 * np.pi * D_LOS)))
                #
            #
        # for循环结束
        
        # 将循环前声明的列表转换为数组
        L33 = np.array(L33).astype('float')
        REL = np.array(REL).astype('complex64')
        diffraction_loss = np.array(diffraction_loss).astype('float')
        yita = np.array(yita).astype('complex64')
        
        R_eff = np.abs(R)
        R_eff_roughness_25 = np.abs(R_roughness_25)
        R_eff_roughness_5 = np.abs(R_roughness_5)
        R_eff_roughness_1 = np.abs(R_roughness_1)
        R_eff_roughness_2 = np.abs(R_roughness_2)
        y = np.linspace(0, 0, np.shape(distance)[0], endpoint = True)
        
        # 对于earth_curvature_loss的内插计算
        # 这段是否有用？
        if index_start != np.shape(distance)[0]:
            Again_L3 = L33.copy()
            index = np.where(Again_L3 > 0.5)[0] + 1
            Y_temp = np.min(Again_L3[int(index_start):])
            index_zero = np.where(Again_L3[int(index_start):] == Y_temp)[0][0] + 1
            
            cache = []
            for element in index.flat:
                cache.append(Again_L3[int(element - 1)])
            cache = np.array(cache).astype('float')
            
            Again_L3[int(index[0])-1:] = np.interp(np.arange(index[0] - 1, Again_L3.shape[0] + 1), index.append(int(index_start + index_zero)), cache.append(0))
            Again_L3[int(index_start + index_zero) - 1 :] = -1 * Again_L3[index_start + index_zero - 1 :]
            Again_L3[index[0] - 1 : index[index_start - 1]] = 0
            Again_L3[index[0] - 1 : index[index_energy - 1]] = 0
            Earth_curvature_loss = Again_L3 + L1 + L2
            Earth_curvature_loss[index[0] - 1 : index[index_start - 1]] = 0
            Earth_curvature_loss[index[0] - 1 : index[index_energy - 1]] = 0
            REL = REL - diffraction_loss + Earth_curvature_loss
        else:
            Earth_curvature_loss = 0
        
        REL = REL - diffraction_loss + Earth_curvature_loss
        REL = -REL
        
        '''
        其它模型输入
        '''
        Free_space = 20 * np.log10(lanmuda / (4 * np.pi * distance))
        Free_space = -Free_space
        One_slope = alpha1 + 10 * beita1 * np.log10(distance * 1000)
        WINNER_B1 = 22.7 * np.log10(distance * 1000) + 41 + 20 * np.log10(fc / 5)
        WINNER_C2 = 26 * np.log10(distance * 1000) + 39 + 20 * np.log10(fc / 5)
        M_distance = distance * 1000
        R_s = 20
        ITU_R_l = np.abs(20 * np.log10(lanmuda * 1000 / (2 * np.pi * R_s))) + 30 * np.log10(M_distance / R_s)
        ITU_R_u = np.abs(20 * np.log10(lanmuda * 1000 / (2 * np.pi * R_s))) + 20 + 30 * np.log10(M_distance / R_s)
        ITU_R_m = np.abs(20 * np.log10(lanmuda * 1000 / (2 * np.pi * R_s))) + 6 + 30 * np.log10(M_distance / R_s)
        
        '''
        Model Selection Part
        '''
        w0 = PL.copy()
        w1 = One_slope.copy()
        w2 = REL.copy()
        w3 = Free_space.copy()
        w4 = WINNER_B1.copy()
        w5 = WINNER_C2.copy()
        w6 = ITU_R_u.copy()
        w7 = ITU_R_l.copy()
        w8 = ITU_R_m.copy()
        n = np.shape(w0)[0]
        
        '''
        RMSE
        '''
        d1 = w1 - w0
        d2 = w2 - w0
        d3 = w3 - w0
        d4 = w4 - w0
        d5 = w5 - w0
        d6 = w6 - w0
        d7 = w7 - w0
        d8 = w8 - w0
        
        '''
        RMSE标准公式： δ=sqrt[(Σ(di^2))/(n-1)]
        '''
        rmse1 = np.sqrt((np.sum(d1 ** 2, axis = 0)) / n)
        rmse2 = np.sqrt((np.sum(d2 ** 2, axis = 0)) / n)
        rmse3 = np.sqrt((np.sum(d3 ** 2, axis = 0)) / n)
        rmse4 = np.sqrt((np.sum(d4 ** 2, axis = 0)) / n)
        rmse5 = np.sqrt((np.sum(d5 ** 2, axis = 0)) / n)
        rmse6 = np.sqrt((np.sum(d6 ** 2, axis = 0)) / n)
        rmse7 = np.sqrt((np.sum(d7 ** 2, axis = 0)) / n)
        rmse8 = np.sqrt((np.sum(d8 ** 2, axis = 0)) / n)
        RMSE = np.array([rmse1, rmse2, rmse3, rmse4, rmse5, rmse6, rmse7, rmse8]).astype('complex64')
        
        maxrxy_0 = np.min(RMSE)
        column0 = np.where(RMSE == maxrxy_0)[0][0] + 1
        print('最小的RMSE值：%s' % str(column0))
        
        '''
        Grey System Thoery & MAPE
        '''
        x0 = GRG_MAPE_AVRG(w0, n)
        x1 = GRG_MAPE_AVRG(w1, n)
        x2 = GRG_MAPE_AVRG(w2, n)
        x3 = GRG_MAPE_AVRG(w3, n)
        x4 = GRG_MAPE_AVRG(w4, n)
        x5 = GRG_MAPE_AVRG(w5, n)
        x6 = GRG_MAPE_AVRG(w6, n)
        x7 = GRG_MAPE_AVRG(w7, n)
        x8 = GRG_MAPE_AVRG(w8, n)
        
        # 差异信息空间
        # 差异信息
        delta_00 = GRG_MAPE_delta(x0, x0)
        delta_01 = GRG_MAPE_delta(x0, x1)
        delta_02 = GRG_MAPE_delta(x0, x2)
        delta_03 = GRG_MAPE_delta(x0, x3)
        delta_04 = GRG_MAPE_delta(x0, x4)
        delta_05 = GRG_MAPE_delta(x0, x5)
        delta_06 = GRG_MAPE_delta(x0, x6)
        delta_07 = GRG_MAPE_delta(x0, x7)
        delta_08 = GRG_MAPE_delta(x0, x8)
        
        delta_1 = np.concatenate([delta_01, delta_02, delta_03, delta_04,
                                  delta_05, delta_06, delta_07, delta_08], axis = 0)
        # 环境参数
        delta_1_max = np.max(delta_1, axis = 0)
        delta_1_min = np.min(delta_1, axis = 0)
        
        # 分辨系数
        e = 0.5
        # 灰关联系数
        R_00 = GRG_MAPE_R(delta_1_min, delta_1_max, e, delta_00)
        R_01 = GRG_MAPE_R(delta_1_min, delta_1_max, e, delta_01)
        R_02 = GRG_MAPE_R(delta_1_min, delta_1_max, e, delta_02)
        R_03 = GRG_MAPE_R(delta_1_min, delta_1_max, e, delta_03)
        R_04 = GRG_MAPE_R(delta_1_min, delta_1_max, e, delta_04)
        R_05 = GRG_MAPE_R(delta_1_min, delta_1_max, e, delta_05)
        R_06 = GRG_MAPE_R(delta_1_min, delta_1_max, e, delta_06)
        R_07 = GRG_MAPE_R(delta_1_min, delta_1_max, e, delta_07)
        R_08 = GRG_MAPE_R(delta_1_min, delta_1_max, e, delta_08)
        # 灰关联度
        r_00 = GRG_MAPE_r1(R_00, n)
        r_01 = GRG_MAPE_r1(R_01, n)
        r_02 = GRG_MAPE_r1(R_02, n)
        r_03 = GRG_MAPE_r1(R_03, n)
        r_04 = GRG_MAPE_r1(R_04, n)
        r_05 = GRG_MAPE_r1(R_05, n)
        r_06 = GRG_MAPE_r1(R_06, n)
        r_07 = GRG_MAPE_r1(R_07, n)
        r_08 = GRG_MAPE_r1(R_08, n)
        grg = np.array([r_01, r_02, r_03, r_04, r_05,
                        r_06, r_07, r_08])
        
        # mape开始
        mape1 = np.sum(np.abs(w1 - w0) / w0) / n
        mape2 = np.sum(np.abs(w2 - w0) / w0) / n
        mape3 = np.sum(np.abs(w3 - w0) / w0) / n
        mape4 = np.sum(np.abs(w4 - w0) / w0) / n
        mape5 = np.sum(np.abs(w5 - w0) / w0) / n
        mape6 = np.sum(np.abs(w6 - w0) / w0) / n
        mape7 = np.sum(np.abs(w7 - w0) / w0) / n
        mape8 = np.sum(np.abs(w8 - w0) / w0) / n
        mape = np.array([1-mape1, 1-mape2, 1-mape3, 1-mape4, 1-mape5, 1-mape6, 1-mape7, 1-mape8])
        GRG_MAPE = 0.1 * grg + 0.9 *np.abs(mape)
        maxrxy_1 = np.max(GRG_MAPE, axis = 0)
        column1 = np.where(GRG_MAPE == maxrxy_1)[0][0] + 1
        print('最大的GRG-MAPE值：%s' % str(column1))
        
        '''
        PEARSON
        '''
        pear1 = pearson_fun(w0, w1, n)
        pear2 = pearson_fun(w0, w2, n)
        pear3 = pearson_fun(w0, w3, n)
        pear4 = pearson_fun(w0, w4, n)
        pear5 = pearson_fun(w0, w5, n)
        pear6 = pearson_fun(w0, w6, n)
        pear7 = pearson_fun(w0, w7, n)
        pwar8 = pearson_fun(w0, w8, n)
        pearson = np.array([pear1, pear2, pear3, pear4, pear5, pear6, pear7, pwar8])
        PEARSON_MAPE = 0.1 * pearson + 0.9 * mape
        maxrxy_2 = np.max(PEARSON_MAPE, axis = 0)
        column2 = np.where(PEARSON_MAPE == maxrxy_2)[0][0] + 1
        print('最大的PEARSON_MAPE值：%s' % str(column2))
        
        '''
        图形生成程序
        '''
        '''
        绘制保存fig1
        '''
        # 自动控制排版
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        ax.plot(M_distance, PL, 'b.', linewidth = 1.5, label = 'Measurement data')
        ax.plot(M_distance, One_slope, 'r-', linewidth = 1.5, label = 'One-slope model')
        ax.plot(M_distance, REL, 'c-', linewidth = 1.5, label = 'REL model')
        ax.plot(M_distance, Free_space, 'k--', linewidth = 1.5, label = 'Free-space model')
        ax.plot(M_distance, WINNER_B1, 'k-', linewidth = 1.5, label = 'WINNER II-B1')
        ax.plot(M_distance, WINNER_C2, 'g-', linewidth = 1.5, label = 'WINNER II-C2')
        ax.plot(M_distance, ITU_R_u, 'g--', linewidth = 1.5, label = 'ITU-R 1411(upper bound)')
        ax.plot(M_distance, ITU_R_l, 'r-.', linewidth = 1.5, label = 'ITU-R 1411(lower bound)')
        ax.plot(M_distance, ITU_R_m, 'b-.', linewidth = 1.5, label = 'ITU-R 1411(average value)')
        
        ax.set_xlabel('Distance in m', fontproperties = 'Times New Roman', fontsize = 8)
        ax.set_ylabel('Propagation path loss in dB', fontproperties = 'Times New Roman', fontsize = 8)
        ax.grid(True)
        plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0.5)
        
        plt.savefig('../results/power_domain/Propagation_path_loss_mainfunction_fig1.png')
        
        '''
        debug message
        '''
        if debug_mode:
            print('rsl')
            print(rsl.shape)
            print(rsl[0:6])
            print(rsl[-6:])
            print('distance')
            print(distance.shape)
            print(distance[0:6])
            print(distance[-6:])
            print('lanmuda')
            print(lanmuda)
            print('k')
            print(k)
            print('PL')
            print(PL.shape)
            print(PL[0:6])
            print(PL[-6:])
            print('D_06')
            print(D_06)
            print('D1')
            print(D1)
            print('D2')
            print(D2)
            print('sum_reflection')
            print(sum_reflection)
            print('D_1')
            print(D_1)
            print('D_2')
            print(D_2)
            print('D3')
            print(D3)
            print('D33')
            print(D33)
            print('d_los')
            print(d_los)
            print('dif')
            print(dif)
            print('h_1_1')
            print(h_1_1)
            print('h_2_2')
            print(h_2_2)
            print('R_eff')
            print(R_eff.shape)
            print(R_eff)
            print('R_eff_roughness_25')
            print(R_eff_roughness_25.shape)
            print(R_eff_roughness_25)
            print('R_eff_roughness_5')
            print(R_eff_roughness_5.shape)
            print(R_eff_roughness_5)            
            print('R_eff_roughness_1')
            print(R_eff_roughness_1.shape)
            print(R_eff_roughness_1)
            print('R_eff_roughness_2')
            print(R_eff_roughness_2.shape)
            print(R_eff_roughness_2)
            print(L33[-6:])
            print('w1')
            print(w1.shape)
            print(w1[0:6])
            print(w1[-6:])
            print('w2')
            print(w2.shape)
            print(w2[0:6])
            print(w2[-6:])
            print('w3')
            print(w3.shape)
            print(w3[0:6])
            print(w3[-6:])
            print('w4')
            print(w4.shape)
            print(w4[0:6])
            print(w4[-6:])
            print('w5')
            print(w5.shape)
            print(w5[0:6])
            print(w5[-6:])
            print('w6')
            print(w6.shape)
            print(w6[0:6])
            print(w6[-6:])
            print('w7')
            print(w7.shape)
            print(w7[0:6])
            print(w7[-6:])
            print('w8')
            print(w8.shape)
            print(w8[0:6])
            print(w8[-6:])
            print('n')
            print(n)
            print('rmse1, rmse2, rmse3, rmse4, rmse5, rmse6, rmse7, rmse8')
            print(RMSE)
            print('x0')
            print(x0.shape)
            print(x0[0:6])
            print(x0[-6:])
            print('delta_1')
            print(delta_1.shape)
            print(delta_1[0:6])
            print(delta_1[500:506])
            print(delta_1[-6:])
            print('R_00')
            print(R_00.shape)
            print(R_00[0:6])
            print(R_00[-6:])
            print('grg')
            print(grg.shape)
            print(grg)
            print('mape')
            print(mape.shape)
            print(mape)
            print('maxrxy_1, column1')
            print(maxrxy_1, column1)
            print('PEARSON_MAPE')
            print(PEARSON_MAPE.shape)
            print(PEARSON_MAPE)
            print('maxrxy_2, column2')
            print(maxrxy_2, column2)
            
            
    
    def f(self, x2, h_1, h_2, r_e, d):
        return ([x2[0] + np.arccos(( r_e + h_1 - r_e * np.cos(x2[0])) /
                 (((h_1 + r_e) ** 2 + (r_e ** 2) - (2 * (h_1 + r_e) * r_e * np.cos(x2[0]))) ** 0.5))
                 - (x2[1] + np.arccos((r_e + h_2 - r_e * np.cos(x2[1])) / (((h_2 + r_e) ** 2 + (r_e ** 2)
                 - (2 * (h_2 + r_e) * r_e * np.cos(x2[1]))) **0.5))), 
                 x2[0] + x2[1] - d / r_e])
    

if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    Propagation_path_loss()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))
