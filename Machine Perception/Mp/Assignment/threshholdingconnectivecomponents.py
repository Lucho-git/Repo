import cv2
import glob
from matplotlib import pyplot as plt
import numpy as np


files = glob.glob("./DirectionalSignage/*.jpg")
count = 0

randomnumbers = [int]*100
count = 0

def imshow_components(connect):

    print("nothing")
    label_hue = np.uint8(179*connect/np.max(connect)) 
    blank_ch = 255*np.ones_like(label_hue)

    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue==0] = 0

    #cv2.imshow('connected components', labeled_img)

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)

    return squares 

def find_squares2(img, cos_limit = 0.1):
    print('search for squares with threshold %f' % cos_limit)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < cos_limit :
                        squares.append(cnt)
                    else:
                        #print('dropped a square with max_cos %f' % max_cos)
                        pass
    return squares


ddepth = -1
sharpen = np.array((
	[0,-1,0],
	[-1,5,-1],
	[0,-1,0]), dtype ="int")


for file in files[0:]:


    img = cv2.imread(file)
    #gray = cv2.imread(file,0)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	

    #blur = cv2.GaussianBlur(gray,(5,5),0)  

    #sharp = blur


   # sharp = cv2.filter2D(blur, ddepth, sharpen)
    #cv2.imshow('notequalized', blur)
    #sharp = cv2.equalizeHist(sharp)
    #cv2.imshow('equalized', sharp)
    #cv2.waitKey(0)

    cv2.imshow('colour',img)
    cv2.waitKey(0)

    _,thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # ensure binary
    _,thresh2 = cv2.threshold(gray, 50, 255, cv2.THRESH_TRUNC)  # ensure binary

   # _,thresh2 = cv2.threshold(sharp, 20, 255, cv2.THRESH_BINARY)  # ensure binary

    _,thresh3 = cv2.threshold(gray, 0, 255, cv2.THRESH_TRUNC+cv2.THRESH_OTSU)  # otsus
    #_,thresh3 = cv2.threshold(sharp, 127, 255, cv2.THRESH_TOZERO)  # ensure binary
    thresh4 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    thresh5 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)


    #otsu = cv2.bitwise_not(otsu)
    titles = ['Grayscale','BINARY', 'TRUNC', 'OTSU','Adaptive_Gaussian','Adaptive Mean']
    images = [gray,thresh1,thresh2,thresh3,thresh4,thresh5]
    
    print(len(images))
    for i in images:
        squares = find_squares(i)
        cv2.drawContours(i, squares,0,(110,110,70),2)
        hist = cv2.equalizeHist(i)  
        cv2.imshow('title',i)

        cv2.waitKey(0)



    for i in range(len(images)):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()


    



   # ret, connect = cv2.connectedComponents(otsu, connectivity=4)

   # im2, contours, hierarchy = cv2.findContours(otsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   # cv2.drawContours(im2, contours, -1, (100,100,30), 2)

    #imshow_components(connect)
   # cv2.imshow('im2',im2)
	
    #cv2.waitKey(0)
###

####https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

