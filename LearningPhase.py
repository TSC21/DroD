import cv2
import numpy
import median

video = cv2.VideoCapture('D:\Stuff\Drowning Detection\drowning.mp4')

retVal, firstFrame = video.read()

buffer = [firstFrame] #creating an array of images

cv2.namedWindow('video')
for count in xrange(99): #considering 100 frames to find initial background
    retVal, frame = video.read()
    if (not retVal) or (cv2.waitKey(1)==27): #break if frame is not read
        break
    
    buffer.append(frame) #buffer is made by appending 99 frames to the initial first frame
    
    cv2.imshow('video', frame)

cv2.destroyWindow('video')
video.release()

print median.name
medianImage = median.getMedian(buffer) #function gives median of buffer

cv2.imshow('m', medianImage)
cv2.waitKey(0)

cv2.destroyAllWindows()
