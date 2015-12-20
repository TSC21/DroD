import cv2
import numpy
import colorDiscrepancy

name = 'DetectionPhase'

class DetectionPhase:
    
    def detect(self, video, initialBackgroundClusterCenters):
        cv2.namedWindow('DifferenceImage')

        print colorDiscrepancy.name
        colorDiscrepancyObj = colorDiscrepancy.ColorDiscrepancy()

        backgroundClusterCenters = initialBackgroundClusterCenters

        while(video.isOpened()):
            retVal, frame = video.read()
            if (not retVal) or (cv2.waitKey(1)==27): #break if frame is not read
                break
    
            resizedFrame = cv2.resize(frame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_LINEAR) #resize each frame

            differenceImage = colorDiscrepancyObj.getColorDiscrepancy(resizedFrame, backgroundClusterCenters, 40)

            cv2.imshow('DifferenceImage', differenceImage)

        cv2.destroyWindow('DifferenceImage')
        video.release()
