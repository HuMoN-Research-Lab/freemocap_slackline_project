import numpy as np
from pathlib import Path

'''Load in a session, and extract the state information from that session, which should look like:
[BOS location, BOS velocity, COM location, COM velocity, angular momentum/velocity]
'''

def get_state_information(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz, angular_velocity):
    '''Puts trajectories into state format to conform with the structure of ODEint, scipy's ODE solver'''
    BOS_frame_x = BOS_trajectories_frame_xyz[:,0]
    BOS_velocity = np.diff(pad_array(BOS_frame_x))

    com_frame_x = com_trajectories_frame_xyz[:,0]
    com_velocity = np.diff(pad_array(com_frame_x))

def get_virtual_pendulum_angle_array(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz):
    '''Get angle of virtual pendulum between BOS and COM (on x and z axis) for each frame'''
    pass

def get_virtual_pendulum_angle(base_coordinate_xyz, top_coordinate_xyz):
    '''Find angle, in degrees, from vertical line (x-axis), between base coordinate and top coordinate. 
    Clockwise angles are positive, counter clockwise angles are negative.
    '''
    
    pendulum_line = [(base_coordinate_xyz[0],base_coordinate_xyz[2]),(top_coordinate_xyz[0],top_coordinate_xyz[2])] #vector representing the pendulum
    vertical_line = [(base_coordinate_xyz[0],base_coordinate_xyz[2]),(base_coordinate_xyz[0],top_coordinate_xyz[2])] #vector representing the vertical line (line of gravity)

    # normalizing vectors is best practice
    normalized_pendulum_vector = normalize_vector(pendulum_line)
    normalized_vertical_vector = normalize_vector(vertical_line)

    angle_between_vectors_radians = get_angle_between_vectors(normalized_vertical_vector, normalized_pendulum_vector)
    return np.degrees(angle_between_vectors_radians)

def get_angle_between_vectors(reference_vector, signed_vector):
    '''Gives the signed angle in radians between two normalized vectors. 
    The sign of the angle will be positive if the signed vector is clockwise of the reference vector, and negative otherwise.
    '''

    return np.arctan2(np.cross(signed_vector,reference_vector),np.dot(reference_vector,signed_vector))

def normalize_vector(vector):
    '''Create vector with length 1 in same direction as input vector (equivalent to unit vector)'''

    return vector / np.linalg.norm(vector)

def pad_array(array):
    '''Duplicates the first item of an array to preserve array size while differentiating.'''
    padded_array = array.copy()

    return np.insert(padded_array,0,array[0])

