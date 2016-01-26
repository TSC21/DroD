#!/usr/bin/env python

#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

import numpy
import cv2
import hysteresisThreshold  # import the hysteresis module
#from matplotlib import pyplot as plt

img = cv2.imread('test.jpeg')  # read the image i.e single video frame
print hysteresisThreshold.name
hys = hysteresisThreshold.hysteresisThreshold()     # class dec
# hysthreshold module with tunable parameters upperThreshold =100,
# lowerThreshold=50
imgout = hys.hysthreshold(img, 100, 50)
# write out the image to disk
cv2.imwrite('output.png', imgout)
# use matplotlib to automatically view images
#titles = ['Original Image','HysteresisThreshold']
#images = [img, imgout]
# for i in xrange(2):
#	plt.subplot(2,1,i+1),plt.imshow(images[i],'gray')
#       plt.title(titles[i])
#       plt.xticks([]),plt.yticks([])
#       plt.show()
#       plt.imshow(imgages[i],'gray')
