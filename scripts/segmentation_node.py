#!/usr/bin/env python3

import rospy
import numpy as np
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from std_msgs.msg import Header

ground_pub = None
nonground_pub = None


def msg_to_np(msg):
    """
    Convert PointCloud2 message to numpy array of shape (N, 3).
    """
    pts = list(pc2.read_points(msg,
                               field_names=("x", "y", "z"),
                               skip_nans=True))

    if len(pts) < 20:
        return None

    return np.asarray(pts, dtype=np.float64)


def ransac_plane(points, thresh=0.15, iters=80):
    """
    Estimate ground plane using RANSAC with model:
        z = a*x + b*y + c

    Procedure:
      1. Randomly sample 3 points.
      2. Solve linear system for (a, b, c).
      3. Compute residuals for all points.
      4. Select model with maximum inliers.
      5. Refit using least squares on inliers.
    """

    n = points.shape[0]
    rng = np.random.default_rng()

    best_mask = None
    best_cnt = 0

    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    for _ in range(iters):

        idx = rng.choice(n, 3, replace=False)

        A = np.array([
            [x[idx[0]], y[idx[0]], 1.0],
            [x[idx[1]], y[idx[1]], 1.0],
            [x[idx[2]], y[idx[2]], 1.0],
        ], dtype=np.float64)

        B = np.array([
            z[idx[0]],
            z[idx[1]],
            z[idx[2]]
        ], dtype=np.float64)

        try:
            a, b1, c = np.linalg.solve(A, B)
        except np.linalg.LinAlgError:
            continue

        # Vertical residual (approx. orthogonal distance for small slopes)
        r = np.abs((a * x + b1 * y + c) - z)

        mask = r < thresh
        cnt = int(mask.sum())

        if cnt > best_cnt:
            best_cnt = cnt
            best_mask = mask

            if best_cnt > 0.90 * n:
                break

    if best_mask is None or best_cnt < 20:
        return None, None, None, None

    # Least-squares refinement on inliers
    Xin = np.column_stack([
        x[best_mask],
        y[best_mask],
        np.ones(best_cnt)
    ])

    zin = z[best_mask]

    abc, _, _, _ = np.linalg.lstsq(Xin, zin, rcond=None)
    a, b1, c = abc

    r2 = np.abs((a * x + b1 * y + c) - z)
    final_mask = r2 < thresh

    return float(a), float(b1), float(c), final_mask


def callback(msg):
    global ground_pub, nonground_pub

    points = msg_to_np(msg)
    if points is None:
        return

    a, b1, c, mask = ransac_plane(points, thresh=0.15, iters=80)

    if mask is None:
        rospy.logwarn("RANSAC failed.")
        return

    header = Header(stamp=msg.header.stamp,
                    frame_id=msg.header.frame_id)

    ground_pub.publish(pc2.create_cloud_xyz32(header,
                                              points[mask]))

    nonground_pub.publish(pc2.create_cloud_xyz32(header,
                                                 points[~mask]))

    rospy.loginfo(
        "Ground: {} | Non-ground: {} | Plane: z={:.4f}x + {:.4f}y + {:.4f}".format(
            int(mask.sum()),
            int((~mask).sum()),
            a, b1, c
        )
    )


def main():
    global ground_pub, nonground_pub

    rospy.init_node("lidar_segmentation_math_ransac")

    ground_pub = rospy.Publisher("/ground",
                                 PointCloud2,
                                 queue_size=2)

    nonground_pub = rospy.Publisher("/nonground",
                                    PointCloud2,
                                    queue_size=2)

    rospy.Subscriber("/lidar",
                     PointCloud2,
                     callback,
                     queue_size=1)

    rospy.spin()


if __name__ == "__main__":
    main()
