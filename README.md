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

## Dataset
The dataset is not included due to GitHub size limits.

Download here:
https://drive.google.com/file/d/1bA6ME2rAj54cUzmAC7u63DUCkyOc1mrT/view?usp=drive_link

After download:
Place lidar.bag into:
data/lidar.bag
