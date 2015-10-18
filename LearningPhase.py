import cv2
import numpy
import median

video = cv2.VideoCapture('D:\Stuff\Drowning Detection\drowning.mp4')

retVal, firstFrame = video.read()
resizedFirstFrame = cv2.resize(firstFrame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_LINEAR)

buffer = [resizedFirstFrame] #creating an array of images

cv2.namedWindow('video')
for count in xrange(99): #considering 100 frames to find initial background
    retVal, frame = video.read()
    if (not retVal) or (cv2.waitKey(1)==27): #break if frame is not read
        break
    
    resizedFrame = cv2.resize(frame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_LINEAR) #resize each frame
    buffer.append(resizedFrame) #buffer is made by appending 99 frames to the initial first frame
    
    cv2.imshow('video', resizedFrame)

cv2.destroyWindow('video')
video.release()

print median.name
medianImage = median.getMedian(buffer) #function gives median of buffer

cv2.imshow('m', medianImage)
cv2.waitKey(0)

cv2.destroyAllWindows()
