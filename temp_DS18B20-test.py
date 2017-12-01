#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:32:13 2015
@author: Bingwei Ling
"""

import os, glob, time
import serial,numpy
import datetime

#cdatas = [[],[],[],[],[]] #celcius degree lists
cdatas = {}

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()

    return lines
 
def read_temp():
    #os.system('sudo modprobe w1-gpio')
    #os.system('sudo modprobe w1-therm')
    dic_dates = {}
    device_folder = glob.glob('/sys/bus/w1/devices/28*')
    # If no such files, return None, and , send message '00000'
    if not device_folder:
        return None
    
    for i in range(len(device_folder)):
        key = str(i+1)
        device_file = device_folder[i] + '/w1_slave'
        try:
            lines = read_temp_raw(device_file)
        except:
            dic_dates[key] = 0  # 1
            continue
        if lines[0].strip()[-3:] != 'YES':
            dic_dates[key] = 0  # 2
            continue
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0  #+ 30  avoid negative value.
            #temp_f = temp_c * 9.0 / 5.0 + 32.0
            if temp_c>0 and temp_c<100:
                dic_dates[key] = temp_c #*10
            else :
                dic_dates[key] = 0  # 3
    
    return dic_dates #, temp_f #return a list of each temperature-sensor value.

sendtime = datetime.datetime.now()
while True:
    cs = read_temp()
    # Loops for no temp-sensors.
    if not cs :
        print "No sensors detected!"
    else:
        print cs
    time.sleep(1)
