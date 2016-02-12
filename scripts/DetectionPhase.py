#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

import cv2
import rospy
import colorDiscrepancy

name = 'DetectionPhase'


class DetectionPhase:

    def detect(self, video, initialBackgroundClusterCenters):
        cv2.namedWindow('DifferenceImage')
        cv2.namedWindow('SegmentedImage')
        cv2.namedWindow('UpdatedBackground')

        rospy.loginfo("Computing %s", colorDiscrepancy.name)
        colorDiscrepancyObj = colorDiscrepancy.ColorDiscrepancy()

        backgroundClusterCenters = initialBackgroundClusterCenters

        buffer = []  # creating an array of images

        meanObj = mean.Mean()

        blockBasedModelObj = blockBasedModel.BlockBasedModel()
        hysteresisThresholdObj = hysteresisThreshold.HysteresisThreshold()

        while(video.isOpened()):
            retVal, frame = video.read()
            if (not retVal) or (cv2.waitKey(1) == 27):  # break if frame is not read
                break

            resizedFrame = cv2.resize(
                frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)  # resize each frame

            differenceImage = colorDiscrepancyObj.getColorDiscrepancy(
                resizedFrame, backgroundClusterCenters, 40)

            segmentedImage = hysteresisThresholdObj.hysThreshold(
                differenceImage, 127, 127)

            buffer.append(resizedFrame)
            if(len(buffer) > 10):
                buffer.pop(0)
            updatedBackground = meanObj.getMean(buffer)

            blockBasedUpdatedBackground = blockBasedModelObj.getBlockBasedModel(
                updatedBackground, 40)
            backgroundClusterCenters = blockBasedModelObj.getClusterCenters()

            cv2.imshow('DifferenceImage', differenceImage)
            cv2.waitKey(1)
            cv2.imshow('SegmentedImage', segmentedImage)
            cv2.waitKey(1)
            cv2.imshow('UpdatedBackground', updatedBackground)
            cv2.waitKey(1)

        cv2.destroyWindow('DifferenceImage')
        cv2.destroyWindow('SegmentedImage')
        cv2.destroyWindow('UpdatedBackground')
        cv2.destroyAllWindows()
        video.release()
