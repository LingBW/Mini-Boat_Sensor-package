# -*- coding: utf-8 -*-
"""
Created on 12 Oct 2016 
Accesses files in backup directory and looks for sensor data
@author: JiM using Huanxin's previous "getap3.py" routine
"""
from matplotlib.dates import date2num
import time
import os
import sys
import subprocess
from dateutil import parser
import glob
import json
import datetime
import numpy as np

#os.chdir('/home/jmanning/py/')
files=sorted(glob.glob('./jfiles/*.json'))
#print type(files),files  #<type 'list'> ['./jfiles/20160108.000000.json',.....]
f_output_sensor=open('emolt_ap3_sensor_rockstar.dat','w')  
hd = 'ID,ESN,TIME,LON,LAT,DEPTH,NAN,MEANAIRTEMP,MINAIRTEMP,MAXAIRTEMP,MEANSEATEMP,MINSEATEMP,MAXSEATEMP\n'

f_output_sensor.write(hd)

#f_output_sensor=open('/net/pubweb_html/drifter/emolt_ap3_sensor_rockstar.dat','w')
ddn = 0; tt = 0; gd = 0
for i in files:
    #with open(i) as data_file:    
    data = json.load(open(i)); #print data; break
    esn=data['momentForward'][0]['Device']['esn'];#print type(esn); break
    if (esn=='300234063371590'):#change last number to "0" to get rockstar
        #print data,'\n'
        tt = tt+1
        id_idn1=160410701
        depth_idn1=0.1
        moment = data['momentForward'][0]['Device']['moments'][0]['Moment']
        #print len(moment['points'])
        # filter good data.
        if len(moment['points'])==14 and len(moment['points'][2]['PointHex']['hex'])==36:
            d = moment['points'][2]['PointHex']['hex'][18:36]
            d1 = moment['points'][2]['PointHex']['hex'][18:27]
            d2 = moment['points'][2]['PointHex']['hex'][27:36]
            try:
                float(d)
            except:
                continue
            if d1 == '111111111' or d2 == '111111111':
                continue
            #if moment['points'][2]['PointHex']['hex'][18:21]!='000':]
            #print moment['points'][2]['PointHex']['hex']
            gd = gd+1
            try:            
                meanairtemp=float(moment['points'][2]['PointHex']['hex'][18:21])/10.-30.
                minairtemp=float(moment['points'][2]['PointHex']['hex'][21:24])/10.-30.
                maxairtemp=float(moment['points'][2]['PointHex']['hex'][24:27])/10.-30.
                meanseatemp=float(moment['points'][2]['PointHex']['hex'][27:30])/10.-30.
                minseatemp=float(moment['points'][2]['PointHex']['hex'][30:33])/10.-30.
                maxseatemp=float(moment['points'][2]['PointHex']['hex'][33:36])/10.-30. 
            
                lat=moment['points'][4]['PointLoc']['Lat'] #
                lon=moment['points'][4]['PointLoc']['Lon']
                
            except:
                ddn = ddn+1
                print '%d Dad Data.'%ddn,i
            else:
                # ID,ESN,MONTH,DAY,HOUR,MINUTE,DAYS,LON,LAT,DEPTH,NAN,MEANAIRTEMP,MINAIRTEMP,MAXAIRTEMP,MEANSEATEMP,MINSEATEMP,MAXSEATEMP,YEAR
                dd=parser.parse(moment['date']); #print dd   
                ddt = str(dd)
                if meanairtemp < -10: print i
                '''yr1=dd.year
                mth1=dd.month
                day1=dd.day
                hr1=dd.hour
                mn1=dd.minute
                yd1=date2num(datetime.datetime(yr1,mth1,day1,hr1,mn1))-date2num(datetime.datetime(yr1,1,1,0,0))
                                
                f_output_sensor.write(str(id_idn1).rjust(10)+ ", "+str(esn[-4:]).rjust(7)+ ", "+str(mth1).rjust(2)+ ", " +
                str(day1).rjust(2)+ ", " +str(hr1).rjust(3)+ ", " +str(mn1).rjust(3)+ ", " )
                f_output_sensor.write(("%10.7f") %(yd1))# Days since 1/1/2017 00:00 #'''
                f_output_sensor.write(str(id_idn1)+ ", "+str(esn[-4:])+ ", "+ddt)
                f_output_sensor.write( ", "+("%10.5f") %(lon)+', '+("%10.5f") %(lat)+', '+str(float(depth_idn1)).rjust(4)+  ", "+str(np.nan))
                f_output_sensor.write(", "+str(meanairtemp).rjust(6)+', '+str(minairtemp).rjust(6)+', '+str(maxairtemp).rjust(6)+ ", " 
                +("%8.2f") %(meanseatemp)+ ", "+("%6.2f") %(minseatemp)+", "+("%6.2f") %(maxseatemp)+'\n')  #+", "+("%6.0f") %(yr1) 
f_output_sensor.close()
print 'tt,gd,ddn',tt,gd,ddn
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
