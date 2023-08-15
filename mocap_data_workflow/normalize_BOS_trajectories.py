import numpy as np


def normalize_BOS_trajectories(BOS_trajectories_frame_xyz, start_frame, end_frame):
    """Centers the x positions of the BOS trajectories around 0 by subtracting the mean during the frame interval."""
    mean_x_across_interval = np.nanmean(BOS_trajectories_frame_xyz[start_frame:end_frame, 0])
    BOS_trajectories_frame_xyz[:, 0] -= mean_x_across_interval
