import cv2
import numpy as np

name = 'hysteresisThreshold'

class hysteresisThreshold():

	def hysthreshold(self,img,uThres,lThres): 					# main threshold function
		
		gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		        #convert into gray scale for intensity access
		ret,imgout = cv2.threshold(gray_image,uThres,255,cv2.THRESH_BINARY)	# openCV binary thresholding function
		height, width = imgout.shape
		for x in range (0,width-1):	
			for y in range (0,height-1):
				value = imgout[y,x]
				if value == 255:
					self.__hysconnect(x,y,width,height,lThres,imgout) # N8 neighborhood function
		return imgout

	def __hysconnect(self,x,y,width,height,lThres,imgout):				# private class
		for x1 in range (x-1,x+1):
			for y1 in range (y-1,y+1): 
				if x1 < width or y1 < height or x1 >= 0 or y1 >= 0 or x1 != x or y1 != y:
					value = imgout[y1,x1]
					if value!=255:
						if value>=lThres:
							imgout[y1,x1] == 255
							self.__hysconnect(x1,y1,width.height,lThres,imgout)
						else:
							imgout[y1,x1] == 0
