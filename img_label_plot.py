# coding=utf-8

from plot_funcs import *
from multiprocessing import Process

def img_label_plot(img_name):
    plot_fun_name = 'plot_' + img_name.split('.')[0]
    a = Process(target = eval(plot_fun_name))
    a.start()
    return