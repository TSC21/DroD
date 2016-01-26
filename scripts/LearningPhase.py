#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

import cv2
import numpy
import median
import blockBasedModel

name = 'LearningPhase'

class LearningPhase:

    def learn(self, video, nSamples):

        retVal, firstFrame = video.read()
        resizedFirstFrame = cv2.resize(firstFrame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_LINEAR)

        buffer = [resizedFirstFrame] #creating an array of images

        cv2.namedWindow('video')
        for count in xrange(nSamples-1): #considering nSamples frames to find initial background
            retVal, frame = video.read()
            if (not retVal) or (cv2.waitKey(1)==27): #break if frame is not read
                break

            resizedFrame = cv2.resize(frame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_LINEAR) #resize each frame

            buffer.append(resizedFrame) #buffer is made by appending nSamples-1 frames to the initial first frame

            cv2.imshow('video', resizedFrame)

        cv2.destroyWindow('video')
        video.release()

        print median.name
        medianObj = median.Median()
        initialBackground = medianObj.getMedian(buffer) #function gives median of buffer

        print blockBasedModel.name
        blockBasedModelObj = blockBasedModel.BlockBasedModel()
        blockBasedInitialBackground = blockBasedModelObj.getBlockBasedModel(initialBackground, 40) #takes image, size of square block, returns k-means clustered-block based-model
        self.initialBackgroundClusterCenters = blockBasedModelObj.getClusterCenters()

        cv2.imshow('m', initialBackground)
        cv2.imshow('cm', blockBasedInitialBackground)
        cv2.waitKey(0)

        cv2.destroyAllWindows()

        return blockBasedInitialBackground

    def getInitialBackgroundClusterCenters(self):
        return self.initialBackgroundClusterCenters
