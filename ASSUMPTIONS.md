# Assumptions

- The ground in the provided haul road dataset is approximately planar in local regions.
- The LiDAR sensor mounting remains fixed during recording (no unexpected frame changes).
- Only XYZ fields are required for segmentation; additional fields (e.g., intensity or ring) are not used.
- A fixed residual threshold (around 0.15 m) is sufficient for separating ground and obstacles in this dataset.
- The goal of this task is ground vs non-ground separation; clustering or advanced filtering is considered out of scope.
- RViz visualization relies on the `frame_id` contained in the incoming PointCloud2 messages.
