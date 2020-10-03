import cv2
import glob
from matplotlib import pyplot as plt
import numpy as np


#puts coordinate points for image rotation in a consistant order
def order_points(pts):
    #initialize ordered coordinates representing a rectangle, rectangle can be angled
    #order, top left, top right, bottom right, bottom left,
    rect = np.zeros((4,2),dtype ="float32")


    #finds the minimum and maximum sum of coordinates as this represents top left and bottom right
    minimum = pts[0]
    maximum = pts[0]
    for i in pts:
        if(i[0] + i[1] > maximum[0] + maximum[1]):
            maximum = i
        if(i[0] + i[1] < minimum[0] + minimum[1]):
            minimum = i

    rect[0] = minimum
    rect[2] = maximum

    #find the difference between coordinate values, as this represents top right vs bottom left
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


#takes in a bounding box around the numbers on the building sign, and rotates to remove tilt from numbers
def warpRotation(img, pts):
    #orders the coordinates consistantely
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    #calcs maximum possible width
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    #calcs max possible height
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")

    #use getPerspective and warpPerspective to rotate rectangle straight
    M = cv2.getPerspectiveTransform(rect,dst)
    warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    return warped

#responsible for detecting the sign contour, post image processing
def find_squares(img):

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

                #implementation of douglas pecker algorithm, grabs a polygon, but allows some leeway based on the arclength
                cnt_len = 0.08 * cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, cnt_len, True)
                #checks polygon has 4 sides, and is above and below size thresholds
                if len(cnt) == 4 and cv2.contourArea(cnt) > 4000 and cv2.contourArea(cnt)<30000 and cv2.isContourConvex(cnt):
                    squares.append(cnt)

    return squares 


