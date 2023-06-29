import numpy as np
import pandas as pd
from pathlib import Path
from rich.progress import track


def construct_arm_displacement_frame_x(session_path_dict: dict) -> list:
    '''Constructs displacement array for x distance from arm center of mass to full body center of mass. '''

    segment_com_frame_joint_xyz = np.load(session_path_dict["segment_COM_frame_xyz"])
    total_body_COM_frame_xyz = np.load(session_path_dict["total_body_COM_frame_xyz"])
    print(f"Shape of segment_com_frame_joint_xyz: {segment_com_frame_joint_xyz.shape}")
    print(f"Shape of total_body_COM_frame_xyz: {total_body_COM_frame_xyz.shape}")

    arm_COM_frame_xyz = calculate_arm_center_of_mass(segment_com_frame_joint_xyz)
    print(f"Shape of arm_COM_frame_xyz: {arm_COM_frame_xyz.shape}")

    arm_displacement_frame_xyz = arm_COM_frame_xyz - total_body_COM_frame_xyz
    print(f"Shape of arm_displacement_frame_xyz: {arm_displacement_frame_xyz.shape}")
    
    arm_displacement_frame_x = arm_displacement_frame_xyz[:,0]
    print(f"Shape of arm_displacement_frame_x: {arm_displacement_frame_x.shape}")

    return arm_displacement_frame_x

def calculate_arm_center_of_mass(
    segment_com_frame_joint_xyz: np.ndarray
) -> np.ndarray:
    arm_segment_frame_xyz_dict = {
        "right_upper_arm": segment_com_frame_joint_xyz[:,2,:],
        "left_upper_arm": segment_com_frame_joint_xyz[:,3,:],
        "right_forearm": segment_com_frame_joint_xyz[:,4,:],
        "left_forearm": segment_com_frame_joint_xyz[:,5,:],
        "right_hand": segment_com_frame_joint_xyz[:,6,:],
        "left_hand": segment_com_frame_joint_xyz[:,7,:],
    }

    segment_COM_percentage_dict = {
        "right_upper_arm": 0.28,
        "left_upper_arm": 0.28,
        "right_forearm": 0.16,
        "left_forearm": 0.16,
        "right_hand": 0.06,
        "left_hand": 0.06,
    }

    num_frames = segment_com_frame_joint_xyz.shape[0]

    arm_com_frame_xyz = np.zeros((num_frames,3))

    for frame in range(num_frames):
        x, y, z = (0, 0, 0)

        for segment_name, segment_frame_xyz in arm_segment_frame_xyz_dict.items():
            x += segment_frame_xyz[frame, 0] * segment_COM_percentage_dict[segment_name]
            y += segment_frame_xyz[frame, 1] * segment_COM_percentage_dict[segment_name]
            z += segment_frame_xyz[frame, 2] * segment_COM_percentage_dict[segment_name]

        arm_com_frame_xyz[frame] = [x, y, z]
    
    return arm_com_frame_xyz


def main():
    session_id = "4stepsequence_session2_10_5_22"
    freemocap_data_folder_path = Path("/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data")
    session_folder_path = freemocap_data_folder_path / session_id
    path_dict_file_name = "session_path_dict.npy"
    path_dict_file_path = session_folder_path / path_dict_file_name

    path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
    
    arm_displacement_frame_x = construct_arm_displacement_frame_x(path_dict)
    print(arm_displacement_frame_x)



if __name__ == "__main__": 
    main()