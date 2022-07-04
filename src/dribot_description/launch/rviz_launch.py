from os.path import join

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command


def get_joint_state_node():
    return Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
    )

def get_robot_state_node(pkg_share):
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            join(pkg_share, 'launch/load_description_launch.py'),
        ])
    )

def get_rviz2_node(pkg_share):
    dribot_rviz_config_path = join(pkg_share, 'config/dribot.rviz')

    # Note that we pass down the rviz configuration file to rviz. This is to avoid
    # adjusting the frame and other options after start.
    return Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', dribot_rviz_config_path],
        name='rviz2',
        output='screen',
    )

def generate_launch_description():
    pkg_share = FindPackageShare(package='dribot_description').find('dribot_description')

    return LaunchDescription([
        get_joint_state_node(),
        get_robot_state_node(pkg_share),
        get_rviz2_node(pkg_share)
    ])
