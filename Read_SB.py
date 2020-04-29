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


## reading L3 files (Flux data)

dnames = ['WD','H', 'LE', 'wc', 'wm', 'wq', 'wt']

#f = h5py.File(r'/Users/Lilyk/Desktop/Sherman_Barn_1/SB_2019365_L3.mat', 'r')
hf = h5py.File(r'D:\FluxData\Sherman_Barn\SB_2019365_L3.mat', 'r')
nrows = hf['data']['year'].size

df = pd.DataFrame();

for dn in dnames:
    df[dn] = hf['data'][dn][:].reshape((nrows,))


# Datetime variable for Flux file
    
df['Mdate'] = hf['data']['Mdate'][:].reshape((nrows,))
unixTime=round((df.Mdate-719529)*86400)
utall=[]

for i in range(len(df['Mdate'])):
    ut=pd.Timestamp(unixTime[i], unit='s')
    utall.append(ut)    
   
df['datetime'] = utall


## Exporting file
df.set_index('datetime')    
#outname = r'/Users/Lilyk/Desktop/Sherman_Barn_1/SB_2019365_export.csv'
outname = r'C:\Users\biomet\Box Sync\UC-Berkeley\Sherman_Barn\Code\SB_2019365_export.csv'
df.to_csv(outname, float_format='%.3f', na_rep='nan')


## reading met files

dnames = ['Mot', 'Mdate_met']

#hf = h5py.File(r'/Users/Lilyk/Desktop/Sherman_Barn_1/SBMet_2019365.mat', 'r')
hf = h5py.File(r'D:\FluxData\Sherman_Barn/met/SBMet_2019365.mat', 'r')
nrows = hf['data']['TA'].size

mf = pd.DataFrame();


for dn in dnames:
    mf[dn] = hf['data'][dn][:].reshape((nrows,))


# Datetime variable for Met file
    
mf['Mdate_met'] = hf['data']['Mdate_met'][:].reshape((nrows,))
unixTime=round((mf.Mdate_met-719529)*86400)
mtall=[]

for i in range(len(mf['Mdate_met'])):
    mt=pd.Timestamp(unixTime[i], unit='s')
    mtall.append(mt)    
   
mf['datetime'] = mtall


## reading cow count csv file

#cow_data = np.array(pd.read_csv(r'/Users/Lilyk/Desktop/Sherman_Barn_1/cow_count2.csv'))
cow_data = np.array(pd.read_csv(r'C:\Users\biomet\Box Sync\UC-Berkeley\Sherman_Barn\Code\SB_code_share/cow_count.csv'))


## datetime for cow count file
nrowsC = len(cow_data[:,0])

date_cow_all = []

for pn in range(0,nrowsC):
    date_cow = datetime(int(cow_data[pn,0]),int(cow_data[pn,1]),int(cow_data[pn,2]),int(cow_data[pn,3]),int(cow_data[pn,4]))
    date_cow=date_cow+timedelta(minutes=15)
    date_cow_all.append(date_cow)


## plotting

plt.plot(df['WD'],df['wm'],'.')
plt.xlabel('wind directon')
plt.ylabel('methane flux (nmol m^-2 s^-1)')
plt.show()


plt.plot(mf['datetime'],mf['Mot'],'.')
plt.xlabel('time')
plt.ylabel('motion sensor counts')
plt.show()


plt.plot(date_cow_all,cow_data[:,5])
plt.xlabel('date')
plt.ylabel('cow count')
plt.show()

plt.plot(date_cow_all, cow_data[:,7])
plt.xlabel('date')
plt.ylabel('distance (meters)')
plt.show()

plt.plot(df['datetime'], df['wm'])
plt.show()


## Matching the indices of the cow count times

# First, round to the nearest half-hour

import pandas as pd
# date_cow_pd=pd.Timestamp(date_cow_all[0])
# RdateCow=date_cow_pd.round('30min').to_pydatetime()
def myfunction(date_cow):
    date_cow_pd=pd.Timestamp(date_cow)
    RdateCow=date_cow_pd.round('30min').to_pydatetime()
    return RdateCow

vfunc = np.vectorize(myfunction)
rdate_cowf = vfunc(date_cow_all)

# Matching


IXS=[]
for pn in range(0,nrowsC):
    ixs=np.where(df['datetime']== np.datetime64(rdate_cowf[pn]))
    ix2=int(ixs[0])
    IXS.append(ix2)
    

# Indexing L3 variables
# We start with a Pandas data frame, then we index one column to create a pandas series
# And then we index based on IXS and create a list (wmf)
    # This list is converted to a panda series and then to a numpy array
    
#matlab notation: wmf = df[IXS,5]
wm = df['wm']
wmf = pd.Series([wm[i] for i in IXS]).to_numpy()

Mot = mf['Mot']
Motf = pd.Series([Mot[i] for i in IXS]).to_numpy()

datetime = df['datetime']
datetimef = pd.Series([datetime[i] for i in IXS]).to_numpy()

wd = df['WD']
wdf = pd.Series([wd[i] for i in IXS]).to_numpy()

wdix=wdf>260

Motff=Motf[wdix]
wmff=wmf[wdix]

# plotting 

# All
plt.plot(Motf, wmf, '.')
plt.xlabel('cows (motion sensor data)')
plt.ylabel('methane flux (nmol m^-2s^-1)')
plt.show()

# With filter
plt.plot(Motff, wmff, '.')
plt.xlabel('cows (motion sensor data)')
plt.ylabel('methane flux (nmol m^-2s^-1)')
plt.show()  



plt.plot(datetimef, cow_data[:,5], marker='', color='blue')
plt.plot(datetimef, Motf, marker='', color='olive')
plt.show()

plt.plot(cow_data[:,5], Motf, '.')
plt.xlabel('phenocam cow count')
plt.ylabel('motion sensor cow count')
plt.show()
