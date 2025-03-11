from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
import os

def generate_launch_description():

    world_file = os.path.join(
        os.getenv('HOME'), 'ros2_ws', 'src', 'main_sim', 'worlds', 'obstacles_world.world'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=world_file,  
            description='Path to the Gazebo Sim world file'
        ),


        # Start Gazebo Sim (Ignition) with the world file
        ExecuteProcess(
            cmd=['gz', 'sim', LaunchConfiguration('world')],
            output='screen'
        ),
    ])


