import cv2
import glob
from matplotlib import pyplot

files = glob.glob("./*.png")
count = 0

print(len(files))

for file in files[0:]:
	img = cv2.imread(file)
	cv2.imshow("Display Window", img)
	cv2.waitKey(0)
	height, width, _ = img.shape
	print( file, height, width)

	f = open('prac01ex02crop.txt')

	contents = f.read()
	coList = contents.split(" ")
	
	for i in coList:
		print(int(i))
	
	cv2.rectangle(img, (int(coList[0]),int(coList[1])), (int(coList[2]),int(coList[3])), (255,0,0), 2)
	cv2.circle(img, (int(coList[0]),int(coList[1])), 5, (0,0,255))
	cv2.circle(img, (int(coList[0]),int(coList[3])), 5, (0,0,255))
	cv2.circle(img, (int(coList[2]),int(coList[1])), 5, (0,0,255))
	cv2.circle(img, (int(coList[2]),int(coList[3])), 5, (0,0,255))

	#cropimg = img[0:100, 0:100]
	cv2.imshow('croppedimg',img)
	word = 'save' + str(count) + '.png'
	cv2.imwrite(word,img)
	count +=1

	
