from os.path import join

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command


def get_robot_state_node():
    pkg_share = FindPackageShare(package='dribot_description').find('dribot_description')
    dribot_description_path = join(pkg_share, 'urdf/dribot_description.xacro')

    return Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command([
                'xacro ', dribot_description_path
            ]),
        }],
    )

def generate_launch_description():
    return LaunchDescription([
        get_robot_state_node(),
    ])
