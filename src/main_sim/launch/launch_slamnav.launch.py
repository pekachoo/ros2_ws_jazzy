import os
from ament_index_python.packages import get_package_share_directory, get_package_share_path
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from launch.conditions import IfCondition

def generate_launch_description():
    # Check if we're told to use sim time
    slam_params = '/home/jason/ros2_ws/src/main_sim/config/mapper_params_online_async.yaml'
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('slam_toolbox'),
                'launch',
                'online_async_launch.py'
            )
        ),
        launch_arguments={
            'slam_params_file': slam_params,
            'use_sim_time': 'true'
        }.items()
    )

    nav2_params = '/home/jason/ros2_ws/src/main_sim/config/nav2_params.yaml'
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('nav2_bringup'),
                'launch',
                'navigation_launch.py'
            )
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'autostart': 'true',
            # 'use_collision_monitoring': 'false',
            'params_file': nav2_params
        }.items()
    )

    rviz_params = '/home/jason/ros2_ws/src/main_sim/config/nav_rviz.rviz'
    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description=''
    )
    
    rviz_config_arg = DeclareLaunchArgument(
        'rviz_config',
        default_value=rviz_params,
        description=''
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rviz_config')],
        condition=IfCondition(LaunchConfiguration('use_rviz'))
    )




    # Launch the full setup
    return LaunchDescription([
        slam_launch,
        nav2_launch,
        use_rviz_arg,
        rviz_config_arg,
        rviz_node
    ])
