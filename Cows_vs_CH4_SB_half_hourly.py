# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 13:36:13 2020

@author: Camilo Rey and Lily Klinek
"""


# Import Libraries

import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta


## reading L3 files (Flux data)

dnames = ['WD','H', 'LE', 'wc', 'wm', 'wq', 'wt']

#hf = h5py.File(r'/Users/Lilyk/Desktop/Sherman_Barn_1/SB_2019365_L3.mat', 'r')
hf = h5py.File(r'D:\FluxData\Sherman_Barn\SB_2019365_L1.mat', 'r')
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


## Reading cow count csv file

#cow_data = np.array(pd.read_csv(r'/Users/Lilyk/Desktop/Sherman_Barn_1/cow_count2.csv'))
cow_data = np.array(pd.read_csv(r'C:\Users\biomet\Box Sync\UC-Berkeley\Sherman_Barn\Code\SB_code_share/cow_count.csv'))

## datetime for cow count file
nrowsC = len(cow_data[:,0])
date_cow_all = []

for pn in range(0,nrowsC):
    date_cow = datetime(int(cow_data[pn,0]),int(cow_data[pn,1]),int(cow_data[pn,2]),int(cow_data[pn,3]),int(cow_data[pn,4]))
    date_cow=date_cow+timedelta(minutes=15)
    date_cow_all.append(date_cow)

cow_effect=cow_data[:,5]/cow_data[:,7]
cow_effect2=cow_effect[...,None]
cow_data=np.append(cow_data,cow_effect2,1)

## plotting preliminar

plt.figure(figsize=(10,8))
plt.plot(df['WD'],df['wm'],'.')
plt.xlabel('wind directon')
plt.ylabel('methane flux (nmol m^-2 s^-1)')
plt.show()
plt.title('Half-hourly Wind direction versus methane flux (unfiltered)')

plt.figure(figsize=(10,8))
plt.plot(mf['datetime'],mf['Mot'],'.')
plt.xlabel('time')
plt.ylabel('motion sensor counts')
plt.title('Half-hourly Motion sensor counts (unfiltered)')

plt.figure(figsize=(10,8))
plt.plot(date_cow_all,cow_data[:,5],'.')
plt.xlabel('date')
plt.ylabel('cow count')
plt.title('Half-hourly Manual cow count (unfiltered)')



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

# Exporting the index
tabIXS = pd.DataFrame(IXS);
outname = r'C:\Users\biomet\Box Sync\UC-Berkeley\Sherman_Barn\Code\IXS_2019.csv'    
tabIXS.to_csv(outname, float_format='%.3f', na_rep='nan')

# Indexing L3 variables
# We start with a Pandas data frame, then we index one column to create a pandas series
# And then we index based on IXS and create a list (wmf)
    # This list is converted to a panda series and then to a numpy array
    
wm = df['wm']
wmf = pd.Series([wm[i] for i in IXS]).to_numpy()

Mot = mf['Mot']
Motf = pd.Series([Mot[i] for i in IXS]).to_numpy()

datetime = df['datetime']
datetimef = pd.Series([datetime[i] for i in IXS]).to_numpy()

wd = df['WD']
wdf = pd.Series([wd[i] for i in IXS]).to_numpy()

wdix=wdf>245

# Filtering variables
Motff=Motf[wdix]
wmff=wmf[wdix]
cow_dataF=cow_data[wdix,:]
datetimeff=datetimef[wdix]



# Plots with filter
plt.figure(figsize=(10,7))
plt.plot(Motff, wmff, '.')
plt.xlabel('cows (filtered motion sensor data)', fontsize=13)
plt.ylabel('methane flux (nmol m-2 s-1)', fontsize=13)
plt.title ('Methane Flux (motion sensor)', fontsize=14)
plt.title('Half-hourly Motion sensor data versus methane fluxes (WD filtered)')

plt.figure(figsize=(10,7))
plt.plot(cow_dataF[:,5], wmff, '.', color='blue')
plt.xlabel('cows (filtered phenocam data)', fontsize=13)
plt.ylabel('methane flux (nmol m-2 s-1)', fontsize=13)
plt.title(('Methane Flux (phenocam)'), fontsize=14)
plt.title('Half-hourly Phenocam count versus methane fluxes (WD filtered)')

plt.figure(figsize=(10,7))
plt.plot(cow_dataF[:,8], wmff, '.', color='blue')
plt.xlabel('Cow effect (number/distance) (phenocam)', fontsize=13)
plt.ylabel('methane flux (nmol m-2 s-1)', fontsize=13)
plt.title('Half-hourly Phenocam count weighed by distance versus methane fluxes (WD filtered)')

plt.figure(figsize=(10,7))
plt.plot(datetimeff, cow_dataF[:,5], marker='.', color='blue', label= 'Phenocam (filtered)',)
plt.plot(datetimeff, Motff, marker='.', color='olive', label= 'Motion Sensor (filtered)',)
plt.xlabel('date', fontsize=13)
plt.ylabel('cow count', fontsize=13)
leg = plt.legend()
plt.title('Comparison of counts with motion sensor versus cow count', fontsize=14)

plt.figure(figsize=(10,7))
plt.plot(cow_dataF[:,5], Motff, '.')
plt.xlabel('phenocam cow count (filtered for wind direction)', fontsize=13)
plt.ylabel('motion sensor cow count (filtered for wind direction)', fontsize=13)
plt.title('Cow Count Sources', fontsize=14)
plt.title('Comparison of counts with motion sensor versus cow count (WD filtered)', fontsize=14)

plt.figure(figsize=(10,7))
plt.plot(cow_dataF[:,7], wmff, '.')
plt.xlabel('cow distance (filtered) (meters)', fontsize=13)
plt.ylabel('methane flux (nmol m-2 s-1)', fontsize=13)
plt.title('Distance and Methane Fluxes', fontsize=14)
plt.title('Comparison of cow distance versus methane fluxes (WD filtered)', fontsize=14)



