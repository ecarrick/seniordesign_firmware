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
def integral(arr):
    a= np.array(arr[0])
    b= np.array(arr[1])
    c=np.array(arr[2])
    r = range(0,len(arr[0]))
    na = []
    nb = []
    nc = []
    for x in range(1,len(arr[0])):
        print(len(a[:x]), len(r[:x]), x)
        apr = scipy.integrate.simps(a[:x], r[:x])
        bpr = scipy.integrate.simps(b[:x], r[:x])
        cpr = scipy.integrate.simps(c[:x], r[:x])
        #print(x,apr,bpr,cpr)
        na.append((apr, x))
        nb.append((bpr, x))
        nc.append((cpr, x))
    return [na, nb, nc]

def integral2(arr):
    a= np.array(arr[0])
    b= np.array(arr[1])
    c=np.array(arr[2])
    r = range(0,len(arr[0]))
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
        
def formatDataSet(a):
    magx = []
    magy = []
    magz = []
    accelx = []
    accely = []
    accelz = []
    gyrox = []
    gyroy= []
    gyroz = []
    for x in range(0,len(a)):
        magx.append(float(a[x][1]))
        magy.append(float(a[x][2]))
        magz.append(float(a[x][3]))
        accelx.append(float(a[x][4]))
        accely.append(float(a[x][5]))
        accelz.append(float(a[x][6]))
        gyrox.append(float(a[x][7]))
        gyroy.append(float(a[x][8]))
        gyroz.append(float(a[x][9]))
    mag = [magx, magy, magz]
    accel = [accelx, accely, accelz]
    gyro = [gyrox, gyroy, gyroz]
    return [accel, gyro, mag]
    

    



