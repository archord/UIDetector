# -*- coding: utf-8 -*-


import numpy as np
import traceback
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os

def countColorByRow(row):
    
    colorNum = []
    tcount = 0
    tcolor = -1
    for i, tcol in enumerate(row):
        
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
        
        #if i>500:
        #    break
    
    return imgColorCount

def isBGRow(row):
    
    return len(row)==1 and row[0][1]>0

def analysisRowLayout(imgColorCount, elementMinHeight=5):
    
    bgRowIdxs = []
    for i, rowCount in enumerate(imgColorCount):
        if isBGRow(rowCount):
            bgRowIdxs.append(i)
    
    layoutIdxs = []
    for i, rowIdx in enumerate(bgRowIdxs[:len(bgRowIdxs)-1]):
        if bgRowIdxs[i+1] - bgRowIdxs[i] >elementMinHeight:
            layoutIdxs.append([bgRowIdxs[i], bgRowIdxs[i+1]])
            
    return layoutIdxs

def mergeRow(img):
    
    rst = img.min(axis=0)
    return rst

#elementMinWeight 统计分析确定
def analysisColLayout(img, rowLayoutIdxs, elementMinWeight=8, bgColor=250):
    
    colLayoutIdxs = []
    for lt in rowLayoutIdxs:
        minY = lt[0]
        maxY = lt[1]+1            
        timg = img[minY:maxY]
        
        tline = mergeRow(timg)
        tcounts = countColorByRow(tline)
        
        tlayouts = []
        tIdx = 0
        tRgnStart = 0
        for tc in tcounts:
            tcolor = tc[0]
            tnum = tc[1]
            if tcolor>=bgColor and tnum>elementMinWeight:
                if tIdx>tRgnStart:
                    tlayouts.append([tRgnStart, tIdx])
                tRgnStart = tIdx + tnum

            tIdx = tIdx + tnum
        
        if tIdx>tRgnStart:
                tlayouts.append([tRgnStart, tIdx])

        colLayoutIdxs.append(tlayouts)
            
    return colLayoutIdxs

def drawLayout(img, rowLayoutIdxs, colLayoutIdxs):
    
    #img = img.reshape(img.shape[0], img.shape[1],1).repeat(3,2)
    for i, lt in enumerate(rowLayoutIdxs):
        minY = lt[0]-2
        maxY = lt[1]+2
        
        if minY<0:
            minY = 0
        if maxY>img.shape[0]-1:
            maxY = img.shape[0]-1
        
        clts = colLayoutIdxs[i]
        for j, clt in enumerate(clts):
            minX = clt[0]-2
            maxX = clt[1]+2
            if minX<0:
                minX = 0
            if maxX>img.shape[1]-1:
                maxX = img.shape[1]-1
            cv2.rectangle(img,(minX,minY),(maxX,maxY),(0,0,255), thickness=2)
        
    return img
        

def analysis(imgColorCount):
        
    for i, rowCount in enumerate(imgColorCount):
        if len(rowCount)<=1:
            continue
        print("\n\n***********i=%d, len=%d"%(i, len(rowCount)))
        for tcount in rowCount:
            if tcount[1]>10:
                print(tcount)
                
        if i>140:
            break


def uiDetect(spath, dpath, imgName):
    
    tpath = "%s/%s"%(spath, imgName)
    print("process %s"%(tpath))
    imgRGB = cv2.imread(tpath, 1) #IMREAD_GRAYSCALE 0:gray, 1:rgb
    img = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
    #Image.fromarray(img).save("imgGray/001.jpg")
    #print(img.shape)
    #plt.imshow(img, cmap='gray') #
    #plt.show()
    
    imgColorCount = countColorByImg(img)
    #analysis(imgColorCount)
    rowLayoutIdxs = analysisRowLayout(imgColorCount, elementMinHeight=5)
    colLayoutIdxs = analysisColLayout(img, rowLayoutIdxs)
    
    img = drawLayout(imgRGB, rowLayoutIdxs, colLayoutIdxs)
    
    tpath = "%s/%s"%(dpath, imgName)
    #Image.fromarray(img).save(tpath)
    cv2.imwrite(tpath, img)
    
if __name__ == "__main__":
    
    spath='img1'
    dpath='imgRegion'
    
    timgs = os.listdir(spath)
    
    for imgName in timgs:
        uiDetect(spath, dpath, imgName)
        #break
    
    