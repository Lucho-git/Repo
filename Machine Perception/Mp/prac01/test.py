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
	imgScale = 0.5
	newimg = cv2.resize(img,(int(width/2),int(height/2)))
	cv2.imshow('newimg',newimg)
	word = 'save' + str(count) + '.png'
	cv2.imwrite(word,newimg)
	count +=1
	color = ('b','g','r')
	for i,col in enumerate(color):
		histr = cv2.calcHist([img],[i],None,[256],[0,256])
		pyplot.plot(histr,color = col)
		pyplot.xlim([0,256])
	pyplot.show()


#	count+=1
#	print(count)

