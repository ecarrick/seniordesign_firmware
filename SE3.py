import numpy as np
import math
import matplotlib.pyplot as plt
import AnalyticsApplication as aa

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
    grav = [0,0,1]
    ggrav = SE3(grav, Reye)
    R = getRot(gCurr)
    gR = SE3(dzero, R)
    newggrav = gR.dot(ggrav)
    newgrav = getPos(newggrav)
    return newgrav
    
def update(g, accel, gyro, vel, theta, tstep, gbias):
    a = gravFix(g)
    accel = 9.8*(accel-a)
    gyro = gyro - gbias
    d = tstep*(vel + .5*accel*tstep)
    thetastep = gyro*tstep
    gupdate = SE3(d, Rmat(math.radians(thetastep[0]),math.radians(thetastep[1]),math.radians(thetastep[2])))
    gnew = g.dot(gupdate)
    vnew = d/tstep
    thetanew = [theta[0]+thetastep[0],theta[1]+thetastep[1],theta[2]+thetastep[2]]
    return [gnew, vnew, thetanew]
    
def filt(accel, gyro, gain):
    ax = [accel[0,0]]
    ay = [accel[1,0]]
    az = [accel[2,0]]
    gx = [gyro[0,0]]
    gy = [gyro[1,0]]
    gz = [gyro[2,0]]
    a = gain
    b = (1-gain)
    for x in range(1,len(accel[0])):
        ax.append(a * ax[x-1] + b * accel[0,x])
        ay.append(a * ay[x-1] + b * accel[1,x])
        az.append(a * az[x-1] + b * accel[2,x])
        gx.append(a * gx[x-1] + b * gyro[0,x])
        gy.append(a * gy[x-1] + b * gyro[1,x])
        gz.append(a * gz[x-1] + b * gyro[2,x])
    aout = np.array([ax, ay, az])
    gout = np.array([gx, gy, gz])
    return [aout, gout]
    
def process(accel, gyro, time, d):
    start = 0
    [ac, gy] = filt(accel, gyro,.9)
 #   [ac, gy] = [accel, gyro]
    g = SE3(d, Reye)
    pos = [getPos(g)]
    v = np.array([0,0,0])
    theta = [[0,0,0]]
    gbias = [0,0,0]
    xa = []
    ya = []
    za = []
    vel = []
    for x in range(0, len(ac[0])):
        if start == 0:
            bool1 = (ac[0,x] > -.1 and ac[0,x] < .1)
            bool2 = (ac[1,x] > -.1 and ac[1,x] < .1)
            bool3 = (ac[2,x] < 1.1 and ac[2,x] > .9)
            if x == 1 or (bool1 and bool2 and bool3):
                start = 1
                gbias = [gy[0,x],gy[1,x],gy[2,x]]
                g = SE3(d,Rmat(math.atan2(ac[1,x],ac[2,x]),math.atan2(ac[0,x],math.sqrt(ac[2,x]*ac[2,x]+ac[1,x]*ac[1,x])),0))
                print(g)
                print(gravFix(g))
        else:
            t = time[x]-time[x-1]
            if t<.05:
                temp = update(g, ac[:3, x], gy[:3, x], v, theta[-1], t, gbias)
            g = temp[0]
            v = temp[1]
            theta.append(temp[2])
            pos.append(getPos(g))
            vel.append([v[0],v[1],v[2]])
            xa.append(getPos(g)[0])
            ya.append(getPos(g)[1])
            za.append(getPos(g)[2])
    return [pos, theta, [xa,ya,za], vel]

def run(num, sensor, l):
    a = aa.dataHandle()
    b = aa.fbtf.formatDataSet2(a[0]['shot'+num],sensor)
    d = filt(b[0],b[1],.9)
    t = aa.fbtf.getTimeArr(a[0]['shot'+num])
    c = process(b[0],b[1],t,[0,l,0])
    return [b,d[0],d[1],t,c]

def plot(result):
    plt.figure(1)
    plt.plot(result[0][0][0])
    plt.plot(result[0][0][1])
    plt.plot(result[0][0][2])
    plt.plot(result[1][0])
    plt.plot(result[1][1])
    plt.plot(result[1][2])
    plt.legend(['x','y','z'])
    plt.title('Filtered Acceleration')
    plt.figure(2)
    plt.plot(result[0][1][0])
    plt.plot(result[0][1][1])
    plt.plot(result[0][1][2])
    plt.plot(result[2][0])
    plt.plot(result[2][1])
    plt.plot(result[2][2])
    plt.legend(['x','y','z'])
    plt.title('Filtered Gyroscope')
    plt.figure(3)
    plt.plot(result[4][0][0:35])
    plt.legend(['x','y','z'])
    plt.title('Position')
    plt.figure(4)
    plt.plot(result[4][1])
    plt.legend(['x','y','z'])
    plt.title('Angle')
    plt.figure(5)
#    plt.plot(result[4][2][0], result[4][2][2])
    plt.plot(result[1][0], result[1][2])
    plt.title('X vs Z')
    plt.figure(6)
#    plt.plot(result[4][2][1],result[4][2][2])
    plt.plot(result[1][1], result[1][2])
    plt.title('Y vs Z')
    plt.figure(7)
    plt.plot(result[3])
    plt.title('Time')
    return result[4]

def metrics():
    result = [run('0',0,0),run('0',1,0),run('0',2,0),run('0',3,0)]
    xa = []
    ya = []
    za = []
    xg = []
    yg = []
    zg = []
    xv = []
    yv = []
    zv = []
    xmax = []
    xmin = []
    ymax = []
    ymin = []
    zmax = []
    zmin = []
    for i in range(0,4):
        xa.append(result[i][1][0])
        ya.append(result[i][1][1])
        za.append(result[i][1][2])
        xg.append(result[i][2][0])
        yg.append(result[i][2][1])
        zg.append(result[i][2][2])
        xv.append(result[i][4][3][0])
        yv.append(result[i][4][3][1])
        zv.append(result[i][4][3][2])
        xmax.append([np.argmax(xa[i]),np.amax(xv[i]),np.amax(xg[i])])
        ymax.append([np.amax(ya[i]),np.amax(yv[i]),np.amax(yg[i])])
        zmax.append([np.amax(za[i]),np.amax(zv[i]),np.amax(zg[i])])
        xmin.append([np.amin(xa[i]),np.amin(xv[i]),np.amin(xg[i])])
        ymin.append([np.amin(ya[i]),np.amin(yv[i]),np.amin(yg[i])])
        zmin.append([np.amin(za[i]),np.amin(zv[i]),np.amin(zg[i])])
    return [xmax, xmin, ymax, ymin, zmax, zmin]
        
    
    
    

    
    
    
    
