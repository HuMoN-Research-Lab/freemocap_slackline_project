import logging
import numpy as np

from pathlib import Path

from utilities.get_euclidean_distance import get_euclidean_distance_between_arrays


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
