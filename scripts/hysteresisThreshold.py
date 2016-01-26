#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

import cv2
import numpy

name = 'HysteresisThreshold'

class HysteresisThreshold():

    def hysThreshold(self, image, upperThreshold, lowerThreshold):                                                              #main threshold function
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                                                                     #convert into gray scale for intensity access
        ret, binaryImage = cv2.threshold(grayImage, upperThreshold, 255, cv2.THRESH_BINARY)                                     #openCV binary thresholding function
        height, width = binaryImage.shape						                                                                #obtain width and height from grayscale image
        for x in range(0, width):						                                                                        #scan through all pixels
            for y in range(0, height):					                                                                        #record intesity value
                if binaryImage[y,x] == 255:					                                                                    #if it is white
                    binaryImage = self.__hysConnect(x, y, width, height, lowerThreshold, binaryImage, grayImage)                # N8 neighborhood function
        return binaryImage								                                                                        #output edited image

    def __hysConnect(self, x, y, width, height, lowerThreshold, binaryImage, grayImage):				                        #private class
        binaryImageCopy = numpy.array(binaryImage)
        for x1 in range(x-1, x+2):						                                                                        #scan N8 pixels
            for y1 in range(y-1, y+2):
                if x1 < width and y1 < height and x1 >= 0 and y1 >= 0 and x1 != x and y1 != y:
                    if binaryImage[y1,x1]!=255 and grayImage[y1,x1]>=lowerThreshold:					                        #make sure it isn't white and if threshold>=lthres
                        binaryImageCopy[y1,x1] = 255		                                                                    #make it white
                        binaryImageCopy = self.__hysConnect(x1, y1, width, height, lowerThreshold, binaryImageCopy, grayImage)
        return binaryImageCopy
