import numpy
import cv2

name = 'blockBasedModel'

def getBlockBasedModel(image, s): #returns k-means clustered-block based-model
    height, width, nChannels = image.shape
    m = width/s #number of horizontal blocks, m as in the paper
    n = height/s #number of vertical blocks, n as in the paper

    #split image into mxn blocks of size sxs each
    blocks = numpy.array([[image[r*s:(r+1)*s, c*s:(c+1)*s] for c in xrange(m)] for r in xrange(n)]) #split into n arrays, each made of m arrays, each of which is a block of size (sxsxnChannels)
    bS = blocks.shape #(n, m, s, s, nChannels)
    aBS = ((bS[0]*bS[1]), bS[2], bS[3], bS[4]) #aligned block shape
    alignedBlocks = blocks.reshape(aBS) #(nxm, s, s, nChannels), array of nxm blocks, all aligned
    
    #k-means cluster each part
    clusteredAlignedBlocks = numpy.array([getClusteredImage(block) for block in alignedBlocks]) #finding cluster for each block and aligning the clusters(same size as block) 

    #combine parts
    clusteredBlocks = clusteredAlignedBlocks.reshape(bS) #reshaped to (n, m, s, s, nChannels)
    image = numpy.vstack([numpy.hstack([block for block in clusteredBlocks[r, :]]) for r in xrange(n)]) #merged into one image by stacking horizontally, then vertically
    return image

def getClusteredImage(image): #returns k-means clustered image
    height, width, nChannels = image.shape 

    stackedImage = image.reshape((height*width, nChannels)) #data needs to be of shape (A, B), where each data[a,:] is a point to be clustered. Our points are colors
    stackedImage = numpy.float32(stackedImage)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(stackedImage, 2, criteria, 10, cv2.KMEANS_RANDOM_CENTERS) #parameter values need to be tuned for optimum performance

    #k centers(of shape nChannels) are generated. Each pixel is closest to one of the centers. That data is in the label array. Each pixel is set to its matching center in next line
    #refer to http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html
    stackedImage = numpy.array([center[x] for x in label.ravel()])

    image = stackedImage.reshape((height, width, nChannels)) #reshape into 2D image
    image = numpy.uint8(image)
    return image
