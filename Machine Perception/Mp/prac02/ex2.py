import cv2
import glob
from matplotlib import pyplot
import numpy as np

files = glob.glob("./*.png")
files += glob.glob("./*.jpg")
count = 0
imgpath = './prac02ex01img01.jpg'

print(len(files))

for file in files[0:]:

	print("Num files")





#	img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_HSV2BGR)
window_name = 'filter2D Demo'

img_bgr = cv2.imread(imgpath)

ddepth = -1
ind = 0

laplacian = np.array((
	[0,1,0],
	[1,-4,1],
	[0,1,0]), dtype ="int")

sobelX = np.array((
	[-1,0,1],
	[-2,0,2],
	[-1,0,1]), dtype ="int")

sobelY = np.array((
	[-1,-2,1],
	[0,0,0],
	[1,2,1]), dtype ="int")

prewitX = np.array((
	[-1,0,1],
	[-1,0,1],
	[-1,0,1]), dtype ="int")

prewitY = np.array((
	[-1,-1,-1],
	[0,0,0],
	[1,1,1]), dtype ="int")

sharpen = np.array((
	[0,-1,0],
	[-1,5,-1],
	[0,-1,0]), dtype ="int")

while True:
	kernel_size = 3 +2 * (ind%5)
	kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
	kernel /= (kernel_size * kernel_size)

#change 3rd variable kernel type to change image
	dst = cv2.filter2D(img_bgr, ddepth, sharpen)

#	blur = cv2.blur(img_bgr,(5,5))
#	blur = cv2.GaussianBlur(img_bgr,(5,5),0)
	median = cv2.medianBlur(img_bgr,5)

	cv2.imshow(window_name, dst)
#	cv2.imshow('normal',img_bgr)
	cv2.imshow('med', median)
	cv2.waitKey(0)


	ind +=1






#img_colorchange = cv2.cvtColor(img_bgr, cv2.IMREAD_GRAYSCALE)






#cv2.imshow("Display Window", img_colorchange)
#cv2.waitKey(0)


