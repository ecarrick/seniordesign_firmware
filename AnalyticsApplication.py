#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:05:47 2017

@author: THK
"""

import pygame
import firebaseFunctions as fbtf
from tkinter import *
import tkinter.filedialog as fd
import SE3
filename= 'FastPickup.txt'
global screen
global clock
global link
global shotArr
global saveArr
global simStop

class App:
        def __init__(self, master):
            frame = Frame(master)
            frame.pack()
            self.label_txt = StringVar()
            self.save_txt = StringVar()
            self.saveList = StringVar()
            self.shotList = StringVar()
            self.spacing = StringVar()
            self.allShots = StringVar()
            self.button2 = Button(frame, 
                                  text="Pull Data", 
                                  command=self.dHHandler).pack(fill=X)
            self.allShotEntry = Entry(frame, textvariable=self.allShots).pack(fill=X)
            self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=quit)
            self.button.pack(fill=X)
            self.slogan = Button(frame,
                         text="Simulate",
                         command=self.simulate)
            self.slogan.pack(fill=X)
            self.saveButton = Button(frame,
                             text="Save",
                             command=self.save).pack(fill=X)
            self.shotLabel = Label(frame, text="Pick Shot").pack(fill=X)
            self.entryArea = Entry(frame, textvariable=self.label_txt).pack(fill=X)
            self.saveLabel = Label(frame, text="Pick Save").pack(fill=X)
            self.saveArea = Entry(frame, textvariable=self.save_txt).pack(fill=X)
            self.msgBox = Message(frame, textvariable = self.shotList).pack(fill=X, side=LEFT)
            self.msgBox3 = Message(frame, textvariable = self.spacing).pack(fill=X, side=LEFT)
            self.msgBox2 = Message(frame, textvariable = self.saveList).pack(fill=X, side=RIGHT)
            
        
        def simulate(self):
            text = self.label_txt.get()
            text2 = self.save_txt.get()
            print(text)
            print(text2)
            #text = self.entryArea.get()
            if(text != ""):
                pygame_start(text, text2, 0)
        
        def save(self):
            text = self.label_txt.get()
            print("Now saving " + text)
            if(text != ""):
                saveShot(text)
           
        
        def dHHandler(self):
            a = dataHandle(self.allShots.get())
            self.spacing.set("")
            strShot = "Shots: "
            strSave = "Saves: "
            b = list(a[0].keys())
            c = list(a[1].keys())
            for d in range(0, len(a[0].keys())):
                strShot += "\n " + b[d]
                if(len(b) > len(c)):
                    self.spacing.set(self.spacing.get() + "|\n")
            for z in range(0, len(a[1].keys())):
                strSave += "\n " + c[z]
                if(len(b) < len(c)):
                    self.spacing.set(self.spacing.get() + "|\n")
            self.shotList.set(strShot)
            self.saveList.set(strSave)
            

def openFile():
    global filename
    filename = fd.askopenfilename()
    if filename is None:
        filename = 'FastPickup.txt'
    print(filename)

def dataHandle(saveArea):
    global shotArr
    global saveArr
    if saveArea == "":
        saveArea = "DataSession28"
    #link = input("Firebase link: ")
    fb = fbtf.establish_connection('https://shotanalytics-17fc3.firebaseio.com/')
    shotArr = fb.get(saveArea,None)
    saveArr = fb.get("/SavedShots", None)
    print("This ran")
    return [shotArr, saveArr]
    #print("Choose key from list: " + str(shotArr.keys()))
    
def saveShot(t):
    global saveArr
    dataHandle()
    fb = fbtf.establish_connection('https://shotanalytics-17fc3.firebaseio.com/')
    toUpload = shotArr[t]
    fb.post('/SavedShots', toUpload)
    saveArr = fb.get("/SavedShots", None)

def init_pygame():
    pygame.init()
    global screen
    global clock
    size= (900,600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Test")
    clock = pygame.time.Clock()
    
def get_doubleIntegral_array(data, sensor, typeToGraph):
    formdata = fbtf.formatDataSet2(data, sensor)
    time = fbtf.getTimeArr(data)
    pos = SE3.run(formdata, time)
    pos2 = refactorArray(pos)
    maxVals = SE3.metrics2(pos, time, pos2)
    return [pos2, maxVals]
    
def pygame_draw(arr, screen, axis, ind, color, maxMax, offset):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                done = True
    
    max0 = maxMax
    max2 = (max(arr[2])-min(arr[2]))
    if(max0 == 0 ):
        if(max(arr[0]) == 0):
            max0=500000000
            #print("this is max0:" + str(max0))
    if(max2 ==0):
        if(max(arr[2]) ==0):
            max2=500000000
            #print("this is max2:" + str(max0))
    xVal = (((arr[axis][ind]+offset)/max0)*300)+300
    yVal = (((arr[2][ind])/max2)*-300)+300
    xValInt = int(xVal.astype(int))
    yValInt = int(yVal.astype(int))
    #print(str(xValInt)+" | " + str(yValInt)+" | " + str(xVal)+" | " + 
     #     str(yVal)+" | " + str(max(arr[0]))+" | " + str(arr[axis][ind]))
    if(max0 == 0):
        xVal=300
    if(max2 ==0):
        yVal=300
    pygame.draw.circle(screen, color, (xValInt, yValInt), 10)
    return [xValInt, yValInt, arr[axis][ind]*100, arr[2][ind]*100]
    #xOld = xVal
    #yOld = yVal  

def calcDistance(x1, y1, x2, y2):
    val = pow((pow((x1-x2),2) + pow((y1-y2),2)), .5)
    return val
#orien controls what axis is graphed with the Z axis
def pygame_start(t, s, orien):
    global simStop
    print(t, s)
    init_pygame()
    BLACK = (0,0,0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0 )
    GREEN = (0, 255, 0) 
    BLUE = (0,0,255)
    trueMaxSaves = []
    font = pygame.font.SysFont('Calabria', 20,True, False)
    global pos
    [pos, maxA1] = get_doubleIntegral_array(shotArr[t], 0, 3)
    [pos1, maxA2] = get_doubleIntegral_array(shotArr[t], 1, 3)
    [pos2, maxA3] = get_doubleIntegral_array(shotArr[t], 2, 3)
    [pos3, maxA4] = get_doubleIntegral_array(shotArr[t], 3, 3)
    x=0
    savePlot = (s!= "")
    minVal = min(len(pos[0]),len(pos1[0]),len(pos2[0]),len(pos3[0]))
    if(savePlot):
        print("Keys: " + str(saveArr.keys()))
        [Spos, smaxA1] = get_doubleIntegral_array(saveArr[s], 0, 3)
        [Spos1, smaxA2] = get_doubleIntegral_array(saveArr[s], 1, 3)
        [Spos2, smaxA3] = get_doubleIntegral_array(saveArr[s], 2, 3)
        [Spos3, smaxA4] = get_doubleIntegral_array(saveArr[s], 3, 3)
        minVal = min(len(Spos[0]),len(Spos1[0]),len(Spos2[0]),
                     len(Spos3[0]), minVal)
        trueMaxSaves = trueMax(smaxA1, smaxA2, smaxA3, smaxA4)
    distArr = []
    trueMaxVals= trueMax(maxA1, maxA2, maxA3, maxA4)
    while x<minVal:
        screen.fill(WHITE)
        max0 = max(pos[orien])-min(pos[orien])+.20
        max1 = max(pos1[orien])-min(pos1[orien])+.10
        max2 = max(pos2[orien])-min(pos2[orien])
        max3 = max(pos3[orien])-min(pos3[orien])-.10
        maxMax = max([max0, max1, max2, max3])
        pygame.draw.line(screen, BLACK, [0,300],[600,300], 5)
        pygame.draw.line(screen, BLACK, [300,0],[300,600], 5)
        pygame.draw.line(screen, BLACK, [601,0], [601,600], 5)
        pygame.draw.line(screen, BLACK, [300,200], [305,200], 5)
        pygame.draw.line(screen, BLACK, [300,100], [305,100], 5)
        pygame.draw.line(screen, BLACK, [300,400], [305,400], 5)
        pygame.draw.line(screen, BLACK, [300,500], [305,500], 5)
        pygame.draw.line(screen, BLACK, [100,300], [100,305], 5)
        pygame.draw.line(screen, BLACK, [200,300], [200,305], 5)
        pygame.draw.line(screen, BLACK, [400,300], [400,305], 5)
        pygame.draw.line(screen, BLACK, [500,300], [500,305], 5)
        text1 = font.render(str(round((maxMax/3)*100)), True, BLACK)
        screen.blit(text1, [400, 290])
        text2 = font.render("cm/s", True, BLACK)
        screen.blit(text2, [570, 310])
        ball1 = pygame_draw(pos, screen, orien, x, RED, maxMax, .20)
        ball2 = pygame_draw(pos1, screen, orien, x, RED, maxMax, .10)
        ball3 = pygame_draw(pos2, screen, orien, x, RED, maxMax, 0)
        ball4 = pygame_draw(pos3, screen, orien, x, RED, maxMax, -0.10)
        if(savePlot):
            smax0 = max(Spos[orien])-min(Spos[orien])+.20
            smax1 = max(Spos1[orien])-min(Spos1[orien])+.10
            smax2 = max(Spos2[orien])-min(Spos2[orien])
            smax3 = max(Spos3[orien])-min(Spos3[orien])-.10
            smaxMax = max([smax0, smax1, smax2, smax3])
            sball1 = pygame_draw(Spos, screen, orien, x, BLUE, smaxMax, .20)
            sball2 = pygame_draw(Spos1, screen, orien, x, BLUE, smaxMax, .10)
            sball3 = pygame_draw(Spos2, screen, orien, x, BLUE, smaxMax, 0)
            sball4 = pygame_draw(Spos3, screen, orien, x, BLUE, smaxMax, -0.10)            
        drawText(screen, ball1, ball2, ball3, ball4, trueMaxVals, trueMaxSaves, 0)
        pygame.display.flip()
        clock.tick(30)
        x+=1
    if simStop:
        pygame.display.quit()
        pygame.quit()

    
def initialize():
    global root
    global simStop
    simStop = False
    root = Tk()
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="file", menu=filemenu)
    filemenu.add_command(label="simStop Toggle", command=toggleStop)
    filemenu.add_command(label="Quit", command=root.quit)
    filemenu.add_command(label="PullData", command=dataHandle)
    app = App(root)
#    e1 = Entry(root)
#    Label(root, text="which shot?").grid(row=1, column=0)
#    e1.grid(row=1, column=1)
    root.mainloop()

def toggleStop():
    global simStop
    simStop = not simStop
    
#converts to 2 digits
def dc(d):
    before_dec, after_dec = str(d).split('.')
    a = float('.'.join((before_dec, after_dec[0:2])))
    return a

def refactorArray(a):
    x = []
    y = []
    z = []
    for i in range(0,len(a[3][3])):
        x.append(a[3][3][i][0])
        y.append(a[3][3][i][1])
        z.append(a[3][3][i][2])
    return [x, y, z]

def trueMax(a, b, c, d):
    output = []
    for i in range(0, len(a)-1):
        for j in range(0,3):
            temp = [a[i][j], b[i][j], c[i][j], d[i][j]]
            if(i % 2 == 0):
                output.append(max(temp))
            else:
                output.append(min(temp))
    return output

def drawText(screen, ball1, ball2, ball3, ball4, trueMaxVals, trueMaxSaves, side):
    BLACK = (0,0,0)
    txt = "shot"
    offset = 0
    save0 = ""
    save1 = ""
    save2 = ""
    save3 = ""
    save4 = ""
    save5 = ""
    save6 = ""
    save7 = ""
    save8 = ""
    save9 = ""
    save10 = ""
    save11 = ""
    save12 = ""
    save13 = ""
    save14 = ""
    save15 = ""
    save16 = ""
    save17 = ""
    font = pygame.font.SysFont('Calabria', 18,True, False)
    text1 = font.render("1", True, BLACK)
    screen.blit(text1, [ball1[0], ball1[1]])
    text2 = font.render("2", True, BLACK)
    screen.blit(text2, [ball2[0], ball2[1]])
    text3 = font.render("3", True, BLACK)
    screen.blit(text3, [ball3[0], ball3[1]])
    text4 = font.render("4", True, BLACK)
    screen.blit(text4, [ball4[0], ball4[1]])
    if len(trueMaxSaves) > 0:
        save0 = " compare to " + str(dc(trueMaxSaves[0]))
        save1 = " compare to " + str(dc(trueMaxSaves[1]))
        save2 = " compare to " + str(dc(trueMaxSaves[2]))
        save3 = " compare to " + str(dc(trueMaxSaves[3]))
        save4 = " compare to " + str(dc(trueMaxSaves[4]))
        save5 = " compare to " + str(dc(trueMaxSaves[5]))
        save6 = " compare to " + str(dc(trueMaxSaves[6]))
        save7 = " compare to " + str(dc(trueMaxSaves[7]))
        save8 = " compare to " + str(dc(trueMaxSaves[8]))
        save9 = " compare to " + str(dc(trueMaxSaves[9]))
        save10 = " compare to " + str(dc(trueMaxSaves[10]))
        save11 = " compare to " + str(dc(trueMaxSaves[11]))
        save12 = " compare to " + str(dc(trueMaxSaves[12]))
        save13 = " compare to " + str(dc(trueMaxSaves[13]))
        save14 = " compare to " + str(dc(trueMaxSaves[14]))
        save15 = " compare to " + str(dc(trueMaxSaves[15]))
        save16 = " compare to " + str(dc(trueMaxSaves[16]))
        save17 = " compare to " + str(dc(trueMaxSaves[17]))
    text5 = font.render("Max " + txt + " X accel: " + str(dc(trueMaxVals[0]))+save0,
                        True,
                        BLACK)
    screen.blit(text5, [620+offset, 20])
    text6 = font.render("Min " + txt + " X accel: " + str(dc(trueMaxVals[3]))+save3, True,
                        BLACK)
    screen.blit(text6, [620+offset, 40])
    text5 = font.render("Max " + txt + " X Vel: " + str(dc(trueMaxVals[1]))+save1, True,
                        BLACK)
    screen.blit(text5, [620+offset, 60])
    text6 = font.render("Min " + txt + " X Vel: " + str(dc(trueMaxVals[4]))+save4, True,
                        BLACK)
    screen.blit(text6, [620+offset, 80])
    text5 = font.render("Max " + txt + " X gyro: " + str(dc(trueMaxVals[2]))+save2, True,
                        BLACK)
    screen.blit(text5, [620+offset, 100])
    text7 = font.render("Min " + txt + " X gyro: " + str(dc(trueMaxVals[5]))+save5, True,
                        BLACK)
    screen.blit(text7, [620+offset, 120])
    text5 = font.render("Max " + txt + " Y accel: " + str(dc(trueMaxVals[6]))+save6, True,
                        BLACK)
    screen.blit(text5, [620+offset, 140])
    text6 = font.render("Min " + txt + " Y accel: " + str(dc(trueMaxVals[9]))+save9, True,
                        BLACK)
    screen.blit(text6, [620+offset, 160])
    text5 = font.render("Max " + txt + " Y Vel: " + str(dc(trueMaxVals[7]))+save7, True,
                        BLACK)
    screen.blit(text5, [620+offset, 180])
    text6 = font.render("Min " + txt + " Y Vel: " + str(dc(trueMaxVals[10]))+save10, True,
                        BLACK)
    screen.blit(text6, [620+offset, 200])
    text5 = font.render("Max " + txt + " Y gyro: " + str(dc(trueMaxVals[8]))+save8, True,
                        BLACK)
    screen.blit(text5, [620+offset, 220])
    text7 = font.render("Min " + txt + " Y gyro: " + str(dc(trueMaxVals[11]))+save11, True,
                        BLACK)
    screen.blit(text7, [620+offset, 240])
    text5 = font.render("Max " + txt + " Z accel: " + str(dc(trueMaxVals[12]))+save12, True,
                        BLACK)
    screen.blit(text5, [620+offset, 260])
    text6 = font.render("Min " + txt + " Z accel: " + str(dc(trueMaxVals[15]))+save15, True,
                        BLACK)
    screen.blit(text6, [620+offset, 280])
    text5 = font.render("Max " + txt + " Z Vel: " + str(dc(trueMaxVals[13]))+save13, True,
                        BLACK)
    screen.blit(text5, [620+offset, 300])
    text6 = font.render("Min " + txt + " Z Vel: " + str(dc(trueMaxVals[16]))+save16, True,
                        BLACK)
    screen.blit(text6, [620+offset, 320])
    text5 = font.render("Max " + txt + " Z gyro: " + str(dc(trueMaxVals[14]))+save14, True,
                        BLACK)
    screen.blit(text5, [620+offset, 340])
    text7 = font.render("Min " + txt + " Z gyro: " + str(dc(trueMaxVals[17]))+save17, True,
                        BLACK)
    screen.blit(text7, [620+offset, 360])

initialize()
    
    

