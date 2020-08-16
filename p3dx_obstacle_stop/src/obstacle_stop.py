#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


def callback(msg):
   pub.publish(twist)
   a=msg.ranges[360]
   if a>1:
     twist.linear.x=0.3
   else:
     twist.linear.x=0.0


rospy.init_node('obstacle')
pub=rospy.Publisher('/pioneer/cmd_vel',Twist,queue_size=1)
twist=Twist()
sub=rospy.Subscriber('/base_scan',LaserScan,callback)

rospy.spin()
