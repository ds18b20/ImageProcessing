#!/usr/bin/env python
# encoding: utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt

def findContours():
    imOri = cv2.imread('data/sample.jpg')
    im = cv2.imread('data/sample.jpg')
    
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # imgray = cv2.GaussianBlur(imgray,(5,5),0)
    thrs1 =900
    thrs2 =300
    edge = cv2.Canny(imgray, thrs1, thrs2, apertureSize=5)
    # ret,binary = cv2.threshold(imgray,127,255,0)
    binary = cv2.adaptiveThreshold(edge,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    
    im2, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # im2, contours, hierarchy = cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_CODE)

    # print(len(contours))
    # print(hierarchy)
    for i in range(len(contours)):
        print('{:d}:{:f}'.format(i,cv2.contourArea(contours[i])))
    print('im.shape[0:2]:\n', im.shape[0:2])
    cv2.drawContours(im, contours, 29, (128,128,0), 5)
    
    print('contours[0]:\n', contours[0])
    
    perimeter = cv2.arcLength(contours[0],False)
    epsilon = 0.1*perimeter
    approx = cv2.approxPolyDP(contours[0],epsilon,True)
    
    titles = ['1.Original Image', '2.Edge', '3.AdaptiveBinary', '4.Contours']
    images = [imOri, edge, binary, im]
    
    for i in range(4):
        plt.subplot(2,2,i+1),plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()
    
if __name__ == '__main__':
    findContours()