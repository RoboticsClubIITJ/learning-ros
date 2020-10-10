from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld=LaunchDescription()

    turtlesim_node=Node(
        package="turtlesim",
        executable="turtlesim_node"
    )

    turtle_control=Node(
        package="capture_turtle",
        executable="turtle_controller"
    )

    turtle_spawn=Node(
        package="capture_turtle",
        executable="turtle_spawner"
    )

    ld.add_action(turtlesim_node)
    ld.add_action(turtle_control)
    ld.add_action(turtle_spawn)
    return ld