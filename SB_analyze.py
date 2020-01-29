# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 09:34:57 2020

@author: biomet
"""

import h5py
with h5py.File('SB_2019365_L2.mat', 'r') as file:
    print(list(file.keys()))
    
with h5py.File('SB_2019365_L2.mat', 'r') as file:
    a = list(file['data'])
    
 DOY=a[5]  
 
 for k, v in a.items():
    arrays[k] = np.array(v)