# AI / LLM Usage

AI assistance (ChatGPT) was used during development as a productivity and learning aid.

## 1. Environment Setup

AI was used to guide the installation and configuration of:

- ROS Noetic
- RViz
- Catkin workspace setup
- Basic ROS launch structure

This helped speed up environment setup and avoid common configuration issues.

---

## 2. Algorithm Discussion

The initial approach was based on full 3D geometry:

    ax + by + cz + d = 0

The idea of using RANSAC for robust plane fitting was discussed with AI to evaluate suitable approaches for LiDAR ground segmentation.

However, the geometric reasoning (starting from 3D plane equations) was my own starting point. After inspecting the dataset, I decided to simplify the model to:

    z = ax + by + c

based on the observation that the ground in the haul road dataset is mostly planar and near-horizontal.

---

## 3. ROS and Syntax Assistance

AI was used to:

- Clarify correct `rospy` syntax for publishers and subscribers.
- Resolve launch file substitution issues.
- Refine catkin packaging structure.
- Debug ROS-related runtime errors.

---

## 4. Code Refinement

AI provided suggestions for:

- Vectorizing residual computation using NumPy.
- Improving code structure for clarity.
- Refining documentation wording.

The final algorithm logic and parameter tuning were validated manually using RViz and rosbag playback.

---

AI was used as a support tool for learning and debugging, while the core design decisions and implementation logic were developed and tested independently.
