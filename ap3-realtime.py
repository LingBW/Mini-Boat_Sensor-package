# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:04:46 2016

@author: bling
"""

import os, glob, time
import serial
import numpy
from datetime import datetime,timedelta

ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1) # linux
time.sleep(1)
ser.writelines('\n')       
time.sleep(1)
ser.writelines('\n')
time.sleep(1)
ser.writelines('\n')       
time.sleep(1)
ser.writelines('t'+'\n')
#l0=ser.readline()
#print l0
l=ser.readall()
ser.close()
print l
print len(l),type(l)
fn = l.find('Real time:'); print fn
nu = l[fn+11:fn+26]; print nu
RealTime = datetime(1970, 1, 1, 0, 0, 0, 0)+timedelta(seconds=float(nu))
print RealTime
