import numpy as np
import math

Reye = np.array([[1,0,0],[0,1,0],[0,0,1]])
dzero = [0,0,0]

def SE3(d, R):
    l1 = [R[0,0], R[0,1], R[0,2], d[0]]
    l2 = [R[1,0], R[1,1], R[1,2], d[1]]
    l3 = [R[2,0], R[2,1], R[2,2], d[2]]
    g = np.array([l1, l2, l3, [0,0,0,1]])
    return g
    
def getPos(g):
    p = [g[0,3],g[1,3],g[2,3]]
    return p
    
def getRot(g):
    R = np.array(g[:3, :3])
    return R
    
def Rx(ang):
    R = np.array([[1,0,0],[0, math.cos(ang), -math.sin(ang)],[0, math.sin(ang), math.cos(ang)]])
    return R

def Ry(ang):
    R = np.array([[math.cos(ang), 0, math.sin(ang)],[0,1,0],[-math.sin(ang), 0, math.cos(ang)]])
    return R

def Rz(ang):
    R = np.array([[math.cos(ang), -math.sin(ang), 0],[math.sin(ang), math.cos(ang), 0],[0,0,1]])
    return R
    
def Rmat(xang, yang, zang):
    R = Rx(xang).dot(Ry(yang)).dot(Rz(zang))
    return R
    
def gravFix(gCurr):
    grav = [0,0,.95]
    ggrav = SE3(grav, Reye)
    R = getRot(gCurr)
    gR = SE3(dzero, R)
    newggrav = gR.dot(ggrav)
    newgrav = getPos(newggrav)
    return newgrav
    
def update(g, accel, gyro, vel, theta, tstep):
    a = gravFix(g)
    accel = 9.8*(accel-a)
    d = tstep*(vel + .5*accel*tstep)
    thetastep = gyro*tstep
    gupdate = SE3(d, Rmat(math.radians(thetastep[0]),math.radians(thetastep[1]),math.radians(thetastep[2])))
    gnew = g.dot(gupdate)
    vnew = vel + accel*tstep
    thetanew = [theta[0] + thetastep[0],theta[1] + thetastep[1],theta[2] + thetastep[2]]
    return [gnew, vnew, thetanew]
    
def filt(accel, gyro):
    ax = [accel[0,0]]
    ay = [accel[1,0]]
    az = [accel[2,0]]
    gx = [gyro[0,0]]
    gy = [gyro[1,0]]
    gz = [gyro[2,0]]
    
    for x in range(1,len(accel[0])):
        ax.append(.7 * ax[x-1] + .3 * accel[0,x])
        ay.append(.7 * ay[x-1] + .3 * accel[1,x])
        az.append(.7 * az[x-1] + .3 * accel[2,x])
        gx.append(.7 * gx[x-1] + .3 * gyro[0,x])
        gy.append(.7 * gy[x-1] + .3 * gyro[1,x])
        gz.append(.7 * gz[x-1] + .3 * gyro[2,x])
    aout = np.array([ax, ay, az])
    gout = np.array([gx, gy, gz])
    return [aout, gout]
    
def process(accel, gyro, time):
    start = 0
    [ac, gy] = filt(accel, gyro)
    g = SE3(dzero, Reye)
    pos = [getPos(g)]
    v = np.array([0,0,0])
    theta = [[0,0,0]]
    for x in range(0, len(ac[0])):
        i = 0
        if start == 0:
            bool1 = (ac[0,x] > -.1 and ac[0,x] < .1)
            bool2 = (ac[1,x] > -.1 and ac[1,x] < .1)
            bool3 = (ac[2,x] > -1.1 and ac[2,x] < -.9)
            if x==1 or (bool1 and bool2 and bool3):
                start = 1
        else:
            t = time[x]-time[x-1]
            temp = update(g, ac[:3, x], gy[:3, x], v, theta[i], t)
            g = temp[0]
            v = temp[1]
            theta.append(temp[2])
            pos.append(getPos(g))            
            i = i + 1
    return [pos, theta]


    
    
    
    
    
