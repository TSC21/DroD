#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

import cv2
import numpy as np

name = 'mean'


class Mean:

    def getMean(self, buffer):
        stackedFlattened = np.vstack((frame.ravel() for frame in buffer))
        firstFrame = buffer[0]
        del buffer

        meanImageFlattened = np.mean(stackedFlattened, axis=0)
        del stackedFlattened

        meanImage = np.uint8(meanImageFlattened.reshape(firstFrame.shape))
        del meanImageFlattened

        return meanImage
