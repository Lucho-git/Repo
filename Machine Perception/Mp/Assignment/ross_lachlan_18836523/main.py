import glob
import cv2
from classification import runSetup
from classification import evaluateNumbers
from numberExtraction import runExtract

#grabs all jpg images in directory - directory path  home/student/test/task1
files = glob.glob("/home/student/test/task1/*.jpg")

#used when creating filenames to write to
count = 1

f = open("./output/Task2/BuildingList"+str(count)+".txt", "w+")
f.close()

if(len(files) < 1):
    print("No Images Detected")

else:

    #trains svm algorithm on training set
    model = runSetup()

    #loops through each image to perform operations
    for f in files:
    
        #extracts sign number images, and sign image
        retnum,sign,valid = runExtract(f)
        if(valid):

            #runs number images with classifier, which returns predicted numbers
            ret = evaluateNumbers(model, retnum)

            #writes detected building numbers to file
            f = open("./output/Task1/Building"+str(count)+".txt", "a")
            f.write("Building " + str(ret))

            #writes image sign detected to file
            cv2.imwrite('./output/Task1/DetectedArea'+str(count)+'.jpg',sign)
            
            count += 1





