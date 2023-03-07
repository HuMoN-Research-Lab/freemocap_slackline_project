import numpy as np
from pathlib import Path


def construct_BOS_frame_xyz(session_path_dict: dict, BOS_frame_list: list, starting_foot: str) -> list:
    '''Constructs trajectory array for base of support depending on which foot is on the line during the given session. '''

    segment_com_frame_joint_xyz = np.load(session_path_dict["segment_COM_frame_xyz"])
    print(f"Shape of segment_com_frame_joint_xyz: {segment_com_frame_joint_xyz.shape}")
    com_frame_xyz_dict = {"right": segment_com_frame_joint_xyz[:,12,:],
                        "left": segment_com_frame_joint_xyz[:,13,:]}

    current_foot = starting_foot
    BOS_frame_xyz = np.empty((0,3))
    print(f"shape of empty array is {BOS_frame_xyz.shape}")
    for index in range(len(BOS_frame_list)):
        start_frame = BOS_frame_list[index]
        if index == len(BOS_frame_list)-1:
            BOS_frame_xyz = np.concatenate((BOS_frame_xyz, com_frame_xyz_dict[current_foot][start_frame:, :]))
        else:
            end_frame = BOS_frame_list[index+1]
            BOS_frame_xyz = np.concatenate((BOS_frame_xyz, com_frame_xyz_dict[current_foot][start_frame:end_frame, :]))
    
    print(f"Shape of BOS_frame_X: {BOS_frame_xyz.shape}")
    return BOS_frame_xyz


def main():
    session_id = "4stepsequence_session2_10_5_22"
    freemocap_data_folder_path = Path("/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data")
    session_folder_path = freemocap_data_folder_path / session_id
    path_dict_file_name = "session_path_dict.npy"
    path_dict_file_path = session_folder_path / path_dict_file_name

    path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
    BOS_frame_list = [0, 3371, 4371]
    starting_foot = "left"
    BOS_frame_xyz = construct_BOS_frame_xyz(path_dict, BOS_frame_list, starting_foot)



if __name__ == "__main__": 
    main()