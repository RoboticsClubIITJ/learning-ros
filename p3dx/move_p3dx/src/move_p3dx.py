#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('topic_publisher')
pub=rospy.Publisher('/pioneer/cmd_vel',Twist,queue_size=1)
rate=rospy.Rate(2)
twist=Twist()
twist.linear.x=0.5
twist.angular.z=0.5

while not rospy.is_shutdown():
    pub.publish(twist)
    rate.sleep()
