#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

import numpy as np
import cv2

name = 'blockBasedModel'


class BlockBasedModel:

    # returns k-means clustered-block based-model
    def getBlockBasedModel(self, image, s):
        height, width, nChannels = image.shape
        m = width / s  # number of horizontal blocks, m as in the paper
        n = height / s  # number of vertical blocks, n as in the paper

        # split image into mxn blocks of size sxs each
        # split into n arrays, each made of m arrays, each of which is a block
        # of size (sxsxnChannels)
        blocks = np.array([[image[r * s:(r + 1) * s, c * s:(c + 1) * s]
                               for c in xrange(m)] for r in xrange(n)])
        bS = blocks.shape  # (n, m, s, s, nChannels)
        aBS = ((bS[0] * bS[1]), bS[2], bS[3], bS[4])  # aligned block shape
        # (nxm, s, s, nChannels), array of nxm blocks, all aligned
        alignedBlocks = blocks.reshape(aBS)

        # k-means cluster each part
        # initializing cluster centers
        self.clusterCenters = [np.zeros([2, nChannels])]
        # finding cluster for each block and aligning the clusters(same size as
        # block)
        clusteredAlignedBlocks = np.array(
            [self.getClusteredImage(block) for block in alignedBlocks])

        # reshape cluster centers to nxm
        self.clusterCenters.pop(0)
        self.clusterCenters = np.array(self.clusterCenters)
        self.clusterCenters = self.clusterCenters.reshape([n, m, 2, nChannels])

        # combine parts
        clusteredBlocks = clusteredAlignedBlocks.reshape(
            bS)  # reshaped to (n, m, s, s, nChannels)
        # merged into one image by stacking horizontally, then vertically
        image = np.vstack(
            [np.hstack([block for block in clusteredBlocks[r, :]]) for r in xrange(n)])
        return image

    def getClusteredImage(self, image):  # returns k-means clustered image
        height, width, nChannels = image.shape

        # data needs to be of shape (A, B), where each data[a,:] is a point to
        # be clustered. Our points are colors
        stackedImage = image.reshape((height * width, nChannels))
        stackedImage = np.float32(stackedImage)

        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        # parameter values need to be tuned for optimum performance
        ret, label, center = cv2.kmeans(
            stackedImage, 2, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # k centers(of shape nChannels) are generated. Each pixel is closest to one of the centers. That data is in the label array. Each pixel is set to its matching center in next line
        # refer to
        # http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html
        stackedImage = np.array([center[x] for x in label.ravel()])
        self.clusterCenters.append(center)

        image = stackedImage.reshape(
            (height, width, nChannels))  # reshape into 2D image
        image = np.uint8(image)
        return image

    def getClusterCenters(self):
        return self.clusterCenters
