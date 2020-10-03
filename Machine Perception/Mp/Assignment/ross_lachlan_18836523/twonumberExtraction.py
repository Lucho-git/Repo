import cv2
import glob
from matplotlib import pyplot as plt
import numpy as np
import copy

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
    #img = cv2.GaussianBlur(img,(5,5),0)     
    #img = cv2.filter2D(img, ddepth, sharpen)
    #img = cv2.GaussianBlur(img,(5,5),0)     
     

    #convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #define colour range, below 50 saturation defines white, gray and black range.
    lower_val = np.array([0,0,0]) #lowest threshold is [0,0,0] black
    upper_val = np.array([179,50,255]) # all 179 hue values, all 255 values, 50/255 saturation


    #all light levels above 120 are set to white 255
    lower_val7 = np.array([0,0,120]) #lowest threshold is [0,0,0] black
    upper_val7 = np.array([179,50,255]) # all 179 hue values, all 255 values, 50/255 saturation


    #threshold using previously defined colour range
    #anything higher than the 50 saturation value will be converted to 115 gray, anything higher than 190 light level will be pure white
    mask = cv2.inRange(hsv, lower_val, upper_val)
    mask2 = cv2.inRange(hsv, lower_val7, upper_val7)
    mask = cv2.bitwise_not(mask)
    img[mask != 0] = [115,115,115]
    img[mask2 !=0] = [255,255,255]
    img[mask2 == 0] = [115,115,115]


    #make hsv processed image gray
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    img = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 17, -10)
   
    img = cv2.filter2D(img, ddepth, sharpen)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))


    #cv2.imshow('binerized', img)
    #cv2.waitKey(0)




    #gets rid of bad patches, filter by contour size and shape
    badcontours = []

    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        appended = False
        hull = cv2.convexHull(cnt)


        #any contours under a certain size are considered bad
        if(cv2.contourArea(hull)<80 and not appended):
            badcontours.append(cnt)
            appended = True

        if(cv2.contourArea(hull)>2000 and not appended):
            badcontours.append(cnt)
            appended = True

        x,y,w,h = cv2.boundingRect(cnt)

        if(h > 40 or h < 10 and not appended):
            badcontours.append(cnt)
            appended = True
        
        if(w > 30 or w < 8 and not appended):
            badcontours.append(cnt)
            appended = True        

    #fill in all bad contours with black
    cv2.fillPoly(img, badcontours,(0,0,0))



    #Dialate then sharpen the image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

    img = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel2)
    img = cv2.filter2D(img, ddepth, sharpen)

    imh,imw = img.shape




    #crop the edge thirds off of the image
    img = img[0 : imh, int(imw/3-15): int(2*(imw/3))]
    outimg = copy.copy(img)


    #find remaining contours, sort them into columns
    goodcontours = []
    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        goodcontours.append(hull)

    verticle = []

    for cnt in goodcontours:
        x,y,w,h = cv2.boundingRect(cnt)


        left = x
        right = x+w
        height = y

        column = []
        column.append(cnt)


        for index,value in enumerate(goodcontours):
            i,j,l,m = cv2.boundingRect(goodcontours[index])

            left2 = i
            right2 = i+l
            height2 = j

            #checks if contours have overlapping x values in their bounding boxes
            #this gets bounding boxes that share the same column area
            if((left2 >= left and left2 <= right) or (right2 <= right and right2 >= left) or (left >= left2 and left <= right2) or (right <= right2 and right >= left2)):
                    if(not height == height2):
                        column.append(goodcontours[index])
        if(len(column) >1):
            verticle.append(column)


    #order the contours using y value, low to high
    for line in verticle:
        ordervert = []
        for cnt in line:
            x,y,w,h = cv2.boundingRect(cnt)
            ordervert.append(y)
                        
        swapped = True
        while swapped:
            swapped = False
            for x in range(len(ordervert) -1):
                if ordervert[x] > ordervert[x+1]:
                    ordervert[x], ordervert[x+1] = ordervert[x+1], ordervert[x]
                    line[x], line[x+1] = line[x+1], line[x]
                    swapped = True


    #create a same size list of the contours containing each of their y values
    heightlist = []
    for line in verticle:
        verheight = []
        for cnt in line:
            x,y,w,h = cv2.boundingRect(cnt)
            verheight.append(y)
        heightlist.append(verheight)



    #remove any duplicate contours columns, based on matching y values
    newvert = []
    newheight = []

    remcount = 0
    for index in range(len(verticle)):
        if index == 0:
            newvert.append(verticle[index])
            newheight.append(heightlist[index])
        else:
            unique = True
            for element in newvert:
                for index2 in range(len(verticle)):
                    if not index == index2:


                        if(len(heightlist[index]) == len(heightlist[index2])):

                            if(str(heightlist[index]) == str(heightlist[index2])):
                                unique = False
                                #print("not unique")
                                break
                    if(not unique):
                        break

            if (unique):
                newvert.append(verticle[index])
                newheight.append(heightlist[index])
  

    #sort contour columns, so that only contours with all even distances apart remain
    even = []
    evenheight = []
 
    for line,height in zip(newvert,newheight):
        loop = True
        if len(height) <= 2:
            line = None
            height = None
            loop = False

        while loop:


            index = 0
            frequency = []
            for i in range(len(height)):
                indir = []
                if(i == 0):
                    right = abs(height[i]-height[i+1])
                    indir.append(right)
                    indir.append(index)

                elif(i == len(height)-1):
                    left = abs(height[i]-height[i-1])
                    indir.append(left)
                    indir.append(index)

                else:
                    right = abs(height[i]-(height[i+1]))
                    left = abs(height[i] - (height[i-1]))
                    indir.append(left)
                    indir.append(right)
                    indir.append(index)


                frequency.append(indir)
                index +=1


            blank = []
            counter = [0] *len(frequency)
            for i in range(len(frequency)):
                if(len(blank) == 0):
                    blank.append(frequency[0][0])
                    counter[0] += 1
                elif(len(frequency[i]) == 2):

                    new = True
                    for x in blank:
                        if(abs(frequency[i][0] - x) < x*0.2):
                            counter[blank.index(x)] +=1
                            new = False
                    if(new):
                        blank.append(frequency[i][0])
                        counter[len(blank)] += 1

                else:
                    new = True
                    for x in blank:
                        if(abs(frequency[i][1] - x) < x*0.2):
                            counter[blank.index(x)] +=1
                            new = False
                    if(new):
                        blank.append(frequency[i][1])
                        counter[len(blank)] += 1
                       
            maximum = 0    
            for i in range(len(blank)):
                if(counter[i] > maximum):
                    maximum = counter[i]
                    index = i
            deleted = False


            median = blank[index]


            #might need a -1
            end = len(frequency)-1
            if(median < frequency[end][0]):
                if(frequency[end][0] - median > median *0.2):
                    del height[end]
                    del line[end]
                    del frequency[end]
                    deleted = True
            elif(median >= frequency[end][0] and median - frequency[end][0] > median *0.2):
                sums = frequency[end][0]
                count = 0
                while(median >= sums and median - sums > median*0.2):
                    sums += frequency[end-count-1][0]
                    count +=1
                if(abs(median - sums) < 0.2 * median):
                    #delete values between 0 and index value
                    for x in range(count):
                        del height[end-x-1]
                        del line[end-x-1]
                        del frequency[end-x-1]
                        deleted = True



            if(median < frequency[0][0]):
                if(frequency[0][0] - median > median *0.2):
                    del height[0]
                    del line[0]
                    del frequency[0]

                    deleted = True
            elif(median >= frequency[0][0] and median - frequency[0][0] > median *0.2):
                sums = frequency[0][0]
                count = 0
                while(median >= sums and median - sums > median*0.2):
                    sums += frequency[count+1][0]
                    count +=1
                if(abs(median - sums) < 0.2*median):
                    #delete values between 0 and index value
                    for x in range(count):
                        del height[count-x]
                        del line[count-x]
                        del frequency[count-x]
                        deleted = True

            if(not deleted and len(blank) > 1):
                for i in range(1,len(frequency)-1):
                    left = frequency[i][0]
                    right = frequency[i][1]
                    if(abs(median-(left+right)) < 0.2*median):
                        del height[i]
                        del line[i]
                        del frequency[i]
                        deleted = True
                        break
 
            if(not deleted and len(blank) > 1):
                for i in range(1,len(frequency)-1):
                    left = frequency[i][0]
                    right = frequency[i][1]
                    if(median-left > 0.2*median and median - right > 0.2*median):
                        del height[i]
                        del line[i]
                        del frequency[i]
                        deleted = True   
                        break                    
   
            if(not deleted and len(blank) > 1):
                for i in range(1,len(frequency)-1):

                    left = frequency[i][0]
                    right = frequency[i][1]
                    if( abs(median-left) > 0.2*median or abs(median-right) > 0.2*median):
                        del height[i]
                        del line[i]
                        del frequency[i]
                        deleted = True   
                        break                         

            if not deleted:

                loop = False
                even.append(line)
                evenheight.append(height)

            if len(height) <= 2:
                loop = False



    newvert = []
    newheight = []

    for index in range(len(even)):
        if index == 0:
            newvert.append(even[index])
            newheight.append(evenheight[index])
        else:
            unique = True
            for element in newvert:
                for index2 in range(len(even)):
                    if not index == index2:


                        if(len(evenheight[index]) == len(evenheight[index2])):

                            if(str(evenheight[index]) == str(evenheight[index2])):
                                unique = False
                                #print("NOT UNIQUE")
                                break
                    if(not unique):
                        break


            if (unique):
                newvert.append(even[index])
                newheight.append(evenheight[index])


    #scores contours list values based on desirable traits, e.g. similar width,area,xvalue
    rank = []
    xlist = []

    for line in newvert:

        score = []
        score.append(len(line)*2)
        xcompare = []
        areacompare = []
        widthcompare = []

        #gathers info
        for cnt in line:
            x,y,w,h = cv2.boundingRect(cnt)
            left = x
            right = x+w
            xcompare.append(x)
            areacompare.append(w)
            widthcompare.append(cv2.contourArea(cnt))

        #score area
        asum = 0
        for i in areacompare:
            asum += i
        asum = asum/len(areacompare)
        countscore =0
        for i in areacompare:
            if(abs(asum - i) < 0.2*asum):
                countscore += 2
        if(countscore == 0):
            score.append(0)
        else:
            score.append(countscore/len(line))

        #scores width
        wsum = 0
        for i in widthcompare:
            wsum += i
        wsum = wsum/len(widthcompare)
        countscore = 0
        for i in widthcompare:
            if(abs(wsum - i) < 0.2*wsum):
                countscore += 2
        if(countscore == 0):
            score.append(0)
        else:
            score.append(countscore/len(line))

        #scores xsize
        xsum = 0
        for i in xcompare:
            xsum += i
        xsum = xsum/len(xcompare)
        countscore =0
        for i in xcompare:
            if(abs(xsum - i) < 0.3*xsum):
                countscore += 2  
        if(countscore == 0):
            score.append(0)
        else:
            score.append(countscore/len(line))
        xlist.append(xsum)
        rank.append(score)

    #picks a best contour list to use
    max1 = 0
    index1 = -1
    max2 = 0 
    index2 = -1
    max3 = 0
    index3 = -1

    #find the rightmost 3 columns
    for i in range(len(xlist)):
        if(xlist[i] > max1):
            temp = max1
            tempdex = index1
            max1 = xlist[i]
            index1 = i

            temp2 = max2
            tempdex2 = index2
            max2 = temp2
            index2 = tempdex2

            max3 = temp2
            index3 =tempdex2

        elif(xlist[i] > max2):
            temp = max2
            tempdex = index2
            max2 = xlist[i]
            index2 = i

            max3 = temp
            index3 = tempdex
        elif(xlist[i] > max3):
            max3 = xlist[i]
            index3 = i
        
    rank[index1][0] += 10
    if index2 > -1:
        rank[index2][0] += 7
    if index3 > -1:
        rank[index3][0] += 5
        
    final = []
    index = 0

    #score everything based on previous score detections

    highest = 0
    for i in range(len(rank)):

        fscore = 0
        for x in rank[i]:
            fscore += x

        if fscore > highest:
            highest = fscore
            index = i
    bestconts = newvert[index]


    xsum = 0
    for cnt in bestconts:
        x,_,_,_ = cv2.boundingRect(cnt)
        xsum += x
        
    xsum = xsum/len(bestconts)
    
    straight = True

    for cnt in bestconts:
        x,_,_,_ = cv2.boundingRect(cnt)
        if(abs(xsum - x) > 0.25*xsum):

             straight = False



    numbers = []
    numberlist = []
    bigreclist = []



    #isolate each number cluster on the sign
    if(straight):
        for cnt in bestconts:
            i,j,l,m = cv2.boundingRect(cnt)
            img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            numapp = 0
            draw = copy.copy(img)
            reclist = [] 
            minx = 99999
            miny = 99999
            maxx = 0
            maxy = 0
            for cnt2 in contours:
                hull = cv2.convexHull(cnt2)
                x,y,w,h = cv2.boundingRect(cnt2)
                if (abs(y-j) < j*0.07) and (x < i):
                    if(h < 3*m and w < 1.5*l):
                        if(x > i-6*w and numapp < 4):
                            cv2.rectangle(draw, (x,y),(x+w,y+h),(255,255,100),2,8,0)  
                            numbers.append(cnt2)
                            numbers.append(cnt)
                            numapp += 1
                           
                            if(x < minx):
                                minx = x
                            if(y < miny):
                                miny = y
                            if(x+w > maxx):
                                maxx = x+w
                            if(y+h > maxy):
                                maxy = y+h
            x,y,w,z = cv2.boundingRect(cnt)
            if(x < minx):
                minx = x
            if(y < miny):
                miny = y
            if(x+w > maxx):
                maxx = x+w
            if(y+h > maxy):
                maxy = y+h


            reclist.append(minx)  
            reclist.append(miny)  
            reclist.append(maxx)  
            reclist.append(maxy)  

            numberlist.append(numbers)
            #cv2.imshow('sorted', draw)
            #cv2.waitKey(0)   

            bigreclist.append(reclist)

    print(len(bigreclist))
    if(len(bigreclist)>0):
        print(len(bigreclist[0]))

    draw = copy.copy(img)

    numbercrop = []

    for rec in bigreclist:
        crop = img[rec[1] : rec[3], rec[0]: rec[2]]
        crop = cv2.copyMakeBorder(crop,4,4,4,4,cv2.BORDER_CONSTANT,(0,0,0))
        h,w = crop.shape
        if(w > 60):
            numbercrop.append(crop)
        
            #cv2.imshow('sign', crop)
            #cv2.waitKey(0) 

    #use bubble sort to make sure number cluster stays in order
    numberlist = []
    for crop in numbercrop:
        crop, contours, hierarchy = cv2.findContours(crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        numbers = []
        sort = []

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

        for cnt in contours:
            hull = cv2.convexHull(cnt)
            x,y,w,h = cv2.boundingRect(cnt)

            cropimg = crop[y : y+h, x: x+w]
    
            cropimg = cv2.copyMakeBorder(cropimg,3,3,3,3,cv2.BORDER_CONSTANT,(0,0,0))

            numbers.append(cropimg)

            #cv2.imshow('rec', cropimg)
            #cv2.waitKey(0)   
        numberlist.append(numbers)
        



    #return cropped numbers, and cropped sign area
    return numberlist, outimg, True








