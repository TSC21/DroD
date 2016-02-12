#!/usr/bin/env python

#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

import cv2
import hysteresisThreshold  # import the hysteresis module
#from matplotlib import pyplot as plt

img = cv2.imread('../test_set/test.jpeg')  # read the image i.e single video frame
print hysteresisThreshold.name
hys = hysteresisThreshold.HysteresisThreshold()     # class dec
# hysthreshold module with tunable parameters upperThreshold =100,
# lowerThreshold=50
imgout = hys.hysThreshold(img, 100, 50)
# write out the image to disk
cv2.imwrite('../test_set/output/output.png', imgout)
# use matplotlib to automatically view images
#titles = ['Original Image','HysteresisThreshold']
#images = [img, imgout]
# for i in xrange(2):
#	plt.subplot(2,1,i+1),plt.imshow(images[i],'gray')
#       plt.title(titles[i])
#       plt.xticks([]),plt.yticks([])
#       plt.show()
#       plt.imshow(imgages[i],'gray')
