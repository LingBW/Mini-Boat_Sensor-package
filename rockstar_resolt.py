# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 15:32:18 2017

@author: bling
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('emolt_ap3_sensor_rockstar.dat',parse_dates={'Time':[2]},index_col='Time')
#data1 = pd.read_csv('MYC_019.txt',skiprows=1,sep="\s+",low_memory=False,parse_dates={'Time':[1]},index_col='Time')
data1 = pd.read_table('MYC_019.txt',skiprows=2,low_memory=False,parse_dates={'Time':[0]},index_col='Time')
################################# Test data ###############################'''
'''#print type(data)
for i in data['MEANAIRTEMP']:
    if i<0: print i
################################# Plot #######################################'''
'''fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(data['MAXAIRTEMP'],'r')
ax.plot(data['MAXSEATEMP'],'b')
#ax.set_xticks(xt)
plt.title('Air&Water temperature comparison')
#ax.set_xticklabels(time,rotation=30,fontsize='small')
#ax.set_ylabel('Temperature(Deg C)')
#plt.savefig('Air&Water_temperature_comparison.png',dpi=100,bbox_inches='tight')#'''
rd = data['MEANAIRTEMP'].resample('M').mean()
rd1 = data['MEANSEATEMP'].resample('M').mean()
rd.plot(label='Top')
rd1.plot(label='Bottom')
#cd = data['MAXAIRTEMP'].ix['08-2016':'04-2017'].resample('M').mean()
#cd1 = data['MINAIRTEMP'].ix['08-2016':'04-2017'].resample('M').mean()
cd = data1['Temperature_9986748_deg_F'].ix['08-2016':'04-2017'].resample('M').mean()
cd1=(cd-32)/1.8
cd1.plot(label='DataGarrison Systems') #'''
#data['MEANAIRTEMP'].plot()
#data['MAXAIRTEMP'].ix['2017':].plot()
#data[['MAXAIRTEMP','MEANAIRTEMP','MINAIRTEMP']].plot()
plt.legend()
plt.show()