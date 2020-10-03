import cv2
import glob
from matplotlib import pyplot as plt
import numpy as np

files = glob.glob("./*.png")
files += glob.glob("./*.jpg")
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

	cv2.imshow('connected components', labeled_img)





for file in files[0:]:


	img = cv2.imread(file)
	#gray = cv2.imread(file,0)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	

	blur = cv2.GaussianBlur(gray,(5,5),0)

	#_,otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	_,otsu = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)  # ensure binary

	#otsu = cv2.bitwise_not(otsu)


	cv2.imshow('otsu',gray)




	ret, connect = cv2.connectedComponents(otsu, connectivity=4)

	im2, contours, hierarchy = cv2.findContours(otsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(im2, contours, -1, (100,100,30), 2)

	imshow_components(connect)
	cv2.imshow('im2',im2)
	
	cv2.waitKey(0)
###

####https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

