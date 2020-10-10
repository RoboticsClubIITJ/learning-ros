import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Kill

from turtle_interfaces.msg import TurtleID

class nodeMaker(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.target_x=None
        self.target_y=None
        self.pose_=None
        # self.declare_parameter("catch_closest",True)
        self.catch_closest=True
        self.turtle_list=[]
        self.turtle_sub=self.create_subscription(TurtleID,"turtleID",self.turtleSubsciber,10)
        self.cmd_vel_publisher=self.create_publisher(Twist,"turtle1/cmd_vel",10)
        self.pose_sub=self.create_subscription(Pose,"turtle1/pose",self.callback_pose_sub,10)
        self.controller_loop=self.create_timer(0.01,self.turtle_controller)

    def turtleSubsciber(self,msg):
        self.get_logger().info("I got coordinates")
        self.turtle_list.append(msg)
        if self.target_x==None or self.target_y==None:
            self.target_x=msg.x
            self.target_y=msg.y

    def callback_pose_sub(self,msg):
        self.pose_=msg

    def kill_turtle(self,name):
        client=self.create_client(Kill,"kill")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("waiting for kill...")
        request=Kill.Request()
        request.name=name
        future=client.call_async(request)
        # future.add_done_callback(self.future_callback)

    def findTarget(self):
        min_dist=None
        I=None
        for i in range(len(self.turtle_list)):
            new_diff_x=self.turtle_list[i].x-self.pose_.x
            new_diff_y=self.turtle_list[i].y-self.pose_.y
            new_dist=math.sqrt(new_diff_x**2+new_diff_y**2)
            if min_dist==None:
                min_dist=new_dist
                I=i
            elif new_dist<min_dist:
                self.get_logger().warn("i found an idiot")
                min_dist=new_dist
                I=i
        self.turtle_list[0],self.turtle_list[I]=self.turtle_list[I],self.turtle_list[0]
        self.target_x=self.turtle_list[0].x
        self.target_y=self.turtle_list[0].y


    def turtle_controller(self):
        if self.pose_==None or self.target_x==None or self.target_y==None:
            self.get_logger().info("i am null")
            return
        if self.catch_closest:
            self.findTarget()
        diff_x=self.target_x-self.pose_.x
        diff_y=self.target_y-self.pose_.y
        target_theta=math.atan2(diff_y,diff_x)
        diff_theta=target_theta-self.pose_.theta
        dist=math.sqrt(diff_x**2+diff_y**2)
        cmd_vel=Twist()
        # if self.get_parameter("catch_closest")=="True":
        # if self.catch_closest:
        #     i=0
        #     while i<len(self.turtle_list):
        #         try:
        #             new_diff_x=self.turtle_list[i].x-self.pose_.x
        #             new_diff_y=self.turtle_list[i].y-self.pose_.y
        #             new_dist=math.sqrt(new_diff_x**2+new_diff_y**2)
        #             if new_dist<0.5:
        #                 self.kill_turtle(self.turtle_list[i].name)
        #                 self.turtle_list.pop(i)
        #                 i-=1
        #             if new_dist<dist:
        #                 self.get_logger().warn("found somebody")
        #                 self.turtle_list[i],self.turtle_list[0]=self.turtle_list[0],self.turtle_list[i]
        #                 dist=new_dist
        #         except Exception as e:
        #             self.get_logger().error("i="+str(i)+" len="+str(len(self.turtle_list)))
        #         i+=1
        if dist>0.5:
            cmd_vel.linear.x=dist
            if diff_theta>math.pi:
                diff_theta-=2*math.pi
            elif diff_theta<-math.pi:
                diff_theta+=2*math.pi
            cmd_vel.angular.z=9*diff_theta
        elif dist<0.5:
            cmd_vel.linear.x=0.0
            cmd_vel.angular.z=0.0
            self.kill_turtle(self.turtle_list[0].name)
            self.turtle_list.pop(0)
            if len(self.turtle_list)>0:
                self.target_x=self.turtle_list[0].x
                self.target_y=self.turtle_list[0].y
            else:
                self.target_x=None
                self.target_y=None
        self.cmd_vel_publisher.publish(cmd_vel)

def main(args=None):
    rclpy.init(args=args)
    node = nodeMaker()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()