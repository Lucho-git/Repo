import cv2
import glob
from matplotlib import pyplot
import numpy as np

files = glob.glob("./*.png")
files += glob.glob("./*.jpg")
count = 0
imgpath = 'prac02ex02img01.jpg'

print(len(files))

for file in files[0:]:

	print("Num files")





#	img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_HSV2BGR)


img_bgr = cv2.imread(imgpath)
img_colorchange = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
img_colorchange = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

img_colorchange = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2Luv)
#img_colorchange = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2Lab)

cv2.imshow("Display Window", img_colorchange)
cv2.waitKey(0)


