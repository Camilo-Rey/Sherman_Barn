# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 13:36:13 2020

@author: jverfail
Modified by Camilo Rey
"""

import h5py
import pandas as pd
#from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta

# reading csv file
cow_data = np.array(pd.read_csv('cow_count.csv'))

# reading L3 files

dnames = ['WD','H', 'LE', 'wc', 'wm', 'wq', 'wt', 'mot']

hf = h5py.File(r'/Users/Lilyk/Desktop/Sherman_Barn_1/SB_2019365_L3.mat', 'r')
nrows = hf['data']['year'].size

df = pd.DataFrame();




for dn in dnames:
    df[dn] = hf['data'][dn][:].reshape((nrows,))


## Datetime variable
    
df['Mdate'] = hf['data']['Mdate'][:].reshape((nrows,))
unixTime=round((df.Mdate-719529)*86400)
utall=[]

for i in range(len(df['Mdate'])):
    ut=pd.Timestamp(unixTime[i], unit='s')
    utall.append(ut)    
   
df['datetime'] = utall

df.set_index('datetime')    
outname = r'/Users/Lilyk/Desktop/Sherman_Barn_1/SB_2019365_L3.mat'
df.to_csv(outname, float_format='%.3f', na_rep='nan')

## reading met files

dnames = ['Mot', 'Mdate_met']

hf = h5py.File(r'/Users/Lilyk/Desktop/Sherman_Barn_1/SBMet_2019365.mat', 'r')
nrows = hf['data']['TA'].size

mf = pd.DataFrame();




for dn in dnames:
    mf[dn] = hf['data'][dn][:].reshape((nrows,))


# Datetime variable
    
mf['Mdate_met'] = hf['data']['Mdate_met'][:].reshape((nrows,))
unixTime=round((mf.Mdate_met-719529)*86400)
mtall=[]

for i in range(len(mf['Mdate_met'])):
    mt=pd.Timestamp(unixTime[i], unit='s')
    mtall.append(mt)    
   
mf['datetime'] = mtall

## datetime for cow count file
date_cow = datetime(cow_data[:,0],cow_data[:,1],cow_data[:,2],cow_data[:,3],cow_data[:,4])
nrows = len(cow_data[:,0])

date_all = []

for pn in range(0,nrows):
    date_cow = datetime(cow_data[int(pn),0],cow_data[int(pn),1],cow_data[int(pn),2],cow_data[int(pn),3],cow_data[int(pn),4])
    date_all.append(date_cow)


## plotting

plt.plot(df['WD'],df['wm'],'.')
plt.xlabel('wind directon')
plt.ylabel('methane flux (nmol m^-2 s^-1)')
plt.show()


plt.plot(mf['datetime'],mf['Mot'],'.')
plt.xlabel('time')
plt.ylabel('motion sensor counts')
plt.show()

plt.plot(date_all,cow_data[:,5])
plt.xlabel('date')
plt.ylabel('cow count')
plt.show()

plt.plot(date_all, cow_data[:,7])
plt.xlabel('date')
plt.ylabel('distance (meters)')
plt.show()

plt.plot(df['datetime'], df['wm'])
plt.show()

