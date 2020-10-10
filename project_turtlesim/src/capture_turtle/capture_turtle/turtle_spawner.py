#!/usr/bin/env python3  
import rclpy
import math
import random
from rclpy.node import Node
from turtlesim.srv import Spawn
from functools import partial
from turtle_interfaces.msg import TurtleID

class nodeMaker(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        self.create_timer(2,self.makeClientSpawner)
        # self.makeClientSpawner()

    def makeClientSpawner(self):
        client=self.create_client(Spawn,"spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("waiting for spawn...")
        request = Spawn.Request()
        new_x=random.random()*11
        new_y=random.random()*11
        new_theta=random.random()*2*math.pi
        # new_x=1.0
        # new_y=4.0
        # new_theta=0.0
        request.x=new_x
        request.y=new_y
        request.theta=new_theta
        future=client.call_async(request)
        future.add_done_callback(partial(self.callback_future,x=new_x,y=new_y,theta=new_theta))

    def callback_future(self,future,x,y,theta):
        try:
            turtle=TurtleID()
            turtle.name=future.result().name
            turtle.x=x
            turtle.y=y
            turtle.theta=theta
            pub=self.create_publisher(TurtleID,"turtleID",10)
            pub.publish(turtle)
        except Exception as e:
            self.get_logger().error("Unexpected Error... {}".format(e))


def main(args=None):
    rclpy.init()
    node = nodeMaker()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()