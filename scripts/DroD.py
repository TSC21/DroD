#!/usr/bin/env python

#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

from __future__ import print_function

import os
import numpy as np
import LearningPhase as lp
import DetectionPhase as dp
import hysteresisThreshold as ht  # added by Sai

import roslib
roslib.load_manifest('drod')
import rospy
import rospkg

import cv2
import Image
from cv_bridge import CvBridge, CvBridgeError
import sensor_msgs.msg


class DrodNode(object):

    def __init__(self):
    	# ROS node setup
        rospy.init_node('drod')

        # setup bridge between OpenCV and ROS
        self.bridge = CvBridge()

        # test set path setup
        rospack = rospkg.RosPack()
        self.pkg_path = rospack.get_path('drod')
        test_set_path = os.path.join(self.pkg_path, rospy.get_param(
            '~test_video', '/test_set/drowning.mp4'))

        # parameters:
        # live stream or video test? True if the latest
        self.is_testing = rospy.get_param('~isatest', True)
        # number of samples to be considered for learning phase
        self.num_of_samples = rospy.get_param('~num_of_samples', 400)
        # set debug
        self.debug = rospy.get_param('~debug', True)

        if is_testing:
            rospy.loginfo('Loaded video to test: %s', test_set_path)
            self.video_src = cv2.VideoCapture(test_set_path)

            width = video_src.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = video_src.get(cv2.CAP_PROP_FRAME_HEIGHT)
            frame_count = video_src.get(cv2.CAP_PROP_FRAME_COUNT)

            if self.debug:
                rospy.loginfo('Image resolution: %dx%d', width, height)
                rospy.loginfo('Number of frames: %d', frame_count)

            # self.video_src.open(test_set_path)
            # self.video_src.set(cv2.CAP_PROP_POS_FRAMES, self.num_of_samples)

        else:
            rospy.loginfo(
                'Getting data from USB camera on topic "/camera/image_raw"')
            self.image_sub = ropy.Subscriber(
                "/camera/image_raw", sensor_msgs.msg.Image, self.camera_callback)

        if self.debug:
            rospy.loginfo(lp.name)
            rospy.loginfo(dp.name)

        self.learner = lp.LearningPhase()
        self.detector = dp.DetectionPhase()

    def camera_callback(self):
    	try:
            img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        if self.debug:
            height, width, channels = img.shape
            rospy.loginfo('Image resolution: %dx%d', width, height)

        self.node_routine(img)

    def node_routine(self, video_src):
        self.learner.learn(video_src, self.num_of_samples)
        self.detector.detect(video_src, self.learner.getInitialBackgroundClusterCenters())

        ''' Added by Sai
        img = cv2.imread('test.jpeg')
        print hysteresisThreshold.name
        hys = hysteresisThreshold.hysteresisThreshold()
        imgout=hys.hysthreshold(img,100,50)
        cv2.imwrite('output.png',imgout)
        Added by Sai '''


def main(args):
    '''
    main function
    '''
    dn = DrodNode()
    if dn.is_testing:
    	dn.node_routine(dn.video_src)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.logwarn("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
