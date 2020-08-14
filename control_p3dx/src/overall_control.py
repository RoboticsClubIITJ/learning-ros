#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

rospy.init_node('topic_publisher','topic_subscriber')
pub=rospy.Publisher('/pioneer/cmd_vel',Twist,queue_size=1)

rate=rospy.Rate(2)
twist=Twist()

twist.linear.x=0.5
twist.angular.z=0.5

def callback(msg):
   print(msg.pose.pose.position)

while not rospy.is_shutdown():
    pub.publish(twist)
    sub=rospy.Subscriber('/odom',Odometry,callback)
    rate.sleep()

