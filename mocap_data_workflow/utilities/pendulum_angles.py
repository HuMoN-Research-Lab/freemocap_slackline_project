import math

import numpy as np

from utilities.vector_utilities import get_angle_between_vectors, normalize_vector


def get_virtual_pendulum_angle_array(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz):
    '''Get angle of virtual pendulum between BOS and COM (on x and z axis) for each frame'''
    virtual_pendulum_angle_array = [get_virtual_pendulum_angle(BOS_trajectories_frame_xyz[i],com_trajectories_frame_xyz[i]) for i in range(BOS_trajectories_frame_xyz.shape[0])]
    
    return np.array(virtual_pendulum_angle_array)
    
def get_virtual_pendulum_angle(base_coordinate_xyz, top_coordinate_xyz):
    '''Find angle, in degrees, from vertical line (x-axis), between base coordinate and top coordinate. 
    Clockwise angles are positive, counter clockwise angles are negative.
    '''
    
    pendulum_line = [(top_coordinate_xyz[0]-base_coordinate_xyz[0]),(top_coordinate_xyz[2]-base_coordinate_xyz[2])] #vector representing the pendulum, moved to the origin
    vertical_line = [0,(top_coordinate_xyz[2]-base_coordinate_xyz[2])] #vector representing the vertical line (line of gravity), moved to the origin

    # normalizing vectors is best practice
    normalized_pendulum_vector = normalize_vector(pendulum_line)
    normalized_vertical_vector = normalize_vector(vertical_line)

    angle_between_vectors_radians = get_angle_between_vectors(normalized_vertical_vector, normalized_pendulum_vector)
    
    return math.degrees(angle_between_vectors_radians)