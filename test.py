# -*- coding: utf-8 -*-


import numpy as np
import traceback
import matplotlib.pyplot as plt
import cv2

def countColorByRow(row):
    
    colorNum = []
    tcount = 0
    tcolor = (-1,-1,-1)
    for i, elm in enumerate(row):
        tcol = tuple(elm)
        if tcolor == tcol:
            tcount = tcount +1
        else:
            if tcount>0:
                colorNum.append([tcolor, tcount])
            tcount = 1
            tcolor = tcol
            
    if tcount>0:
        colorNum.append([tcolor, tcount])
    
    return colorNum

def countColorByImg(img):
    
    imgColorCount=[]
    for i, row in enumerate(img):
        
        trst = countColorByRow(row)
        imgColorCount.append(trst)
        
        if len(trst)<=1:
            continue
        print("\n\n***********i=%d, len=%d"%(i, len(trst)))
        for tcount in trst:
            if tcount[1]>10:
                print(tcount)
        if i>150:
            break
    
    '''
    for i, rowCount in enumerate(imgColorCount):
        print(i, rowCount)
        if i>10:
            break
    '''

def uiDetect(tpath):
    
    img = cv2.imread(tpath, 1) #IMREAD_GRAYSCALE 
    print(img.shape)
    #plt.imshow(img) #, cmap='gray'
    #plt.show()
    
    countColorByImg(img)

    
if __name__ == "__main__":
    
    tpath='img/001.jpg'
    uiDetect(tpath)