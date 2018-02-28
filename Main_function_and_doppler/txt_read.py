# coding=utf-8
import numpy as np
import os
import timeit

'''
读取并转换txt文件
'''
class txt_read():
    # signal_CIR
    signal_CIR = []                                                       # signal_CIR初始化，其长度是.txt文件数量
    txt_num = 0
    
    def __init__(self, path):
        # 遍历path目录选取所有.txt文件
        file_list = []
        for dir_path, dir_names, file_names in os.walk(path):             # 只选取.txt文件
            for file_name in file_names:
                if os.path.splitext(file_name)[-1] == '.txt':
                    file_list.append(os.path.join(dir_path, file_name))
        
        # 提取txt文件名的前一部分，这里需要保证排序的数字的前一部分必须确定，且以'_'分割
        file_header = '_'.join(os.path.splitext(file_list[0])[0].split('_')[:-1])
        # 提取txt文件名中排序的部分
        file_list = [os.path.splitext(file_name)[0].split('_')[-1] for file_name in file_list]
        file_list.sort()
        # 对文件名进行拼接
        file_list = [file_header + '_' + file_name + '.txt' for file_name in file_list]
        print(file_list)
        self.txt_num = len(file_list)
        
        # 对每个.txt文件调用read方法处理
        for file in file_list:
            self.__read(file)
    
    def __read(self, file):
        txt_lines = []
        with open(file, mode='r') as fp:                                  # 打开txt文件，读入所有的行
            txt_lines = fp.readlines()

            
        '''
        从第7行开始，每隔4行，采取实部和虚部
        '''
        real = []                                                         # real和imag一个二维列表，总行数是实部或虚部的行数
        imag = []
        for i in range(6, len(txt_lines), 4):
            txt_lines[i] = txt_lines[i].rstrip('\n')                      # 去掉数据行最后的换行符
            txt_lines[i + 1] = txt_lines[i + 1].rstrip('\n')
            real.append(txt_lines[i].split(', '))                         # 实部一行存入列表
            imag.append(txt_lines[i + 1].split(', '))                     # 紧接着的虚部一行存入列表
        
        '''
        将每一个对应的实部和虚部相加，存入一个二维数组
        对这个二维数组的每个元素求共轭
        对共轭后的数组，按照每一行进行傅里叶反变换
        最后得到结果存入signal_CIR
        '''
        re_array = np.array(real, dtype='float')
        im_array = np.array(imag, dtype='float')
        signal_array = re_array + im_array * np.complex('0+1j')
        signal_array = np.conj(signal_array)                              # 对二维数组每个元素进行共轭
        
        i = 0
        signal_cir = np.zeros_like(signal_array, dtype='complex64')
        for i in range(signal_array.shape[0]):                            # 对每一行进行傅里叶反变换
            signal_cir[i] = np.fft.ifft(signal_array[i], axis = 0)
        
        self.signal_CIR.append(signal_cir)
    
if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    txt_info = txt_read('txt')
    for signal_cir in txt_info.signal_CIR:
        print(signal_cir.shape)
        print(signal_cir[0][0:6])
    
    end_time = timeit.default_timer()
    print(str(end_time - begin_time))