import math
import logging
import numpy as np
from pathlib import Path

logging.basicConfig(level=logging.INFO)

"""Load in a session, and extract the state information from that session, which should look like:
Q: [BOS location, pendulum angle, arm distance]
QDot: [BOS velocity, pendulum angle velocity, arm distance velocity]
QDDot: [BOS acceleration, pendulum angle acceleration, arm distance acceleration]
"""


def pendulum_arms_state_information(
    BOS_trajectories_frame_xyz: np.ndarray,
    pendulum_angle_frame: np.ndarray,
    arm_displacement_frame: np.ndarray,
):
    start_frame = 2750
    end_frame = 3250

    """Puts trajectories into state format to conform with the structure of ODEint, scipy's ODE solver"""
    BOS_frame_x = BOS_trajectories_frame_xyz[:, 0]
    print(f"Shape of BOS frame x array is: {BOS_frame_x.shape}")
    BOS_velocity = np.diff(pad_array(BOS_frame_x))
    print(f"Shape of BOS velocity array is: {BOS_velocity.shape}")
    BOS_acceleration = np.diff(pad_array(BOS_velocity))
    print(f"Shape of BOS acceleration array is: {BOS_acceleration.shape}")

    print(f"Shape of pendulum angle array is: {pendulum_angle_frame.shape}")
    pendulum_velocity = np.diff(pad_array(pendulum_angle_frame))
    print(f"Shape of pendulum velocity array is: {pendulum_velocity.shape}")
    pendulum_acceleration = np.diff(pad_array(pendulum_velocity))
    print(f"Shape of pendulum acceleration array is: {pendulum_acceleration.shape}")

    print(f"Shape of arm displacement array is: {arm_displacement_frame.shape}")
    arm_velocity = np.diff(pad_array(arm_displacement_frame))
    print(f"Shape of arm velocity array is: {arm_velocity.shape}")
    arm_acceleration = np.diff(pad_array(arm_velocity))
    print(f"Shape of arm acceleration array is: {arm_acceleration.shape}")

    assert check_arrays_have_same_shape(
        [
            BOS_frame_x,
            BOS_velocity,
            BOS_acceleration,
            pendulum_angle_frame,
            pendulum_velocity,
            pendulum_acceleration,
            arm_displacement_frame,
            arm_velocity,
            arm_acceleration,
        ]
    ), "Input arrays must have same length"

    q = []
    qdot = []
    qddot = []
    for frame in range(start_frame, end_frame):
        this_frame_q = np.array(
            [
                BOS_frame_x[frame],
                pendulum_angle_frame[frame],
                arm_displacement_frame[frame],
            ]
        )
        q.append(this_frame_q)
        this_frame_qdot = np.array(
            [BOS_velocity[frame], pendulum_velocity[frame], arm_velocity[frame]]
        )
        qdot.append(this_frame_qdot)
        this_frame_qddot = np.array(
            [BOS_acceleration[frame], 
            pendulum_acceleration[frame],
            arm_acceleration[frame]]
        )
        qddot.append(this_frame_qddot)


    print(f"Shape of q array is: {np.array(q).shape}")
    print(f"Shape of qdot array is: {np.array(qdot).shape}")
    print(f"Shape of qddot array is: {np.array(qddot).shape}")
    return (np.array(q), np.array(qdot), np.array(qddot))


def save_state_information(path_dict, state_information, start_frame, end_frame):
    save_name = (
        path_dict["session_id"] + "_" + str(start_frame) + "_" + str(end_frame) + ".npy"
    )
    save_path = path_dict["freemocap_data_folder"] / save_name

    np.save(save_path, state_information[start_frame:end_frame, :])
    logging.info(f"state information saved to file {save_path}")


def get_virtual_pendulum_angle_array(
    BOS_trajectories_frame_xyz, com_trajectories_frame_xyz
):
    """Get angle of virtual pendulum between BOS and COM (on x and z axis) for each frame"""
    virtual_pendulum_angle_array = [
        get_virtual_pendulum_angle(
            BOS_trajectories_frame_xyz[i], com_trajectories_frame_xyz[i]
        )
        for i in range(BOS_trajectories_frame_xyz.shape[0])
    ]

    return np.array(virtual_pendulum_angle_array)


def get_virtual_pendulum_angle(base_coordinate_xyz, top_coordinate_xyz):
    """Find angle, in degrees, from vertical line (x-axis), between base coordinate and top coordinate.
    Clockwise angles are positive, counter clockwise angles are negative.
    """

    pendulum_line = [
        (top_coordinate_xyz[0] - base_coordinate_xyz[0]),
        (top_coordinate_xyz[2] - base_coordinate_xyz[2]),
    ]  # vector representing the pendulum, moved to the origin
    vertical_line = [
        0,
        (top_coordinate_xyz[2] - base_coordinate_xyz[2]),
    ]  # vector representing the vertical line (line of gravity), moved to the origin

    # normalizing vectors is best practice
    normalized_pendulum_vector = normalize_vector(pendulum_line)
    normalized_vertical_vector = normalize_vector(vertical_line)

    angle_between_vectors_radians = get_angle_between_vectors(
        normalized_vertical_vector, normalized_pendulum_vector
    )

    return math.degrees(angle_between_vectors_radians)


def get_angle_between_vectors(reference_vector, signed_vector):
    """Gives the signed angle in radians between two normalized vectors.
    The sign of the angle will be positive if the signed vector is clockwise of the reference vector, and negative otherwise.
    """

    angle = np.arctan2(
        np.cross(signed_vector, reference_vector),
        np.dot(reference_vector, signed_vector),
    )
    return angle


def normalize_vector(vector):
    """Create vector with length 1 in same direction as input vector (equivalent to unit vector)"""

    return vector / np.linalg.norm(vector)


def check_arrays_have_same_shape(list_of_arrays: list) -> bool:
    """Check if all arrays in provided list have the same length."""
    if check_arrays_are_ndarrays(list_of_arrays):
        shape_to_check_against = list_of_arrays[0].shape

        list_of_shapes = [
            array.shape
            for array in list_of_arrays
            if array.shape != shape_to_check_against
        ]
        if len(list_of_shapes) == 0:
            logging.debug("All input arrays are the same length")
            return True

        logging.error("Arrays are not all of same length")
        print(f"array shapes: {list_of_shapes}")
        return False


def check_arrays_are_ndarrays(list_of_potential_arrays: list) -> bool:
    """Check if all arrays in provided list are of the type np.ndarray, to catch errors before calling .shape"""
    for array in list_of_potential_arrays:
        if not isinstance(array, np.ndarray):
            logging.error(f"{array} must be of type np.ndarray")
            return False

    logging.debug("All arrays are np.ndarray type")
    return True


def pad_array(array):
    """Duplicates the first item of an array to preserve array size while differentiating."""
    padded_array = array.copy()

    return np.insert(padded_array, 0, array[0])

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


def main():
    session_id = "4stepsequence_session2_10_5_22"
    freemocap_data_folder_path = Path(
        "/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data"
    )
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
    arm_displacement_frame = session_info_dict["arm_displacement_frame_x"]

    state_q, state_qdot, state_qddot = pendulum_arms_state_information(
        BOS_trajectories_frame_xyz, pendulum_angle_frame, arm_displacement_frame
    )
    np.save(session_folder_path / "state_q.npy", state_q)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_q.npy'}"
    )
    np.save(session_folder_path / "state_qdot.npy", state_qdot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_qdot.npy'}"
    )
    np.save(session_folder_path / "state_qddot.npy", state_qddot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_qddot.npy'}"
    )


if __name__ == "__main__":
    main()
