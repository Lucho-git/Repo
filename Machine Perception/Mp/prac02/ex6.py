from __future__ import print_function
import cv2
import glob
from matplotlib import pyplot
import numpy as np
import argparse


files = glob.glob("./*.png")
files += glob.glob("./*.jpg")
count = 0
imgpath = 'prac02ex06img01.png'

print(len(files))

for file in files[0:]:

	print("Num files")



src = cv2.imread(imgpath)

erosion_size = 0
max_elem = 2
max_kernel_size = 21
title_trackbar_element_type = 'Element:\n 0: Rect \n 1: Cross \n 2: Ellipse'
title_trackbar_kernel_size = 'Kernel size:\n 2n +1'
title_erosion_window = 'Erosion Demo'
title_dilatation_window = 'Dilation Demo'

def erosion(val):
    erosion_size = cv2.getTrackbarPos(title_trackbar_kernel_size, title_erosion_window)
    erosion_type = 0
    val_type = cv2.getTrackbarPos(title_trackbar_element_type, title_erosion_window)
    if val_type == 0:
        erosion_type = cv2.MORPH_RECT
    elif val_type == 1:
        erosion_type = cv2.MORPH_CROSS
    elif val_type == 2:
        erosion_type = cv2.MORPH_ELLIPSE
    element = cv2.getStructuringElement(erosion_type, (2*erosion_size + 1, 2*erosion_size+1), (erosion_size, erosion_size))
    erosion_dst = cv2.erode(src, element)
    cv2.imshow(title_erosion_window, erosion_dst)


def dilatation(val):
    dilatation_size = cv2.getTrackbarPos(title_trackbar_kernel_size, title_dilatation_window)
    dilatation_type = 0
    val_type = cv2.getTrackbarPos(title_trackbar_element_type, title_dilatation_window)
    if val_type == 0:
        dilatation_type = cv2.MORPH_RECT
    elif val_type == 1:
        dilatation_type = cv2.MORPH_CROSS
    elif val_type == 2:
        dilatation_type = cv2.MORPH_ELLIPSE
    element = cv2.getStructuringElement(dilatation_type, (2*dilatation_size + 1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
    dilatation_dst = cv2.dilate(src, element)
    cv2.imshow(title_dilatation_window, dilatation_dst)


cv2.namedWindow(title_erosion_window)
cv2.createTrackbar(title_trackbar_element_type, title_erosion_window , 0, max_elem, erosion)
cv2.createTrackbar(title_trackbar_kernel_size, title_erosion_window , 0, max_kernel_size, erosion)
cv2.namedWindow(title_dilatation_window)
cv2.createTrackbar(title_trackbar_element_type, title_dilatation_window , 0, max_elem, dilatation)
cv2.createTrackbar(title_trackbar_kernel_size, title_dilatation_window , 0, max_kernel_size, dilatation)
erosion(0)
dilatation(0)

cv2.waitKey(0)


