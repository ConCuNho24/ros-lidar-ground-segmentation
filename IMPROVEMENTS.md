# Improvements / Future Work

The current implementation works well for the provided haul road dataset. 
However, if I had more time, there are a few areas I would like to improve.

## 1. More General Plane Model

Right now, I model the ground as:

    z = a*x + b*y + c

This is suitable because the ground in the dataset is mostly flat.

If the terrain was more complex (for example, with steeper slopes), it would be better to use the full 3D plane equation:

    ax + by + cz + d = 0

and compute the true distance from each point to the plane.  
This would make the solution more general and less dependent on the flat-ground assumption.

---

## 2. Threshold Adjustment

The segmentation currently uses a fixed threshold (0.15 m).

This value works for the given bag file, but in different environments the optimal value may change.

In the future, I would:

- Tune this value more carefully,
- Make it easier to adjust via ROS parameters,
- Test how different thresholds affect the segmentation quality.

---

## 3. Basic Performance Improvements

For larger point clouds or higher-frequency LiDAR data, performance could become important.

Some simple improvements could include:

- Downsampling the point cloud before running RANSAC,
- Reducing unnecessary memory allocations,
- Measuring processing time per frame.

The current implementation is fast enough for the provided dataset, but these changes would help in more demanding scenarios.

---

## 4. Code Improvements

Some engineering improvements could also be added:

- Writing small unit tests for the plane fitting function,
- Logging basic runtime information,
- Further cleaning and organizing the code.

Overall, this implementation focuses on clarity and correctness for the given task, with room for gradual improvement as system requirements increase.
