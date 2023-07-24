import numpy as np


def get_angle_between_vectors(reference_vector, signed_vector):
    '''Gives the signed angle in radians between two normalized vectors. 
    The sign of the angle will be positive if the signed vector is clockwise of the reference vector, and negative otherwise.
    '''

    angle = np.arctan2(np.cross(signed_vector,reference_vector),np.dot(reference_vector,signed_vector))
    return angle

def normalize_vector(vector):
    '''Create vector with length 1 in same direction as input vector (equivalent to unit vector)'''

    return vector / np.linalg.norm(vector)