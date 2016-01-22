import cv2
import numpy

name = 'ColorDiscrepancy'

class ColorDiscrepancy:

    def getColorDiscrepancy(self, currentFrame, backgroundClusterCenters, s):
        bgcBYXa = cv2.copyMakeBorder(backgroundClusterCenters[:,:,0], 1, 1, 1, 1, cv2.BORDER_CONSTANT, value = [0, 0, 0])
        bgcBYXb = cv2.copyMakeBorder(backgroundClusterCenters[:,:,1], 1, 1, 1, 1, cv2.BORDER_CONSTANT, value = [0, 0, 0])
        diff00a = currentFrame - cv2.resize(bgcBYXa[1:10, 1:17, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff00b = currentFrame - cv2.resize(bgcBYXb[1:10, 1:17, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff01a = currentFrame - cv2.resize(bgcBYXa[1:10, 2:18, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff01b = currentFrame - cv2.resize(bgcBYXb[1:10, 2:18, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff10a = currentFrame - cv2.resize(bgcBYXa[2:11, 1:17, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff10b = currentFrame - cv2.resize(bgcBYXb[2:11, 1:17, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff11a = currentFrame - cv2.resize(bgcBYXa[2:11, 2:18, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff11b = currentFrame - cv2.resize(bgcBYXb[2:11, 2:18, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff0m1a = currentFrame - cv2.resize(bgcBYXa[1:10, 0:16, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff0m1b = currentFrame - cv2.resize(bgcBYXb[1:10, 0:16, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diffm10a = currentFrame - cv2.resize(bgcBYXa[0:9, 1:17, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diffm10b = currentFrame - cv2.resize(bgcBYXb[0:9, 1:17, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff1m1a = currentFrame - cv2.resize(bgcBYXa[2:11, 0:16, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diff1m1b = currentFrame - cv2.resize(bgcBYXb[2:11, 0:16, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diffm11a = currentFrame - cv2.resize(bgcBYXa[0:9, 2:18, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diffm11b = currentFrame - cv2.resize(bgcBYXb[0:9, 2:18, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diffm1m1a = currentFrame - cv2.resize(bgcBYXa[0:9, 0:16, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)
        diffm1m1b = currentFrame - cv2.resize(bgcBYXb[0:9, 0:16, :], None, fx = s, fy = s, interpolation = cv2.INTER_NEAREST)

        stackedFlattenedDifferences = numpy.vstack([diff00a.ravel(), diff00b.ravel(), diff01a.ravel(), diff01b.ravel(), diff10a.ravel(), diff10b.ravel(), diff11a.ravel(), diff11b.ravel(), diff0m1a.ravel(), 
                                                    diff0m1b.ravel(), diffm10a.ravel(), diffm10b.ravel(), diff1m1a.ravel(), diff1m1b.ravel(), diffm11a.ravel(), diffm11b.ravel(), diffm1m1a.ravel(), diffm1m1b.ravel()])
        
        differenceImageFlattened = numpy.min(numpy.absolute(stackedFlattenedDifferences), axis = 0)
        del stackedFlattenedDifferences
        differenceImage = numpy.uint8(differenceImageFlattened.reshape(currentFrame.shape))
        del differenceImageFlattened
        return differenceImage
