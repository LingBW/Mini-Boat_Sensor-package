#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:32:13 2015
@author: Bingwei Ling
"""

import os, glob, time
import serial,numpy
import datetime
 
# Hard codes
transmit = 'ON' # ON,OFF
send_interval = 7100 # unit: seconds. eg 2*3600
temp_inter = 58 #collect data interval, every minute
sd_num = 3 #send data times

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
    dic_dates = {}
    device_folder = glob.glob('/sys/bus/w1/devices/28*')
    # If no such files, return None, and , send message '00000'
    if not device_folder:
        return None
    
    for i in device_folder:
        key = i[-12:]
        device_file = i + '/w1_slave'
        try:
            lines = read_temp_raw(device_file)
        except:
            dic_dates[key] = 0
            continue
        if lines[0].strip()[-3:] != 'YES':
            dic_dates[key] = 0
            continue
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0 + 30  # avoid negative value.
            #temp_f = temp_c * 9.0 / 5.0 + 32.0
            if temp_c>0 and temp_c<100:
                dic_dates[key] = temp_c*10
            else :
                dic_dates[key] = 0
    
    return dic_dates #, temp_f #return a list of each temperature-sensor value.

def transdata(mes):
    try:
        try:
            ser=serial.Serial('/dev/ttyUSB0',9600) # linux
        except:
            ser=serial.Serial('/dev/ttyUSB1',9600)
        # send the data
        time.sleep(1)
        ser.writelines('\n')       
        time.sleep(1)
        ser.writelines('\n')
        time.sleep(1)
        ser.writelines('yab'+'\n') # Force the given message to idle.
        time.sleep(5)
        ser.writelines('\n')
        time.sleep(1)
        ser.writelines('\n')
        time.sleep(1)
        ser.writelines('ylb'+mes+'\n')
        time.sleep(1) # 1100s 18 minutes        
        ser.close() # close port
        time.sleep(1)
    except:
        print 'Can not send data.'  #'''
        return 0
    return 1
    
ki = 0 # count failsure times.
kp = 0 # Halt Pi
time.sleep(3)	
sendtime = datetime.datetime.now()
while True:
    looptime = datetime.datetime.now()
    cs = read_temp()
    #print looptime,cs
    
    # Loops for no temp-sensors.
    if not cs:
        time.sleep(0.2)
        print ki
        if ki == 100:
            nmes = '00000'
            transdata(nmes)
            ki = 0
            time.sleep(3600)
        ki = ki+1
        continue
    
    #for j in range(len(cs)):
        #cdatas[j].append(cs.values()[j])
    for j in cs:
        if j in cdatas:
            cdatas[j].append(cs[j])
        else:
            cdatas[j] = [cs[j]]
            
    if (looptime-sendtime).total_seconds() >= send_interval:
        sendtime = datetime.datetime.now()
        mes = ''
        #print cdatas
        for b in cdatas:
            cl = cdatas[b]
            if 0 in cl:
                mes3 = '111111111'#'''
            else:
                mes0 = numpy.mean(cl)
                mes1 = numpy.min(cl)
                mes2 = numpy.max(cl)
                mes3 = str(int(mes0))+str(int(mes1))+str(int(mes2))
            mes = mes + mes3

        cdatas.clear()
        print mes
        if transmit == 'ON':
            transdata(mes)
        kp = kp+1
    if kp == sd_num:
        os.system('sudo halt')
    time.sleep(temp_inter)