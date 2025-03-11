import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Create the absolute path to the URDF file
    urdf_file_path = os.path.join(
        os.getenv('HOME'), 'ros2_ws', 'src', 'main_sim', 'urdf', 'my_robot.sdf'
    )

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gz', 'sim', '-r'],
            output='screen'
        ),
        ExecuteProcess(
            cmd=['gz', 'model', '--spawn-file', urdf_file_path, '--model-name', 'my_robot'],
            output='screen'
        ),
    ])

