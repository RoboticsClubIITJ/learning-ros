#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def callback(msg):
   print(msg.pose.pose.position)
   twist.linear.x=0.5
   twist.angular.z=0.5
   pub.publish(twist)

rospy.init_node('topic_publisher')
pub=rospy.Publisher('/pioneer/cmd_vel',Twist,queue_size=1)
twist=Twist()
sub=rospy.Subscriber('/odom',Odometry,callback)

rospy.spin()
