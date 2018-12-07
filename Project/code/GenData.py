# GenData.py
import numpy as np
import cv2
import TrainAndTest as tr

# module level variables ##########################################################################
MIN_CONTOUR_AREA = 100
MAX_CONTOUR_AREA = 1000
modeAppend=1
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30
def Train(img):
    imgTrainingNumbers = cv2.imread(img)            # read in training numbers image

    if imgTrainingNumbers is None:                          # if image was not read successfully
        print ("error: image not read from file \n\n")        # print error message to std out
        return                                              # and exit function (which exits program)
    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_RGB2GRAY)          # get grayscale image
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                        # blur
    kernel = np.ones((1, 1), np.uint8)
    imgBlurred = cv2.dilate(imgBlurred, kernel, iterations=1)
    imgBlurred = cv2.erode(imgBlurred, kernel, iterations=1)
                                                        # filter image from grayscale to black and white
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY,                # invert so foreground will be white, background will be black
                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
                                      2)                                    # constant subtracted from the mean or weighted mean

    cv2.imshow("imgThresh", imgThresh)      # show threshold image for reference

    imgThreshCopy = imgThresh.copy()        # make a copy of the thresh image, this in necessary b/c findContours modifies the image

    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,        # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                 cv2.RETR_LIST,                 # retrieve the outermost contours only
                                                 cv2.CHAIN_APPROX_SIMPLE)	           # compress horizontal, vertical, and diagonal segments and leave only their end points

														                        # declare empty numpy array, we will use this to write to file later
																				   # zero rows, enough cols to hold all image data
    npaFlattenedImages =  np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

    intClassifications = []         # declare empty classifications list, this will be our list of how we are classifying our chars from user input, we will write to file at the end

                                    # possible chars we are interested in are digits 0 through 9, put these in list intValidChars
    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'),
                     ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),
                     ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'), ord('R'), ord('S'), ord('T'),
                     ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z'), ord('+'), ord('*'), ord('/'), ord('-'),
					 ord('('), ord(')'), ord('x'), ord('y'), ord('z'), ord('a'), ord('b'), ord('c')]
    allContoursWithData=[]
    for npaContour in npaContours:                             	                        # for each contour
        contourWithData = tr.ContourWithData()                                          # instantiate a contour with data object
        contourWithData.npaContour = npaContour                                         # assign contour to contour with data
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     # get the bounding rect
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           # calculate the contour area
        allContoursWithData.append(contourWithData)                                     # add contour with data object to list of all contours with data

    print(allContoursWithData)
    validContoursWithData=[]
    for contourWithData in allContoursWithData:                 # for all contours
        if contourWithData.checkIfContourIsValid():             # check if valid
            validContoursWithData.append(contourWithData)       # if so, append to valid contour list
    validContoursWithData=tr.adjustOverlaps(validContoursWithData)
#    print(validContoursWithData)
    for npaContour in validContoursWithData:                         # for each contour
													# draw rectangle around each contour as we ask user for input
        cv2.rectangle(imgTrainingNumbers,           # draw rectangle on original training image
                      (npaContour.intRectX, npaContour.intRectY),                 # upper left corner
                      (npaContour.intRectX+npaContour.intRectWidth,npaContour.intRectY+npaContour.intRectHeight),        # lower right corner
                      (0, 255, 0),                  # green
                      2)                            # thickness

        imgROI = imgThresh[npaContour.intRectY:npaContour.intRectY+npaContour.intRectHeight, npaContour.intRectX:npaContour.intRectX+npaContour.intRectWidth]                                  # crop char out of threshold image
        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))     # resize image, this will be more consistent for recognition and storage

        cv2.imshow("imgROI", imgROI)                    # show cropped out char for reference
        cv2.imshow("imgROIResized", imgROIResized)      # show resized image for reference
        cv2.imshow("training_numbers.png", imgTrainingNumbers)      # show training numbers image, this will now have red rectangles drawn on it

        intChar = cv2.waitKey(0)                     # get key press

        if intChar == 27:                   # if esc key was pressed
            cv2.destroyAllWindows()                      # exit program
            return
        elif intChar in intValidChars:      # else if the char is in the list of chars we are looking for . . .

            intClassifications.append(intChar)                                                # append classification char to integer list of chars (we will convert to float later before writing to file)

            npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image to 1d numpy array so we can write to file later
            npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)                    # add current flattened impage numpy array to list of flattened image numpy arrays
        cv2.rectangle(imgTrainingNumbers,           # draw rectangle on original training image
                      (npaContour.intRectX, npaContour.intRectY),                 # upper left corner
                      (npaContour.intRectX+npaContour.intRectWidth,npaContour.intRectY+npaContour.intRectHeight),        # lower right corner
                      (0, 0, 255),                  # red
                      2)                            # thickness
    fltClassifications = np.array(intClassifications, np.float32)                   # convert classifications list of ints to numpy array of floats

    npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))   # flatten numpy array of floats to 1d so we can write to file later

    print ("\n\ntraining complete !!\n")
    if (modeAppend==1):
	    f1=open("learned/classifications.txt",'ab')
	    np.savetxt(f1, npaClassifications)           # write flattened images to file
	    f1.close()
	    f2=open("learned/flattened_images.txt", 'ab')
	    np.savetxt(f2, npaFlattenedImages)
	    f2.close()
    else:
	    np.savetxt("learned/classifications.txt", npaClassifications)           # write flattened images to file
	    np.savetxt("learned/flattened_images.txt", npaFlattenedImages)          #
    cv2.destroyAllWindows()             # remove windows from memory

    return

###################################################################################################
img="../images/training/"
#for i in range(7):
#	Train(img+"all"+str(i+1)+".png")
#for i in range(4):
#	Train(img+"numbers"+str(i+1)+".png")
#for i in range(2):
#	Train(img+"symbols"+str(i+1)+".png")	
#Train(img+"numbers2.png")
#Train(img+"symbols2.png")