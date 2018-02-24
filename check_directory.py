# coding=utf-8
import os

def check_directory():
    current_directory = os.getcwd()
    # 即将要检查或者生成的文件夹
    directory_list = ['icon', 'params', 'plot_params', 'results', os.path.join('results', 'angel_domain'), 
                      os.path.join('results', 'delay_domain'), os.path.join('results', 'frequency_domain'),
                      os.path.join('results', 'Main_function_and_doppler'), os.path.join('results', 'power_domain')]
    # 循环检测文件夹是否存在，不存在则创建
    for i in directory_list:
        directory = os.path.join(current_directory, i)
        if not os.path.isdir(directory):
            os.makedirs(directory)
    
    
if __name__ == '__main__':
    check_directory()
