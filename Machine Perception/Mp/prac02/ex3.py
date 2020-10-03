import cv2
import glob
from matplotlib import pyplot
import numpy as np

files = glob.glob("./*.png")
files += glob.glob("./*.jpg")
count = 0
imgpath = './prac02ex03img01.jpg'

print(len(files))

for file in files[0:]:

	print("Num files")





#	img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_HSV2BGR)
window_name = 'filter2D Demo'

img_bgr = cv2.imread(imgpath)

ddepth = -1
ind = 0


#change 3rd variable kernel type to change image

#	blur = cv2.blur(img_bgr,(5,5))
#	blur = cv2.GaussianBlur(img_bgr,(5,5),0)
median = cv2.medianBlur(img_bgr,5)

cv2.imshow('normal',img_bgr)
cv2.imshow('med', median)
cv2.waitKey(0)








#img_colorchange = cv2.cvtColor(img_bgr, cv2.IMREAD_GRAYSCALE)






#cv2.imshow("Display Window", img_colorchange)
#cv2.waitKey(0)


