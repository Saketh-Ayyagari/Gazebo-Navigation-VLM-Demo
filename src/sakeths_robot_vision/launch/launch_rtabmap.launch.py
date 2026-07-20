from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    parameters = [{
        'frame_id': 'base_link',
        'subscribe_depth': True,
        'subscribe_rgb': True,
        'use_sim_time': True,
        'approx_sync': True,
        'Reg/Force3DoF': 'true',   # good for ground robots
        'Grid/FromDepth': 'true',
    }]

    remappings = [
        ('rgb/image', '/camera/image_raw'),
        ('rgb/camera_info', '/camera/camera_info'),
        ('depth/image', '/camera/depth_image'),
        ('odom', '/odom'),
    ]

    return LaunchDescription([
        Node(
            package='rtabmap_odom', executable='rgbd_odometry', output='screen',
            parameters=parameters, remappings=remappings),

        Node(
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=parameters, remappings=remappings,
            arguments=['-d']),  # -d deletes old database on start

        Node(
            package='rtabmap_viz', executable='rtabmap_viz', output='screen',
            parameters=parameters, remappings=remappings),
    ])