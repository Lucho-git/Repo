import glob
import cv2
from numberExtraction import runExtract

#grabs all jpg images in directory - directory path
files = glob.glob("./*.jpg")


for f in files:
    
    #extracts sign number images, and sign image
    runExtract(f)
  





