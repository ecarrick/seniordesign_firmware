import numpy as np
import math

Reye = np.array([[1,0,0],[0,1,0],[0,0,1]])
dzero = np.array([[0],[0],[0]])

def SE3(d, R):
    g = np.array([[R, d] , [0,0,0,1]])
    return g
    
def getPos(g):
    p = np.array([g[:3, 3]])
    return p
    
def getRot(g):
    R = np.array([g[:3, :3]])
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
    R = Rx(xang).dot(Ry.yang).dot(Rz.zang)
    return R
    
def gravFix(gCurr):
    grav = np.array([[0],[0],[-1]])
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
    
def filt(accel, gyro):
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
    
def process(accel, gyro, time)
	start = 0
	[ac, gy] = filt(accel, gyro)
	for x in range(0, len(a[0])
		if start == 0 
			bool1 = ac[0,x] > -.1 && ac[0,x] < .1
			bool2 = ac[1,x] > -.1 && ac[1,x] < .1
			bool3 = ac[2,x] > -1.1 && ac[2,x] < -.9
			if bool1 && bool2 && bool3
				start = 1
				i = 0
				g[0] = SE3(dzero, Reye)
				v[0] = np.array([[0],[0],[0]])
				theta[0] = np.array([[0],[0],[0]])
				pos[0] = getPos(g[0])
		else
			i = i + 1
			[g[i], v[i], theta[i]] = update(gcurr, ac[:3, x], gy[:3, x], v, theta, time[x])
			pos[i] = getPos(g[i])
	return [g, pos, v, theta]
	
    
    
    
    
    
    
