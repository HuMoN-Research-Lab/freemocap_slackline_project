from pathlib import Path
import numpy as np

from utilities.get_euclidean_distance import get_euclidean_distance_between_arrays
from utilities.com_values import segment_COM_percentages

def construct_inertia_frame(session_path_dict: dict) -> np.ndarray:
    """
    Constructs an array of the overall moment of inertia for each frame, calculated from the segment COM point.
    
    The moment of inertia is given in terms of percent mass * mm^2, and must be multiplied by the subjects mass before use.
    """

    segment_com_frame_joint_xyz = np.load(session_path_dict["segment_COM_frame_xyz"])
    total_body_COM_frame_xyz = np.load(session_path_dict["total_body_COM_frame_xyz"])

    print(f"Shape of segment_com_frame_joint_xyz: {segment_com_frame_joint_xyz.shape}")
    print(f"Shape of total_body_COM_frame_xyz: {total_body_COM_frame_xyz.shape}")
    
    segment_inertia = np.empty((total_body_COM_frame_xyz.shape[0], len(segment_COM_percentages)))
    for i, percentage in enumerate(segment_COM_percentages):
        distance = get_euclidean_distance_between_arrays(array_1=segment_com_frame_joint_xyz[:,i,:], array_2=total_body_COM_frame_xyz)
        segment_inertia[:, i] = percentage * distance * distance
        

    total_inertia =  np.sum(segment_inertia, axis=1)
    print(f"Shape of total_inertia: {total_inertia.shape}")
    return total_inertia


if __name__ == "__main__":
    session_id = "4stepsequence_session2_10_5_22"
    freemocap_data_folder_path = Path("/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data")
    session_folder_path = freemocap_data_folder_path / session_id
    path_dict_file_name = "session_path_dict.npy"
    path_dict_file_path = session_folder_path / path_dict_file_name

    path_dict = np.load(path_dict_file_path, allow_pickle=True).item()

    construct_inertia_frame(session_path_dict=path_dict)