from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from utilities.vector_utilities import (
    get_signed_angle_between_vectors,
    normalize_vector,
)
from utilities.com_values import segment_COM_percentages


def construct_rotation_frame(
    session_path_dict: dict, session_info_dict: dict
) -> np.ndarray:
    """
    Constructs an array of the overall rotation for each frame, relative to the line of the virtual pendulum.
    """

    segment_com_frame_joint_xyz = np.load(session_path_dict["segment_COM_frame_xyz"])
    total_body_COM_frame_xyz = np.load(session_path_dict["total_body_COM_frame_xyz"])
    bos_frame_xyz = session_info_dict["BOS_frame_xyz"]

    print(f"Shape of segment_com_frame_joint_xyz: {segment_com_frame_joint_xyz.shape}")
    print(f"Shape of total_body_COM_frame_xyz: {total_body_COM_frame_xyz.shape}")
    print(f"Shape of bos_frame_xyz: {bos_frame_xyz.shape}")

    rotation_frame = np.empty(total_body_COM_frame_xyz.shape[0])
    for frame in range(total_body_COM_frame_xyz.shape[0]):
        pendulum_vector = [
            (total_body_COM_frame_xyz[frame, 0] - bos_frame_xyz[frame, 0]),
            (total_body_COM_frame_xyz[frame, 2] - bos_frame_xyz[frame, 2]),
        ]
        normalized_pendulum_vector = normalize_vector(pendulum_vector)
        segment_vector_list = []
        for segment_index in range(segment_com_frame_joint_xyz.shape[1]):
            segment_vector = np.array([
                (
                    total_body_COM_frame_xyz[frame, 0]
                    - segment_com_frame_joint_xyz[frame, segment_index, 0]
                ),
                (
                    total_body_COM_frame_xyz[frame, 2]
                    - segment_com_frame_joint_xyz[frame, segment_index, 2]
                ),
            ])
            weighted_segment_vector = segment_vector * segment_COM_percentages[segment_index] # multiply by relative weight of segment
            segment_vector_list.append(weighted_segment_vector)
            # segment_vector_list.append(segment_vector)
        this_frame_vector = np.sum(segment_vector_list, axis=0)
        normalized_frame_vector = normalize_vector(this_frame_vector)
        this_frame_angle = get_signed_angle_between_vectors(
            normalized_pendulum_vector, normalized_frame_vector
        )
        rotation_frame[frame] = this_frame_angle

    print(f"Shape of rotation_frame: {rotation_frame.shape}")
    print(f"rotation at frame 0: {rotation_frame[0]}")

    return rotation_frame


def get_segment_vectors(
    total_body_com_frame_xyz: np.ndarray,
    segment_com_frame_joint_xyz: np.ndarray,
    frame: int,
    segment_COM_percentages: list,
) -> list:
    """Get the vectors from the total body center of mass to the segment center of mass for a given frame"""
    segment_vectors = []
    for segment_index in range(segment_com_frame_joint_xyz.shape[1]):
        segment_vector = [
            (
                total_body_com_frame_xyz[frame, 0]
                - segment_com_frame_joint_xyz[frame, segment_index, 0]
            ),
            (
                total_body_com_frame_xyz[frame, 2]
                - segment_com_frame_joint_xyz[frame, segment_index, 2]
            ),
        ]
        segment_vector *= segment_COM_percentages[segment_index]
        segment_vectors.append(segment_vector)
    return segment_vectors


def plot_rotation_across_frames(rotation_frame: np.ndarray):
    fig, axs = plt.subplots(3, 1)  # Create a figure with 3 subplots arranged vertically

    # Plot the rotation_frame in the first subplot
    axs[0].plot(rotation_frame)
    axs[0].set_ylabel('Rotation Frame')
    axs[0].set_title('Rotation Across Frames')
    axs[0].set_xlim(2750, 3250)

    # Plot the first difference of the rotation_frame in the second subplot
    diff1 = np.diff(rotation_frame)
    axs[1].plot(diff1, alpha=0.6)
    axs[1].set_ylabel('First Difference')
    axs[1].set_xlim(2750, 3250)

    # Plot the second difference of the rotation_frame in the third subplot
    diff2 = np.diff(diff1)
    axs[2].plot(diff2, alpha=0.4)
    axs[2].set_ylabel('Second Difference')
    axs[2].set_xlabel('Frame')
    axs[2].set_xlim(2750, 3250)

    plt.tight_layout()  # Adjust spacing between subplots
    plt.show()


if __name__ == "__main__":
    session_id = "4stepsequence_session2_10_5_22"
    freemocap_data_folder_path = Path(
        "/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data"
    )
    session_folder_path = freemocap_data_folder_path / session_id
    path_dict_file_name = "session_path_dict.npy"
    path_dict_file_path = session_folder_path / path_dict_file_name
    info_dict_file_name = "session_info_dict.npy"
    info_dict_file_path = session_folder_path / info_dict_file_name

    path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
    session_info_dict = np.load(info_dict_file_path, allow_pickle=True).item()

    rotation_frame = construct_rotation_frame(
        session_path_dict=path_dict, session_info_dict=session_info_dict
    )
    plot_rotation_across_frames(rotation_frame)
