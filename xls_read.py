# coding=utf-8

import numpy as np
import xlrd

'''
读取并转换tx的excel
'''
class tx_xls_read():
    GPS_tx = np.zeros((1))
    v_tx = np.zeros((1))
    t_start = 64;                                                                        # 读取excel的开始时间，第几行，包括这一行
    t_stop =  69;                                                                        # 读取excel的结束时间，第几行，包括这一行
    
    def __init__(self, file):
        # 从file加载第一个工作表
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_index(0)
        GPS_tx_list_lat = sheet.col_values(8, self.t_start - 1, self.t_stop)             # 获取第9列的纬度
        GPS_tx_list_long = sheet.col_values(9, self.t_start - 1, self.t_stop)            # 获取第10列的经度
        
        GPS_tx_lat = np.array(GPS_tx_list_lat, dtype='float')                            # 将列表转换为数组(一个行向量)
        GPS_tx_long = np.array(GPS_tx_list_long, dtype='float')
        self.GPS_tx = np.vstack((GPS_tx_lat, GPS_tx_long)).T                             # 将纬度的行向量与经度的行向量进行列合并，求转置，就得到了需要的(lat, long)矩阵
        
        v_tx_list = sheet.col_values(4, self.t_start - 1, self.t_stop)                   # 获取第5列的速度
        self.v_tx = np.transpose([np.array(v_tx_list)])                                  # 转变为列向量
        
'''
读取并转换rx的excel
'''
class rx_xls_read():
    GPS_rx = np.zeros((1))
    v_rx = np.zeros((1))
    t_start = 64;                                                                        # 读取excel的开始时间，第几行，包括这一行
    t_stop =  69;                                                                        # 读取excel的结束时间，第几行，包括这一行
    
    def __init__(self, file):
        # 从file加载第一个工作表
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_index(0)
        GPS_rx_list_lat = sheet.col_values(9, self.t_start - 1, self.t_stop)             # 获取第9列的纬度
        GPS_rx_list_long = sheet.col_values(10, self.t_start - 1, self.t_stop)           # 获取第10列的经度
        
        GPS_rx_lat = np.array(GPS_rx_list_lat, dtype='float')                            # 将列表转换为数组(一个行向量)
        GPS_rx_long = np.array(GPS_rx_list_long, dtype='float')
        self.GPS_rx = np.vstack((GPS_rx_lat, GPS_rx_long)).T                             # 将纬度的行向量与经度的行向量进行列合并，求转置，就得到了需要的(lat, long)矩阵
        
        v_rx_list = sheet.col_values(5, self.t_start - 1, self.t_stop)
        self.v_rx = np.transpose([np.array(v_rx_list)])
    
if __name__ == '__main__':
    tx_xls = tx_xls_read('excel/81_out_tx.xls')
    print(tx_xls.GPS_tx.shape)
    print(tx_xls.v_tx)
    
    rx_xls = rx_xls_read('excel/81_out_rx.xls')
    print(rx_xls.GPS_rx.shape)
    print(rx_xls.v_rx)
    
    print(max(tx_xls.v_tx, rx_xls.v_rx))
    