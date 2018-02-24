# coding=utf-8
import numpy as np

def small_scale_match(small_seq, seq):
    value = []
    for i in range(0, len(small_seq) - 1):
        a = np.shape(small_seq[i])[0]
        value.append(np.linspace(seq[i], seq[i + 1], a))
    return value    
