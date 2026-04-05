# Decoda LiDAR Ground Segmentation (ROS1 Noetic)

## Environment

- Ubuntu 20.04
- ROS Noetic
- Python 3
- RViz

---

## Setup

Unzip the folder `lidar_segmentation` into:

    ~/catkin_ws/src/

Then build the workspace:

    cd ~/catkin_ws
    catkin_make
    source devel/setup.bash

---

## Run

    roslaunch lidar_segmentation my_launch.launch

The launch file will:

- Enable simulated time
- Play the provided rosbag file
- Run the segmentation node
- Open RViz with a preconfigured view

---

## Topics

Subscribes to:

- `/lidar` (sensor_msgs/PointCloud2)

Publishes:

- `/ground`
- `/nonground`

---

## Notes

- The included rosbag file is located in the `data/` folder.
- RViz configuration is provided in `segmentation.rviz`.
