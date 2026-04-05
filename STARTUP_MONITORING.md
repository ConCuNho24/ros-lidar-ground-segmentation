# Automatic Startup and Monitoring

This section describes how the segmentation node could be started automatically and monitored in a real system.

## 1. Automatic Startup

In a practical deployment, the program should not require manual terminal commands to run.

On Ubuntu, one reasonable approach would be to use **systemd** to start the ROS launch file at boot.

The service would:

- Source the ROS Noetic environment,
- Source the catkin workspace (`devel/setup.bash`),
- Execute:

      roslaunch lidar_segmentation my_launch.launch

With this setup, the segmentation node would start automatically whenever the system boots.

---

## 2. Restart on Failure

To improve reliability, the system should restart the node if it crashes.

Using systemd, this can be configured with options such as:

- `Restart=always`
- `RestartSec=3`

This ensures that the program is automatically restarted after unexpected termination.

---

## 3. Basic Monitoring

Basic monitoring can be performed using standard ROS tools:

- `rosnode list` to confirm that the node is running,
- `rosnode ping` to verify responsiveness,
- `rostopic hz /ground` and `/nonground` to check that data is being published.

Logging with `rospy.logwarn` and `rospy.logerr` can also help identify runtime issues.

Overall, this approach keeps the setup simple while ensuring automatic startup and basic reliability.
