from os.path import join

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def get_gazebo_launcher():
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            join(get_package_share_directory('gazebo_ros'), 'launch'),
            '/gazebo.launch.py'
        ]),
    )

def get_spawn_entity():
    return Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'dribot', '-topic', '/robot_description'],
        output='screen',
    )

def get_robot_state_node():
    pkg_share = FindPackageShare(package='dribot_description').find('dribot_description')

    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            join(pkg_share, 'launch/load_description_launch.py'),
        ])
    )

def get_dribot_perception():
    pkg_share = FindPackageShare(package='dribot_perception').find('dribot_perception')

    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            join(pkg_share, 'launch/dribot_ekf_launch.py'),
        ])
    )

def generate_launch_description():
    # Uncomment for manually controlling the robot.
    #teleop_keyboard = Node(
    #    package='teleop_twist_keyboard',
    #    executable='teleop_twist_keyboard',
    #    output='screen',
    #    prefix='xterm -e',
    #)

    return LaunchDescription([
        get_gazebo_launcher(),
        get_spawn_entity(),
        get_robot_state_node(),
        get_dribot_perception(),
        #teleop_keyboard,
    ])
