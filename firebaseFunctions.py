#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:52:53 2017

@author: THK
"""
from firebase import firebase
import json
from random import randint
import numpy as np
import scipy
from plotly.graph_objs import Scatter, Layout

def establish_connection(link):
    fb = firebase.FirebaseApplication(link, None)
    return fb
#accel, gyro, mag are lists(A) of lists(B), B containing tuples of x,y,z data
def format_data(accel, gyro, mag):
    jstr = { 'accel' : {
            'x' : accel[0],
            'y' : accel[1],
            'z' : accel[2]},
            'gyro' : {
            'x' : gyro[0],
            'y' : gyro[1],
            'z' : gyro[2]
                    },
            'mag' : {
            'x' : mag[0],
            'y' : mag[1],
            'z' : mag[2]
                    }
    }
    return json.dumps(jstr)

def generateData():
    a = [(randint(1,4), 0)]
    b = [(randint(1,4), 0)]
    c = [(randint(1,4), 0)]
    for x in range(1,501):
        atemp = a[x-1][0] - (a[x-1][0]*(randint(-20,20)/100))
        btemp = b[x-1][0] - (b[x-1][0]*(randint(-20,20)/100))
        ctemp = c[x-1][0] - (c[x-1][0]*(randint(-20,20)/100))
        a.append((atemp,x))
        b.append((btemp,x))
        c.append((ctemp,x))
    return [a,b,c]

def genFullSet():
    return [generateData(), generateData(), generateData()]

#takes in x,y,z list values
def timeIntegral(arr):
    a= arr
    r = range(0,len(arr))
    na = []
    for x in range(0,len(arr)):
        print(len(a[:x]), len(r[:x]), x)
        apr = scipy.integrate.simps(a[:x], r[:x])
        na.append(apr)
    return na

def integral2(arr, r):
    a= np.array(arr[0])
    b= np.array(arr[1])
    c=np.array(arr[2])
    #r = range(0,len(arr[0]))
    na = []
    nb = []
    nc = []
    for x in range(1,len(arr[0])):
        apr = scipy.integrate.simps(a[:x], r[:x])
        bpr = scipy.integrate.simps(b[:x], r[:x])
        cpr = scipy.integrate.simps(c[:x], r[:x])
        #print(x,apr,bpr,cpr)
        na.append((apr))
        nb.append((bpr))
        nc.append((cpr))
    return [na, nb, nc]
    
def makeScatterJson(arr):
    xVals = []
    yVals = []
    end = len(arr[0])
    for x in range(0,end):
        xVals.append(arr[0][x])
        yVals.append(arr[1][x])
    jstr = { 
            "data" : [Scatter(x=xVals, y=yVals)],
            "layout" : Layout(title=".-^-.")
            }
    return jstr

def makeScatterJson2(arr, var):
    xVals = []
    yVals = []
    end = len(arr[0])
    for x in range(0,end):
        xVals.append(x)
        yVals.append(arr[var][x])
    jstr = { 
            "data" : [Scatter(x=xVals, y=yVals)],
            "layout" : Layout(title=".-^-.")
            }
    return jstr

def makeScatterJsonZ(arr,var):
    xVals = []
    yVals = []
    end = len(arr[0])
    for x in range(0,end):
        xVals.append(arr[var][x])
        yVals.append(arr[2][x])
    jstr = { 
            "data" : [Scatter(x=xVals, y=yVals)],
            "layout" : Layout(title=".-^-.")
            }
    return jstr


def dataSplice(fName):
    f = open(fName,'r+')
    a = []
    for x in f:
        #print(x)
        a.append(x.split(' '))
    return a[9:453]
        
#Takes in the individual shot array, not the array of all shots
def formatDataSet(a):
    accelx = []
    accely = []
    accelz = []
    gyrox = []
    gyroy= []
    gyroz = []
    for x in range(2,len(a)):
        key = sorted(list(a.keys()))[x]
        accelx.append(float(a['sample'+str(x)][key][0]))
        accely.append(float(a['sample'+str(x)][key][1]))
        accelz.append(float(a['sample'+str(x)][key][2]))
        gyrox.append(float(a['sample'+str(x)][key][3]))
        gyroy.append(float(a['sample'+str(x)][key][4]))
        gyroz.append(float(a['sample'+str(x)][key][5]))
    accel = [accelx, accely, accelz]
    gyro = [gyrox, gyroy, gyroz]
    return [accel, gyro]
  
def formatDataSet2(a, sensor):
    accelx = []
    accely = []
    accelz = []
    gyrox = []
    gyroy= []
    gyroz = []
    for x in range(0,len(a)):
        key = sorted(list(a.keys()))[x]
        fromHex = dataFromHex(a[key][sensor])
        accelx.append(float(fromHex[3])*.000244)
        accely.append(float(fromHex[4])*.000244)
        accelz.append(float(fromHex[5])*.000244)
        gyrox.append(float(fromHex[0])*.0175)
        gyroy.append(float(fromHex[1])*.0175)
        gyroz.append(float(fromHex[2])*.0175)
    accel = [accelx, accely, accelz]
    gyro = [gyrox, gyroy, gyroz]
    return [accel, gyro]    

def getTimeArr(a):
    time = []
    offsetKey = sorted(list(a.keys()))[0]
    offset = int(a[offsetKey][4])
    for x in range(0,len(a)):
        key = sorted(list(a.keys()))[x]
        newTime = int(a[key][4]) - offset
        secTime = newTime*pow(10,-6)
        time.append(secTime)
    return time

def dataFromHex(a):
    #imu_string = "530030001700520017ff780f"
    imu_string = a
    imu_reading = {}
    for i in range(0, 24, 4):
        lower_byte = int(imu_string[i:i+2], 16) # get first two hex values and convert to base 10
        upper_byte = int(imu_string[i+2:i+4], 16) # get next two hex values and convert to base 10
        value = (upper_byte << 8) + lower_byte # shift left 8 and add lower byte
        if (value > pow(2, 15)): 
            value = value - pow(2, 16) # unsigned to signed conversion
        imu_reading[i/4] = value # store in list
    return imu_reading    



