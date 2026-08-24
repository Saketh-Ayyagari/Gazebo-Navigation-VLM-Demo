import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

def generate_launch_description():

    # Custom Message creator node
    msg_creator = Node(
        package='sakeths_robot_vision',
        executable='message_creator',
        name='message_creator',
    )

    img_subscriber = Node(
            package='sakeths_robot_vision',
            executable='image_subscriber',
            name='pipeline',
        )


    # Launch them all!
    return LaunchDescription([
        msg_creator,
        img_subscriber
    ])