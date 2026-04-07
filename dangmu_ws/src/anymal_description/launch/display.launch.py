from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_joint_state_publisher = LaunchConfiguration("use_joint_state_publisher")

    urdf_path = PathJoinSubstitution(
        [FindPackageShare("anymal_description"), "urdf", "anymal.urdf"]
    )
    rviz_config_path = PathJoinSubstitution(
        [FindPackageShare("anymal_description"), "rviz", "display.rviz"]
    )

    robot_description = ParameterValue(
        Command(["xacro ", urdf_path]),
        value_type=str,
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true",
            description="Use simulation clock if available",
        ),
        DeclareLaunchArgument(
            "use_joint_state_publisher",
            default_value="true",
            description="Launch joint_state_publisher for visualization/testing",
        ),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[{
                "use_sim_time": use_sim_time,
                "robot_description": robot_description,
            }],
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="base_to_lidar",
            output="screen",
            arguments=["0.35", "0", "0.2", "0", "0", "0", "base", "lidar_frame"],
        ),
        Node(
            package="anymal_description",
            executable="odom_to_tf_broadcaster",
            name="odom_to_tf_broadcaster",
            output="screen",
            parameters=[{
                "odom_topic": "/odom",
                "odom_frame_id": "odom",
                "base_frame_id": "base",
            }],
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config_path],
            parameters=[{
                "use_sim_time": use_sim_time,
            }],
        ),
    ])
