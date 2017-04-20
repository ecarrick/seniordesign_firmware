import numpy as np
import math

Reye = [[1,0,0],[0,1,0],[0,0,1]]
dzero = [[0],[0],[0]]

def SE3(d, R):
    g = [[R, d] , [0,0,0,1]]
    return g
    
def getPos(g):
    p = [g[:3, 3]]
    return p
    
def getRot(g):
    R = [g[:3, :3]]
    return R
    
def Rx(ang):
    R = [[1,0,0],[0, math.cos(ang), -math.sin(ang)],[0, math.sin(ang), math.cos(ang)]]
    return R

def Ry(ang):
    R = [[math.cos(ang), 0, math.sin(ang)],[0,1,0],[-math.sin(ang), 0, math.cos(ang)]]
    return R

def Rz(ang):
    R = [[math.cos(ang), -math.sin(ang), 0],[math.sin(ang), math.cos(ang), 0],[0,0,1]]
    return R
    
def Rmat(xang, yang, zang):
    R = Rx(xang).dot(Ry.yang).dot(Rz.zang)
    return R
    
def gravFix(gCurr):
    grav = [[0],[0],[-1]]
    ggrav = SE3(grav, Reye)
    R = getRot(gCurr)
    gR = SE3(dzero, R)
    newggrav = ggrav.dot(gR)
    newgrav = getpos(newggrav)
    return newgrav
    
def update(g, accel, gyro, vel, theta, tstep):
    a = gravFix(g)
    accel = accel-a
    d = tstep*(vel + .5*accel*tstep)
    thetastep = gyro*tstep
    gupdate = SE3(d, Rmat(thetastep[0],thetastep[1],thetastep[2]))
    gnew = g.dot(gupdate)
    vnew = vel + accel*tstep
    thetanew = theta + thetastep
    return [gnew, vnew, thetanew]
    
def filter(accel, gyro):
    ax[0] = accel[0,0]
    ay[0] = accel[1,0]
    az[0] = accel[2,0]
    gx[0] = gyro[0,0]
    gy[0] = gyro[1,0]
    gz[0] = gyro[2,0]
    
    for x in range(1,len(accel[0]))
        ax[x] = .75 * ax[x-1] + .25 * accel[0,x]
        ay[x] = .75 * ay[x-1] + .25 * accel[1,x]
        az[x] = .75 * az[x-1] + .25 * accel[2,x]
        gx[x] = .75 * gx[x-1] + .25 * gyro[0,x]
        gy[x] = .75 * gy[x-1] + .25 * gyro[1,x]
        gz[x] = .75 * gz[x-1] + .25 * gyro[2,x]
    aout = [ax, ay, az]
    gout = [gx, gy, gz]
    return [aout, gout]
    
def process(
    
    
    
    
    
    
