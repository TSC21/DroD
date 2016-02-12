#!/usr/bin/env python

#
# Copyright (c) 2016, DroD Team.
# All rights reserved.
#

from __future__ import print_function

import os
import sys
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
        self.test_set_path = self.pkg_path + rospy.get_param(
            '~test_video', '/test_set/DrowningvSwimming_(Edited).mp4')

        # parameters:
        # live stream or video test? True if the latest
        self.is_testing = bool(rospy.get_param('~isatest', True))
        # number of samples to be considered for learning phase
        self.num_of_samples = rospy.get_param('~num_of_samples', 400)

        if self.is_testing:
            rospy.loginfo('Loaded video to test: %s', self.test_set_path)
            self.video_src = cv2.VideoCapture(self.test_set_path)

            width = self.video_src.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self.video_src.get(cv2.CAP_PROP_FRAME_HEIGHT)
            frame_count = self.video_src.get(cv2.CAP_PROP_FRAME_COUNT)

            rospy.loginfo('Image resolution: %dx%d', width, height)
            rospy.loginfo('Number of frames: %d', frame_count)

        else:
            rospy.loginfo(
                'Getting data from USB camera on topic "/camera/image_raw"')
            self.image_sub = ropy.Subscriber(
                "/camera/image_raw", sensor_msgs.msg.Image, self.camera_callback)

        rospy.logdebug(lp.name)
        rospy.logdebug(dp.name)

        self.learner = lp.LearningPhase()
        self.detector = dp.DetectionPhase()

    def camera_callback(self):
        '''
        function to get data from camera
        '''
        try:
            img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        height, width, channels = img.shape
        rospy.logdebug('Image resolution: %dx%d', width, height)

        self.node_routine(img)

    def node_routine(self, video_src):
        '''
        function to launch the pipeline routine
        '''
        self.learner.learn(video_src, self.num_of_samples)

        if self.is_testing:
            video_src.open(self.test_set_path)
            video_src.set(cv2.CAP_PROP_POS_FRAMES, self.num_of_samples)
            self.detector.detect(
                video_src, self.learner.getInitialBackgroundClusterCenters())
        else:
            self.detector.detect(
                video_src, self.learner.getInitialBackgroundClusterCenters())

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
