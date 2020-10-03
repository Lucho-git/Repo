import cv2
import glob
from matplotlib import pyplot
import numpy as np

files = glob.glob("./*.png")
files += glob.glob("./*.jpg")
count = 0
imgpath = 'prac02ex04img01.png'

print(len(files))

for file in files[0:]:

	print("Num files")





#	img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_HSV2BGR)


img_bgr = cv2.imread(imgpath)
img_colorchange = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
dst = cv2.equalizeHist(img_colorchange)



cv2.imshow("Original", img_bgr)
cv2.imshow("Equalized", dst)
cv2.waitKey(0)


color = ('b','g','r')
for i,col in enumerate(color):
	histr = cv2.calcHist([img_bgr],[i],None,[256],[0,256])
	pyplot.plot(histr,color = col)
	pyplot.xlim([0,256])
pyplot.show()

