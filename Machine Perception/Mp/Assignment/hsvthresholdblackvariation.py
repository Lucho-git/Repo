import cv2
import glob
from matplotlib import pyplot as plt
import numpy as np

files = glob.glob("./*.png")
files += glob.glob("./*.jpg")
count = 0

def imshow_components(connect):

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
    #img = cv2.GaussianBlur(img, (5, 5), 0)
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
                cnt_len = 0.08 * cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 4000 and cv2.contourArea(cnt)<30000 and cv2.isContourConvex(cnt):
    
                    #cnt = cnt.reshape(-1, 2)
                    #max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])
                    #if max_cos < 0.1:
                    squares.append(cnt)

    return squares 



ddepth = -1
sharpen = np.array((
	[0,-1,0],
	[-1,5,-1],
	[0,-1,0]), dtype ="int")


for file in files[0:]:

    #read in image
    colour = cv2.imread(file)
    img = cv2.imread(file)
    img = cv2.GaussianBlur(img,(5,5),0)     
    img = cv2.filter2D(img, ddepth, sharpen)
    img = cv2.GaussianBlur(img,(5,5),0)     
     
    #img = cv2.GaussianBlur(img,(5,5),0)     
    #convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define colour range
    lower_val = np.array([0,0,0]) #lowest threshold is [0,0,0] black
    upper_val = np.array([179,50,255]) # all 179 hue values, all 255 values, 50/255 saturation values, representing the white-gray-black range
    lower_val2 = np.array([80,0,0])
    upper_val2 = np.array([150,255,100]) 
    
    #define black tinged with blue colour range, 2 range sets are required due to red being 0 on hsv gradient
    # red value range below 100 light level
    lower_val3 = np.array([0,0,0])
    upper_val3 = np.array([15,90,100])
    lower_val4 = np.array([165,0,0])
    upper_val4 = np.array([179,90,100]) 


    #make values whiter
    lower_val7 = np.array([0,0,190]) #lowest threshold is [0,0,0] black
    upper_val7 = np.array([179,50,255]) # all 179 hue values, all 255 values, 50/255 saturation


    #make any colour variation black
   # lower_val8 = np.array([0,0,0]) #lowest threshold is [0,0,0] black
   # upper_val8 = np.array([179,1,110]) # all 179 hue values, all 255 values, 50/255 saturation


    mask = cv2.inRange(hsv, lower_val2, upper_val2)
    img[mask != 0] = [0,0,0]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_val3, upper_val3)
    img[mask != 0] = [0,0,0]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_val4, upper_val4)
    img[mask != 0] = [0,0,0]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    #threshold using previously defined colour range
    #anything higher than the 50 saturation value will be converted to pure white
    mask = cv2.inRange(hsv, lower_val, upper_val)
    mask2 = cv2.inRange(hsv, lower_val7, upper_val7)
    mask = cv2.bitwise_not(mask)
    img[mask != 0] = [115,115,115]
    img[mask2 !=0] = [255,255,255]

    #mask3 = cv2.inRange(hsv, lower_val8, upper_val8)
    #img[mask3!=0] = [0,0,0]


    #apply mask
    #nocolour = cv2.bitwise_and(img,img,mask=mask)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)





    _,thresh1 = cv2.threshold(gray, 114, 255, cv2.THRESH_BINARY)  # ensure binary
    _,thresh2 = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)  # ensure binary

    #_,thresh2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)  # ensure binary

    _,thresh3 = cv2.threshold(gray, 0, 255, cv2.THRESH_TRUNC+cv2.THRESH_OTSU)  # otsus
    _,thresh3 = cv2.threshold(thresh3, 114,255, cv2.THRESH_BINARY)


    #_,thresh3 = cv2.threshold(sharp, 127, 255, cv2.THRESH_TOZERO)  # ensure binary
    thresh4 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    thresh5 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)


    #otsu = cv2.bitwise_not(otsu)
    titles = ['color','gray','blackbox','whitetext']
    images = [colour,gray,thresh1,thresh2]

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

    prebound = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
    images[2] = prebound

    cv2.imshow('color',img)

    for i in range(3):
        squares = find_squares(images[i+1])
        cv2.drawContours(images[i+1], squares,0,(110,110,70),2)
        #hist = cv2.equalizeHist(images[i+1])  
        #cv2.imshow('title',images[i+1])

        #cv2.waitKey(0)
        thresh1 = images[2]


    for i in range(4):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
   # plt.show()

    cv2.imshow('bestchoice',thresh1)
    #cv2.waitKey(0)
    
   # thresh1 = cv2.filter2D(thresh1, ddepth, sharpen)


    #opening = cv2.GaussianBlur(thresh1,(5,5),0)     
    #opening = cv2.GaussianBlur(opening,(5,5),0)     
    #opening = cv2.filter2D(opening, ddepth, sharpen)
    #opening = cv2.filter2D(opening, ddepth, sharpen)
    #cv2.imshow('morphed',opening)
    #cv2.waitKey(0)

    hulls = []

    ret, connect = cv2.connectedComponents(prebound, connectivity=4)

    im2, contours, hierarchy = cv2.findContours(prebound, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        if(cv2.contourArea(hull)>3000 and cv2.contourArea(hull) < 20000):
            hulls.append(hull)

    cv2.drawContours(im2, hulls, -1, (100,0,255), 2)



    imshow_components(connect)
    cv2.imshow('im2',im2)
	
    cv2.waitKey(0)
###

####https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/






