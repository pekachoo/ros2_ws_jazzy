import os
from ament_index_python.packages import get_package_share_directory, get_package_share_path
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Get the urdf/xacro file path
    path_to_urdf = "/home/jason/ros2_ws/src/main_sim/urdf/mecanum_sphere/mecanum_sphere.urdf.xacro"

    urdf_string = ParameterValue(Command(['xacro ', str(path_to_urdf)]), value_type=str)

    # Create a robot_state_publisher node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': urdf_string,
            'use_sim_time': use_sim_time,
        }]
    )

    # Use a custom Gazebo world (if needed)
    # world_file = '/opt/ros/jazzy/opt/gz_sim_vendor/share/gz/gz-sim8/worlds/empty.sdf'
    world_file = '/home/jason/ros2_ws/src/main_sim/worlds/updated_dynamic.world'

    # Start Gazebo Sim
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ]),
        launch_arguments={"gz_args": ['-r -v4 ', world_file], 'on_exit_shutdown': 'true'}.items(),
    )

    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('main_sim'),'launch','joystick.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Spawn the robot in Gazebo Sim
    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name",
            "my_bot",
            "-topic",
            "/robot_description",
            "-x",
            "0",
            "-y",
            "0",
            "-z",
            "1.4",
        ],
        output="screen",
    )

    mecanum_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["mecanum_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    twist_mux_params = '/home/jason/ros2_ws/src/main_sim/config/twist_mux_mecanum.yaml'
    twist_mux = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_mux_params, {'use_sim_time': True, 'use_stamped': True}],
        remappings=[('/cmd_vel_out','/cmd_vel_stamped')]
    )

    bridge_params = '/home/jason/ros2_ws/src/main_sim/config/gz_bridge_mecanum.yaml'
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            # '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ]
    )

    # Launch the full setup
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use sim time if true'),
        node_robot_state_publisher,
        # joystick,
        twist_mux,
        gz_sim,
        spawn_entity,
        mecanum_drive_spawner,
        joint_broad_spawner,
        ros_gz_bridge
    ])
