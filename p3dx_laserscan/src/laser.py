#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
   print(msg.ranges)

rospy.init_node('topic_subscriber')
syb=rospy.Subscriber('/base_scan',LaserScan,callback)
rospy.spin()
