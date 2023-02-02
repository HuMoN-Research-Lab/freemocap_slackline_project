import math
import numpy as np
from pathlib import Path

'''Load in a session, and extract the state information from that session, which should look like:
[BOS location, BOS velocity, COM location, COM velocity, angular momentum/velocity]
'''

def get_state_information(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz, pendulum_angle_frame):
    '''Puts trajectories into state format to conform with the structure of ODEint, scipy's ODE solver'''
    BOS_frame_x = BOS_trajectories_frame_xyz[:,0]
    BOS_velocity = np.diff(pad_array(BOS_frame_x))

    com_frame_x = com_trajectories_frame_xyz[:,0]
    com_velocity = np.diff(pad_array(com_frame_x))
    print(pendulum_angle_frame.shape)
    pendulum_velocity = np.diff(pad_array(pendulum_angle_frame))

    if check_arrays_have_same_length([BOS_frame_x, BOS_velocity, com_frame_x, com_velocity, pendulum_angle_frame, pendulum_velocity]):
        state_information = []
        for frame in range(BOS_frame_x.shape[0]):
            this_frame_state = np.array([BOS_frame_x[frame], BOS_velocity[frame], com_frame_x[frame], com_velocity[frame], pendulum_angle_frame[frame], pendulum_velocity[frame]])
            state_information.append(this_frame_state)

        return np.array(state_information)

    else:
        print("input arrays must have same length")

def save_state_information(path_dict, state_information, start_frame, end_frame):
    save_name = path_dict["session_id"] + "_" + str(start_frame) + "_" + str(end_frame) + ".npy"
    save_path = path_dict["freemocap_data_folder"] / save_name
    
    np.save(save_path,state_information[start_frame:end_frame,:])

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

def get_angle_between_vectors(reference_vector, signed_vector):
    '''Gives the signed angle in radians between two normalized vectors. 
    The sign of the angle will be positive if the signed vector is clockwise of the reference vector, and negative otherwise.
    '''

    angle = np.arctan2(np.cross(signed_vector,reference_vector),np.dot(reference_vector,signed_vector))
    return angle

def normalize_vector(vector):
    '''Create vector with length 1 in same direction as input vector (equivalent to unit vector)'''

    return vector / np.linalg.norm(vector)


def check_arrays_have_same_length(list_of_arrays: list) -> bool:
    '''Checks if all arrays in provided list have the same length.'''
    return True


def pad_array(array):
    '''Duplicates the first item of an array to preserve array size while differentiating.'''
    padded_array = array.copy()

    return np.insert(padded_array,0,array[0])

def main():
    session_id = "4stepsequence_session2_10_5_22"
    freemocap_data_folder_path = Path("/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data")
    session_folder_path = freemocap_data_folder_path / session_id
    path_dict_file_name = "session_path_dict.npy"
    path_dict_file_path = session_folder_path / path_dict_file_name
    session_info_dict_name = "session_info_dict.npy"
    session_info_dict_path = session_folder_path / session_info_dict_name

    path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
    session_info_dict = np.load(session_info_dict_path, allow_pickle=True).item()

    BOS_trajectories_frame_xyz = session_info_dict["BOS_frame_xyz"]
    com_trajectories_frame_xyz = np.load(path_dict["total_body_COM_frame_xyz"])
    pendulum_angle_frame = get_virtual_pendulum_angle_array(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz)

    state_information = get_state_information(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz, pendulum_angle_frame)
    print("State information succesfully extracted")



if __name__ == "__main__":
    main()
