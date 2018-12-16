#!/usr/bin/env python
# encoding: utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

def test():
    video = cv2.VideoCapture("data/moon.avi")
    if video.isOpened():
        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        # Old version OpenCV
        if int(major_ver) < 3 :
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)   # float
            width = video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float
            height = video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT) # float
            print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
        # New version OpenCV
        else :
            # FRAME_WIDTH
            width = video.get(3)
            # FRAME_HEIGHT
            height = video.get(4)
            # FPS
            fps = video.get(5)
            # FRAME_COUNT
            frameCount = video.get(7)
            # DURATION
            duration = frameCount / fps
            
            print("width : {0}".format(width))
            print("height : {0}".format(height))
            print("frameCount : {0}".format(frameCount))
            print("FPS : {0}".format(fps))
            print("duration : {0}".format(duration))
            
        for frameNo in range(int(frameCount)):
            # frameNo = 0
            video.set(1, frameNo)
            ret0, frame0 = video.read()
            video.set(1, frameNo)
            ret, frame = video.read()
            
            imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            # imgray = cv2.GaussianBlur(imgray,(5,5),0)
            thrs1 =600
            thrs2 =200
            edge = cv2.Canny(imgray, thrs1, thrs2, apertureSize=5)
            ret,binary = cv2.threshold(imgray,127,255,0)
            # binary = cv2.adaptiveThreshold(edge,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            im2, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            for contourNo in range(len(contours)):
                area = cv2.contourArea(contours[contourNo])
                if ((area > 500) and (area < 800)):
                    contourSelected = contourNo
                    areaSelected = area
            cv2.drawContours(frame, contours, contourSelected, (128,128,0), 1)
            
            imgText = addText2img(frame, str(areaSelected), x = 0, y = 15, font_size = 1)
            cv2.imshow("",imgText)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    video.release()
    # cv2.destroyAllWindows()

def addText2img(im, text = 'TEMP', x = 0, y = 0, font_size = 1):
	font = cv2.FONT_HERSHEY_PLAIN
	cv2.putText(im, text, (x, y), font, font_size, (28, 128, 128))
	return im
    
# http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#
if __name__ == '__main__' :
    test()