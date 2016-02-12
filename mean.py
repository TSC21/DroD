import cv2
import numpy

name = 'mean'

class Mean:

    def getMean(self, buffer):
        
        stackedFlattened = numpy.vstack((frame.ravel() for frame in buffer)) 
        firstFrame = buffer[0]
        del buffer
        
        meanImageFlattened = numpy.mean(stackedFlattened, axis = 0)
        del stackedFlattened
        
        meanImage = numpy.uint8(meanImageFlattened.reshape(firstFrame.shape))
        del meanImageFlattened

        return meanImage
