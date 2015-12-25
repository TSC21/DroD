import numpy
import cv2
import hysteresisThreshold
#from matplotlib import pyplot as plt

img = cv2.imread('test.jpeg')
print hysteresisThreshold.name
hys = hysteresisThreshold.hysteresisThreshold()
imgout=hys.hysthreshold(img,100,50)
cv2.imwrite('output.png',imgout)
#titles = ['Original Image','HysteresisThreshold']
#images = [img, imgout]
#for i in xrange(2):
#	plt.subplot(2,1,i+1),plt.imshow(images[i],'gray')
#       plt.title(titles[i])
#       plt.xticks([]),plt.yticks([]) 
#       plt.show()
#       plt.imshow(imgages[i],'gray')
