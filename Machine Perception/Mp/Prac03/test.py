import cv2
import glob
from matplotlib import pyplot as plt
import numpy as np

files = glob.glob("./*.png")
files += glob.glob("./*.jpg")
count = 0




print(len(files))

for file in files[0:]:


	img = cv2.imread(file)
	gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
	gray = np.float32(gray)
	corners = cv2.cornerHarris(gray,10,3,0.04)
	corners = cv2.dilate(corners,None)
	img[corners>0.01*corners.max()]=[0,0,255]	

	plt.subplot(2,1,1), plt.imshow(img, cmap = 'jet')
	plt.title('harris corner detection'), plt.xticks([]), plt.yticks([])


	img2 = cv2.imread(file)
	corners2 = cv2.goodFeaturesToTrack(gray,25,0.01,10)
	corners2 = np.int0(corners2)

	for i in corners2:
		x,y = i.ravel()
		cv2.circle(img2,(x,y),10,(0,0,255),-1)



	plt.subplot(2,1,2), plt.imshow(img2, cmap = 'gray')
	plt.title('jap name edge detection'), plt.xticks([]), plt.yticks([])

	plt.show()

	cv2.waitKey(0)


