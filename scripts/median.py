#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

import cv2
import rospy
import numpy as np

name = 'median'


class Median:

    def getMedian(self, buffer):

        # each frame is flattened into a 1 dimensional array to look like : [B1, G1, R1, B2, G2, R2, B3, G3, R3,..........] using ravel()
        # all frames are stacked to form one 2 dimensional array : [ [1B1, 1G1, 1R1, 1B2, 1G2, 1R2, 1B3, 1G3, 1R3,..........],
        #                                                           [2B1, 2G1, 2R1, 2B2, 2G2, 2R2, 2B3, 2G3, 2R3,..........],
        #                                                           [3B1, 3G1, 3R1, 3B2, 3G2, 3R2, 3B3, 3G3, 3R3,..........],
        #                                                             ...........................................
        #                                                           [99B1, 99G1, 99R1, 99B2, 99G2, 99R2, 99B3, 99G3, 99R3,..........] ] using numpy.vstack()

        # refer to
        # http://stackoverflow.com/questions/16135677/efficient-way-to-find-median-value-of-a-number-of-rgb-images

        lap1 = cv2.getTickCount()  # measuring performance
        stackedFlattened = np.vstack((frame.ravel() for frame in buffer))
        firstFrame = buffer[0]
        del buffer

        # np.median() is used to get the median of each column in the 2
        # dimensional array

        lap2 = cv2.getTickCount()
        medianImageFlattened = np.median(stackedFlattened, axis=0)
        del stackedFlattened

        # now we have a one dimensional array of only medians : [MB1, MG1, MR1, MB2, MG2, MR2, MB3, MG3, MR3,...........]
        # it is reshaped to form the image

        lap3 = cv2.getTickCount()
        medianImage = np.uint8(
            medianImageFlattened.reshape(firstFrame.shape))
        del medianImageFlattened

        lap4 = cv2.getTickCount()

        t1 = (lap2 - lap1) / cv2.getTickFrequency()
        t2 = (lap3 - lap2) / cv2.getTickFrequency()
        t3 = (lap4 - lap3) / cv2.getTickFrequency()

        rospy.loginfo(
            "\nTime taken by vstack(ravel()): \t%f sec\nTime taken by numpy.median: \t%f sec\nTime taken by reshape: \t\t%f sec", t1, t2, t3)
        return medianImage
