import glob
import cv2
from twoclassification import runSetup
from twoclassification import evaluateNumbers
from twonumberExtraction import runExtract

#grabs all jpg images in directory - directory path  home/student/test/task1
files = glob.glob("./val_DirectionalSignage/*.jpg")

#used when creating filenames to write to
count = 1

if(len(files) < 1):
    print("No Images Detected")

else:

    #trains svm algorithm on training set
    model = runSetup()

    #loops through each image to perform operations
    for f in files:
    
        #extracts sign number images, and sign image

        numbers,signpost,valid = runExtract(f)

        #writes signpost detected to file
        cv2.imwrite('./output/Task2/DetectedArea'+str(count)+'.jpg',signpost)

        if(valid):
            ret = evaluateNumbers(model,numbers)
            for x in ret:
                string = str(x)
                string = string.replace('13','Left')
                string = string.replace('14','Right')

                f = open("./output/Task2/BuildingList"+str(count)+".txt", "a")
                f.write("Building " + str(string) + '\n')
      
            count +=1
