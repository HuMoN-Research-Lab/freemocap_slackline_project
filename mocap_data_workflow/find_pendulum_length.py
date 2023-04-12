import logging
import numpy as np

from pathlib import Path


def load_path_dict(path_dict_file_path):
    path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
    logging.info("path dictionary loaded")

    return path_dict


def load_info_dictionary(freemocap_data_path, session):
    session_folder_path = freemocap_data_path / session
    info_dict_file_path = session_folder_path / "session_info_dict.npy"

    # load base of support data based on which foot I'm standing on
    if session == "4stepsequence_session2_10_5_22":
        start_frame = 2400
    elif session == "4stepsequence_session3_10_5_22":
        start_frame = 3900
    elif session == "4stepsequence_session4_10_5_22":
        start_frame = 3450
    elif session == "4stepsequence_session5_10_5_22":
        start_frame = 3540
    else:
        raise ValueError(f"Unknown session {session}")

    info_dict = np.load(info_dict_file_path, allow_pickle=True).item()

    info_dict["start_frame"] = start_frame

    return info_dict


def get_euclidean_distance_between_arrays(
    array_1: np.ndarray, array_2: np.ndarray
) -> np.ndarray:
    """
    Calculate the 2D Euclidean distance between corresponding points in two input arrays.
    
    The function computes the distance using only the x (0) and z (2) dimensions.
    
    Parameters:
    array_1 (np.ndarray): First input array with shape [X, 3], where X matches the other array.
    array_2 (np.ndarray): Second input array with shape [X, 3], where X matches the other array.
    
    Returns:
    np.ndarray: A 1D array of shape [X] containing the 2D Euclidean distances between corresponding points.
    """

    assert array_1.shape == array_2.shape, "Both input arrays must have the same shape"
    assert array_1.shape[1] == 3, "Each point must have 3 dimensions (x, y, z)"

    # Extract x and z dimensions from the arrays
    x1, z1 = array_1[:, 0], array_1[:, 2]
    x2, z2 = array_2[:, 0], array_2[:, 2]

    # Compute the 2D difference and squared difference
    squared_diff_x = (x1 - x2) ** 2
    squared_diff_z = (z1 - z2) ** 2

    # Compute the sum of squared differences and the final distances
    sum_squared_diff = squared_diff_x + squared_diff_z
    distances = np.sqrt(sum_squared_diff)

    return distances


def get_min_distance(distance_array: np.ndarray) -> float:
    min_distance = np.min(distance_array)
    print(f"Min distance: {min_distance}")
    return min_distance


def get_max_distance(distance_array: np.ndarray) -> float:
    max_distance = np.max(distance_array)
    print(f"Max distance: {max_distance}")
    return max_distance


def get_average_distance(distance_array: np.ndarray) -> float:
    average_distance = np.mean(distance_array)
    print(f"Average distance: {average_distance}")
    return average_distance

def get_standard_deviation(distance_array: np.ndarray) -> float:
    standard_deviation = np.std(distance_array)
    print(f"Standard deviation: {standard_deviation}")
    return standard_deviation


def find_pendulum_length(session_info_dictionary: dict, session_path_dictionary: dict) -> float:
    """
    Find the average length of the pendulum in the XZ plane for the given the session.
    
    Parameters:
    session_info_dictionary (dict): Info dictionary for the session (created by session_read_in.py).
    session_path_dictionary (dict): Path dictionary for the session (created by session_read_in.py).

    Returns:
    float: The average length of the pendulum.
    """

    start_frame = session_info_dictionary["start_frame"]
    fps = 60
    data_length_in_seconds = 15
    end_frame = start_frame + (data_length_in_seconds * fps)

    bos_frame_xyz = session_info_dictionary["BOS_frame_xyz"]
    total_body_COM_frame_xyz = np.load(session_path_dictionary["total_body_COM_frame_xyz"])

    distance_array = get_euclidean_distance_between_arrays(
        array_1=bos_frame_xyz[start_frame:end_frame, :],
        array_2=total_body_COM_frame_xyz[start_frame:end_frame, :],
    )

    min_distance = get_min_distance(distance_array)
    max_distance = get_max_distance(distance_array)
    average_distance = get_average_distance(distance_array)
    standard_deviation = get_standard_deviation(distance_array)

    return average_distance

def main():
    freemocap_data_path = Path(
        "/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data"
    )
    session_id = "4stepsequence_session2_10_5_22"

    session_dictionary = load_path_dict(
        freemocap_data_path / session_id / "session_path_dict.npy"
    )
    info_dictionary = load_info_dictionary(freemocap_data_path, session_id)

    find_pendulum_length(session_info_dictionary=info_dictionary, session_path_dictionary=session_dictionary)


if __name__ == "__main__":
    main()
