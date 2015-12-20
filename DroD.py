import numpy
import cv2
import LearningPhase
import DetectionPhase

video = cv2.VideoCapture('D:\Stuff\Drowning Detection\drowning.mp4')

w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
fc = video.get(cv2.CAP_PROP_FRAME_COUNT)

print 'Resolution = ', w, 'x', h, ' and number of frames = ', fc

nSamples = 400 #number of samples to be considered for learning phase

print LearningPhase.name
learner = LearningPhase.LearningPhase()

learner.learn(video, nSamples)
initialBackgroundClusterCenters = learner.getInitialBackgroundClusterCenters()

video.open('D:\Stuff\Drowning Detection\drowning.mp4')
video.set(cv2.CAP_PROP_POS_FRAMES, nSamples)

print DetectionPhase.name
detector = DetectionPhase.DetectionPhase()
detector.detect(video, initialBackgroundClusterCenters)

