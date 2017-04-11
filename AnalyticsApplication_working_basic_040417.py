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

class App:
        def __init__(self, master):
            frame = Frame(master)
            frame.pack()
            self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=quit)
            self.button.pack(side=LEFT)
            self.slogan = Button(frame,
                         text="Simulate",
                         command=pygame_start)
            self.slogan.pack(side=LEFT)

def openFile():
    global filename
    filename = fd.askopenfilename()
    if filename is None:
        filename = 'FastPickup.txt'
    print(filename)

def dataHandle():
    global shotArr
    #link = input("Firebase link: ")
    fb = fbtf.establish_connection('https://shotanalytics-17fc3.firebaseio.com/')
    shotArr = fb.get("/testdata",None)
    print("Choose key from list: " + str(shotArr.keys()))
    
    

def init_pygame():
    pygame.init()
    global screen
    global clock
    size= (600,600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Test")
    clock = pygame.time.Clock()
    
def get_doubleIntegral_array(data):
    formdata = fbtf.formatDataSet(data)
    accel = formdata[0]
    vel = fbtf.integral2(accel)
    pos = fbtf.integral2(vel)
    return pos
    
def pygame_draw(arr, screen, axis, ind, color):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                done = True
        #for x in range(0,len(testInt[0])):
    xVal = (((arr[axis][ind])/(max(arr[0])-min(arr[0])))*300)+300
    yVal = (((arr[2][ind])/(max(arr[2])-min(arr[2])))*-300)+300
    xValInt = int(xVal.astype(int))
    yValInt = int(yVal.astype(int))
    #print(str(xValInt)+" | " + str(yValInt)+" | " + str(xVal)+" | " + 
         # str(yVal)+" | " + str(max(arr[0]))+" | " + str(arr[axis][ind]))
    #print(xVal, yVal)
    pygame.draw.circle(screen, color, (xValInt, yValInt), 10)
    #xOld = xVal
    #yOld = yVal  

def pygame_start():
    init_pygame()
    BLACK = (0,0,0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0 )
    GREEN = (0, 255, 0) 
    BLUE = (0,0,255)
    global pos
    pos = get_doubleIntegral_array(shotArr['shot0'])
    x=0
    while x<len(pos[0]):
        screen.fill(WHITE)
        pygame.draw.line(screen, BLACK, [0,300],[600,300], 5)
        pygame.draw.line(screen, BLACK, [300,0],[300,600], 5)
        pygame_draw(pos, screen, 0, x, RED)
        pygame_draw(pos, screen, 1, x, BLUE)
        pygame.display.flip()
        clock.tick(60)
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
    
    