#processes and extracts numbers from sign
def process_sign(crop):

    badcontours = []

    height, width = crop.shape

    #grabs all contours using convex hull and puts minrect around them
    cropimg, contours, hierarchy = cv2.findContours(crop, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        appended = False
        hull = cv2.convexHull(cnt)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        #if any rectangle section touches the edge, that contour is considered bad
        if(box[0][0] < 1 or box[0][1] < 1 or box[1][0] < 1 or box[1][1] < 1 and box[2][0] < 1 or box[2][1] < 1 or box[3][0] < 1 or box[3][1] < 1):
            badcontours.append(cnt)
            appended = True

        if(box[0][0] >= width-1 or box[1][0] >= width-1 or box[2][0] >= width-1 or box[3][0] >= width-5):
            if(not appended):
                badcontours.append(cnt)
                appended = True

        if(box[0][1] >= height-1 or box[1][1] >= height-1 or box[2][1] >= height-1 or box[3][1] >= height-1):
            if(not appended):
                badcontours.append(cnt)
                appended = True       


        cv2.imshow('new',img)
        cv2.waitKey(0)

        #any contours under a certain size are considered bad
        if(cv2.contourArea(hull)<300 and not appended):
            badcontours.append(cnt)

    
        cv2.imshow('new',img)
        cv2.waitKey(0)

    #bad contours are filled with black (0,0,0)
    cv2.fillPoly(cropimg, badcontours,(0,0,0))

    cv2.imshow('aftercrop',cropimg)
    cv2.waitKey(0)


    #grab remaining contours, should only be numbers now
    cropimg, contours, hierarchy = cv2.findContours(crop, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    combine = []

    #takes the min area around combined contours, this gets angle of number slant
    for cnt in contours:
        for i in cnt:
            combine.append(i)

    combine = np.asarray(combine)


    minrect = cv2.minAreaRect(combine)
    box = cv2.boxPoints(minrect)
    box = np.int0(box)

    #rotates slanted numbers to be straight
    cropimg = warpRotation(cropimg, box)

    #thresholds again after rotation reintroduces gray values
    _,cropimg = cv2.threshold(cropimg, 200, 255, cv2.THRESH_BINARY)

    #adds a thin border around number cluster
    cropimg = cv2.copyMakeBorder(cropimg,10,10,10,10,cv2.BORDER_CONSTANT,(0,0,0))

    #grab individual external contours, each should be a number
    cropimg, contours, hierarchy = cv2.findContours(cropimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    numbers = []
    sort = []
    sortcont = []

    #place rectangle around each contour and grabs coordinate x value representing top left coordinate
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        sort.append(x)
        
    #implement bubble sort, based on x bounding box of each contour, to sort left to right
    swapped = True
    while swapped:
        swapped = False
        for x in range(len(sort) -1):
            if sort[x] > sort[x+1]:
                sort[x], sort[x+1] = sort[x+1], sort[x]
                contours[x], contours[x+1] = contours[x+1], contours[x]
                swapped = True

    #place rectangle around each individual number, crop them out seperately into a list
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        x,y,w,h = cv2.boundingRect(cnt)

        crop = cropimg[y : y+h, x: x+w]

        crop = cv2.copyMakeBorder(crop,4,4,4,4,cv2.BORDER_CONSTANT,(0,0,0))

        numbers.append(crop)

    #return cropped numbers, and cropped signarea
    return numbers, cropimg


#main of this module, takes in 1 image to process at a time, locates sign and extracts numbers
def runExtract(inFile):

#image preprocessing begins

#creating kernel used to sharpen images, and default values
    ddepth = -1
    sharpen = np.array((
	    [0,-1,0],
	    [-1,5,-1],
	    [0,-1,0]), dtype ="int")

    #read in image
    img = cv2.imread(inFile)


    #blur, sharpen, blur
    img = cv2.GaussianBlur(img,(5,5),0)     
    img = cv2.filter2D(img, ddepth, sharpen)
    img = cv2.GaussianBlur(img,(5,5),0)     
     

 

    #convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define colour range, below 50 saturation defines white, gray and black range.
    lower_val = np.array([0,0,0]) #lowest threshold is [0,0,0] black
    upper_val = np.array([179,50,255]) # all 179 hue values, all 255 values, 50/255 saturation

    #define black tinged with blue colour range
    lower_val2 = np.array([80,0,0])
    upper_val2 = np.array([150,255,100]) 
    

    # define red value range below 100 light level, 2 range sets are required due to red being 0 on hsv gradient, up to 90 saturation
    lower_val3 = np.array([0,0,0])
    upper_val3 = np.array([15,90,100])
    lower_val4 = np.array([165,0,0])
    upper_val4 = np.array([179,90,100]) 


    #all light levels above 190 are set to white 255
    lower_val7 = np.array([0,0,190]) #lowest threshold is [0,0,0] black
    upper_val7 = np.array([179,50,255]) # all 179 hue values, all 255 values, 50/255 saturation


    #preprocess, by whitening and blackening some background sections
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
    #anything higher than the 50 saturation value will be converted to 115 gray, anything higher than 190 light level will be pure white
    mask = cv2.inRange(hsv, lower_val, upper_val)
    mask2 = cv2.inRange(hsv, lower_val7, upper_val7)
    mask = cv2.bitwise_not(mask)
    img[mask != 0] = [115,115,115]
    img[mask2 !=0] = [255,255,255]



    #make hsv processed image gray
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #binarize on threshold 114
    _,thresh1 = cv2.threshold(gray, 114, 255, cv2.THRESH_BINARY)  # ensure binary

    #create morphology kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))


    cv2.imshow('new',img)
    cv2.waitKey(0)

    #apply morphology kernel for the OPEN operation
    prebound = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
    thresh1 = prebound

    #find contours of decent size and shape
    squares = find_squares(thresh1)
    if(len(squares) >= 1):
        rect = cv2.minAreaRect(squares[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        #cv2.drawContours(thresh1,[box],0,(100,100,100),2)
        x,y,w,h = squares[0]

        #the x,y,w,h values are different depending on the angle of square, this checks to make sure the right values are used while cropping
        if(x[0][0] > w[0][0]):
            crop = thresh1[h[0][1]:y[0][1], h[0][0]:y[0][0]]
        else:
            crop = thresh1[x[0][1]:w[0][1], x[0][0]:w[0][0]]

        #if sign processing fails e.g.(sign detected, but numbers are bad), catch expection here and return invalid
        try:
            x,y = process_sign(crop)
        except Exception:
            print("Sign Proccessing Failed")
            return False, False, False

        return x,y,True
    else:
        print("No Sign Detected")

    return False,False,False







