# Design Overview – LiDAR Ground Segmentation Node

This document outlines the design decisions behind the ROS node developed to segment LiDAR point clouds into ground and non-ground points, as required in the skills test.

The focus of this implementation is clarity, robustness, and computational simplicity while remaining suitable for real-time usage.

---

## 1. Initial Geometric Thinking

My first approach was to model the ground using the general 3D plane equation:

    ax + by + cz + d = 0

Using three non-collinear points, it is always possible to compute a plane in 3D space.

The idea was to:

1. Randomly sample three points.
2. Compute the full 3D plane.
3. Measure perpendicular distances from all points to the plane.
4. Classify inliers (ground) and outliers (obstacles).

This formulation is mathematically general and works for arbitrary plane orientations.

However, after inspecting the provided haul road bag file in RViz, it was clear that the ground surface is mostly horizontal and locally smooth. This observation allowed for simplification.

---

## 2. Model Simplification

Given the near-horizontal ground assumption, the plane can be expressed as:

    z = a*x + b*y + c

This treats z as a dependent variable instead of using the full 3D normal vector form.

Residuals are then computed as:

    |a*x + b*y + c - z|

This represents vertical distance rather than true orthogonal distance to the plane.

Why simplify?

- Avoids computing normal vectors and normalization.
- Avoids square root operations.
- Reduces computational cost.
- Sufficient for this dataset where vertical deviation dominates.

This simplification trades geometric generality for efficiency, which is acceptable for the haul road scenario.

---

## 3. RANSAC-Based Segmentation

To make the plane estimation robust to obstacles, a RANSAC strategy is used for each incoming frame:

1. Randomly sample 3 points.
2. Solve a 3x3 linear system to estimate (a, b, c).
3. Compute residuals for all points.
4. Count inliers within a fixed threshold (0.15 m).
5. Keep the model with the highest consensus.
6. Early stop if more than 90% of points agree.
7. Refit the plane using least squares on the inliers for improved stability.

This approach prevents obstacles (e.g., rocks or vegetation) from biasing the plane estimate.

---

## 4. Why RANSAC?

Direct least squares fitting over the entire point cloud would be sensitive to outliers.

LiDAR data from real environments contains many non-ground points, and RANSAC helps isolate the dominant planar structure by maximizing consensus among inliers.

This makes it a practical and robust choice for ground segmentation problems.

---

## 5. ROS Integration Design

The node subscribes to:

    /lidar (sensor_msgs/PointCloud2)

It publishes two separate topics:

    /ground
    /nonground

Separating these streams allows downstream modules (e.g., path planning, obstacle detection) to independently consume either surface or obstacle information.

Parameters such as threshold and iteration count are configurable via ROS parameters, allowing tuning without modifying the source code.

A launch file is used to:

- Enable simulated time
- Play the rosbag
- Start the segmentation node
- Open RViz with a preconfigured view

This ensures reproducibility and simplified execution.

---

## 6. Real-Time Considerations

The design supports real-time processing through:

- Vectorized NumPy operations for residual computation
- Limited iteration count (80)
- Early stopping at 90% consensus
- No inter-frame memory storage

The goal was to keep the algorithm lightweight and frame-independent.

---

## 7. Trade-offs

Advantages:

- Simple and easy to understand
- Robust to outliers
- Computationally efficient
- Suitable for relatively flat terrain

Limitations:

- Assumes approximately planar ground
- Uses vertical residual instead of orthogonal plane distance
- Does not perform obstacle clustering
- May struggle with steep or highly uneven terrain

---

## 8. Possible Improvements

With more time, the following extensions could be considered:

- Use full plane model (ax + by + cz + d = 0)
- Compute true orthogonal distances
- Add Euclidean clustering for obstacle grouping
- Implement adaptive thresholding
- Port to C++ for high-frequency LiDAR systems

---

Overall, the design prioritizes robustness and computational simplicity while remaining extensible for more advanced perception pipelines.
