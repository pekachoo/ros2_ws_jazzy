from launch import LaunchDescription
from launch_ros.actions import Node
import os
import xacro

def generate_launch_description():
    # Get the path to the workspace source directory and construct the correct path to the xacro file
    ws_path = os.path.join(os.getenv('HOME'), 'ros2_ws', 'src', 'main_sim')
    xacro_file = os.path.join(ws_path, 'urdf', 'mecanum_robot.urdf.xacro')

    # Print the path for debugging purposes
    print(f"Full path to xacro file: {xacro_file}")

    # Process the xacro file
    try:
        robot_description_raw = xacro.process_file(xacro_file).toxml()
    except Exception as e:
        print(f"Error processing xacro file: {e}")
        raise

    # Configure the robot_state_publisher node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}]
    )

    return LaunchDescription([
        node_robot_state_publisher
    ])
