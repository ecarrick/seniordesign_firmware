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
filename= 'FastPickup.txt'
global screen
global clock
global link
global shotArr
global saveArr

class App:
        def __init__(self, master):
            frame = Frame(master)
            frame.pack()
            self.label_txt = StringVar()
            self.save_txt = StringVar()
            self.saveList = StringVar()
            self.shotList = StringVar()
            self.spacing = StringVar()
            self.button2 = Button(frame, 
                                  text="Pull Data", 
                                  command=self.dHHandler).pack(fill=X)
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
            print(self.label_txt.get())
            #text = self.entryArea.get()
            if(text != ""):
                pygame_start(text)
        
        def save(self):
            text = self.label_txt.get()
            print("Now saving " + text)
            if(text != ""):
                saveShot(text)
        
        def dHHandler(self):
            a = dataHandle()
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

def dataHandle():
    global shotArr
    global saveArr
    #link = input("Firebase link: ")
    fb = fbtf.establish_connection('https://shotanalytics-17fc3.firebaseio.com/')
    shotArr = fb.get("/DataSession29",None)
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
    size= (600,600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Test")
    clock = pygame.time.Clock()
    
def get_doubleIntegral_array(data, sensor):
    formdata = fbtf.formatDataSet2(data, sensor)
    time = fbtf.getTimeArr(data)
    accel = formdata[0]
    vel = fbtf.integral2(accel, time)
    pos = fbtf.integral2(vel, time[:len(time)-1])
    return pos
    
def pygame_draw(arr, screen, axis, ind, color, maxMax):
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
    xVal = (((arr[axis][ind])/max0)*300)+300
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

def pygame_start(t):
    init_pygame()
    BLACK = (0,0,0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0 )
    GREEN = (0, 255, 0) 
    BLUE = (0,0,255)
    font = pygame.font.SysFont('Calabria', 20,True, False)
    global pos
    pos = get_doubleIntegral_array(shotArr[t], 0)
    x=0
    distArr = []
    while x<len(pos[0]):
        screen.fill(WHITE)
        maxX= max(pos[0])-min(pos[0])
        maxY = max(pos[1])-min(pos[1])
        maxMax = max([maxX, maxY])
        pygame.draw.line(screen, BLACK, [0,300],[600,300], 5)
        pygame.draw.line(screen, BLACK, [300,0],[300,600], 5)
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
        text2 = font.render("cm", True, BLACK)
        screen.blit(text2, [570, 310])
        ball1 = pygame_draw(pos, screen, 0, x, RED, maxMax)
        ball2 = pygame_draw(pos, screen, 1, x, BLUE, maxMax)
        text3 = font.render(str(round(ball1[2])) + ", " + str(round(ball1[3])), True, RED)
        screen.blit(text3, [ball1[0], ball1[1]+15])
        text4 = font.render(str(round(ball2[2])) + ", " + str(round(ball2[3])), True, RED)
        screen.blit(text4, [ball2[0], ball2[1]-15])
        dist = calcDistance(ball1[2], ball1[3], ball2[2], ball2[3])
        distArr.append(dist)
        text5 = font.render("Current Seperation: " + str(round(dist)), True, BLACK)
        screen.blit(text5, [320, 500])
        text6 = font.render("Max Seperation: " + str(round(max(distArr))), True, BLACK)
        screen.blit(text6, [320, 520])
        pygame.display.flip()
        clock.tick(30)
        x+=1
    pygame.display.quit()
    pygame.quit()

    
def initialize():
    global root
    root = Tk()
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="file", menu=filemenu)
    filemenu.add_command(label="Open", command=openFile)
    filemenu.add_command(label="Quit", command=root.quit)
    filemenu.add_command(label="PullData", command=dataHandle)
    app = App(root)
#    e1 = Entry(root)
#    Label(root, text="which shot?").grid(row=1, column=0)
#    e1.grid(row=1, column=1)
    root.mainloop()



initialize()
    
    

