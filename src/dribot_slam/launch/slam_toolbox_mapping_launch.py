from os.path import join

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def get_slam_toolbox():
    pkg_share = FindPackageShare(package='dribot_slam').find('dribot_slam')

    return Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            join(pkg_share, 'params', 'mapper_params_online_async.yaml'),
            {'use_sim_time': True},
        ],
    )

def generate_launch_description():
    return LaunchDescription([
        get_slam_toolbox(),
    ])
