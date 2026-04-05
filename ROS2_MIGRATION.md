# ROS 2 Migration (Jazzy+) – High-level Notes

This node is currently implemented in ROS 1 Noetic (rospy + catkin).  
To migrate to ROS 2 (Jazzy or later), the core segmentation math can stay mostly the same, but the ROS integration changes in several areas:

## 1) Build System
- ROS 1: catkin (`catkin_make`, `source devel/setup.bash`)
- ROS 2: ament/colcon (`colcon build`, `source install/setup.bash`)

## 2) Node Structure (Python)
- ROS 1 uses `rospy` scripts (`rospy.init_node`, `Publisher`, `Subscriber`, `spin`)
- ROS 2 uses `rclpy` and typically an OOP Node class:
  - `class SegmentationNode(Node)`
  - `self.create_publisher(...)`
  - `self.create_subscription(...)`
  - `rclpy.spin(node)`

## 3) Parameters
- ROS 1: `rospy.get_param("~thresh", 0.15)`
- ROS 2: parameters must be declared and then retrieved:
  - `self.declare_parameter("thresh", 0.15)`
  - `self.get_parameter("thresh").value`

## 4) QoS (Important in ROS 2)
- ROS 2 requires choosing a QoS profile for topics.
- For PointCloud2 sensor topics, a small queue depth and sensor-style QoS is commonly used.
- Upstream and downstream nodes must use compatible QoS to communicate.

## 5) Launch Files
- ROS 1 uses XML launch files.
- ROS 2 uses Python launch files (`.launch.py`), so `my_launch.launch` must be rewritten.

## 6) Bag Playback
- ROS 1: `rosbag play`
- ROS 2: `rosbag2 play` (different bag format)

Overall, the migration mainly involves changing the ROS “glue code” (node structure, params, launch, QoS), while the segmentation algorithm remains largely unchanged.
