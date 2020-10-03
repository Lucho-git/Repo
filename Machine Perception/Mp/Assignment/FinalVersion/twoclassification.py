import glob
import cv2
import sys
import numpy as np
import itertools as it

#grabs training set of images
files = glob.glob("./Digits/original/*.jpg")

# load training digits, label them appropriately
def load_digits(imglist):
    digits = []
    labels = []

    #label training set based on filename
    for img in files[0:]:
        digits_img = cv2.imread(img, 0)

        if('Zero' in img):
            digits.append(digits_img)
            labels.append(0)
        elif('One' in img):
            digits.append(digits_img)    
            labels.append(1)        
        elif('Two' in img):
            digits.append(digits_img)    
            labels.append(2)       
        elif('Three' in img):
            digits.append(digits_img)    
            labels.append(3)       
        elif('Four' in img):
            digits.append(digits_img)    
            labels.append(4)       
        elif('Five' in img):
            digits.append(digits_img)    
            labels.append(5)       
        elif('Six' in img):
            digits.append(digits_img) 
            digits_img = cv2.resize(digits_img,(28,40))   
            labels.append(6)       
        elif('Seven' in img):
            digits.append(digits_img)   
            digits_img = cv2.resize(digits_img,(28,40)) 
            labels.append(7)       
        elif('Eight' in img):
            digits.append(digits_img)   
            digits_img = cv2.resize(digits_img,(28,40)) 
            labels.append(8)       
        elif('Nine' in img):
            print(type(digits_img))
            digits.append(digits_img)   
            digits_img = cv2.resize(digits_img,(28,40)) 
            labels.append(9)  
        elif('Left' in img):
            print(type(digits_img))
            labels.append(13)  
            digits_img = cv2.resize(digits_img,(28,40))
            digits.append(digits_img)
        elif('Right' in img):
            labels.append(14)
            digits_img = cv2.resize(digits_img,(28,40))
            digits.append(digits_img)



    digits = np.array(digits)
    labels = np.array(labels)
    return digits, labels


#initialize svm with default values, that will be used to classify the numbers
def svmInit(C=1, gamma=0.50625):
  model = cv2.ml.SVM_create()
  model.setGamma(gamma)
  model.setC(C)
  model.setKernel(cv2.ml.SVM_RBF)
  model.setType(cv2.ml.SVM_C_SVC)
  return model

#train svm on training set
def svmTrain(model, samples, responses):
  model.train(samples, cv2.ml.ROW_SAMPLE, responses)
  return model

#runs the svm predictions algorithm
def svmEvaluate(model, samples):
    #predictions = svmPredict(model, samples)
    predictions = model.predict(samples)[1].ravel()
    print("Predictions: " + str(predictions))

    return predictions


#initializes hog_descriptor values, used for running svm
def get_hog() : 
    winSize = (28,40)
    blockSize = (16,16)
    blockStride = (4,4)
    cellSize = (16,16)
    nbins = 9
    derivAperture = 1
    winSigma = -1.
    histogramNormType = 0
    L2HysThreshold = 0.2
    gammaCorrection = 1
    nlevels = 64
    signedGradient = True

    hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,histogramNormType,L2HysThreshold,gammaCorrection,nlevels, signedGradient)

    return hog
    affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR


#Does all initialization and setup/training
def runSetup():

    print('Loading digits from digits.png ... ')
    # Load data.
    digits, labels = load_digits('digits.png')

    #customTrain()


    print('Shuffle data ... ')
    # Shuffle data
    rand = np.random.RandomState(10)
    shuffle = rand.permutation(len(digits))
    digits, labels = digits[shuffle], labels[shuffle]
    
    
    print('Defining HoG parameters ...')
    # HoG feature descriptor
    hog = get_hog();

    print('Calculating HoG descriptor for every training image ... ')
    hog_descriptors = []
    for img in digits:
        #print(img.shape)
        hog_descriptors.append(hog.compute(img))
    hog_descriptors = np.squeeze(hog_descriptors)

    
    digits_train = digits
    labels_train = labels
    hog_descriptors_train = hog_descriptors

    digits_test = None
    labels_test = None
    

    print('Training SVM model ...')
    model = svmInit()
    svmTrain(model, hog_descriptors_train, labels_train)

    return model

#pass in numbers to be evaluated by model, returns predicted number results
def evaluateNumbers(model, intake):


    retlist = []
    for numbers in intake:
        num_descriptors = []
        hog = get_hog()
        #cv2.imshow('anything',numbers)
        #cv2.waitKey(0)
        for num in numbers:

            #print(num.shape)
            num = cv2.resize(num,(28,40))


            num_descriptors.append(hog.compute(num))
        num_descriptors = np.squeeze(num_descriptors)

        print('Evaluating model ... ')
        predictions = svmEvaluate(model, num_descriptors)
        numlist = []
        for p in predictions:
            p = int(p)
            numlist.append(p)
        retlist.append(numlist)

    return retlist

     
    


