import numpy as np
from pathlib import Path

from session_read_in import FreemocapSession

def construct_BOS_array(session_path_dict: dict, BOS_frame_list: list, starting_foot: str) -> list:
    '''equivalent code to replicate: 
    BOS_frame_x = np.concatenate((Lfoot_COM_frame_xyz[:3371,0], Rfoot_COM_frame_xyz[3371:4371,0], Lfoot_COM_frame_xyz[4371:,0]))'''
    segment_com_frame_joint_xyz = np.load(session_path_dict["segment_COM_frame_xyz"])
    
    com_frame_xyz_dict = {"right": segment_com_frame_joint_xyz[:,12,:],
                        "left": segment_com_frame_joint_xyz[:,13,:]}

    current_foot = starting_foot
    BOS_frame_x = np.array([])

    for index in range(len(BOS_frame_list)):
        start_frame = BOS_frame_list[index]
        if index == len(BOS_frame_list)-1:
            BOS_frame_x = np.concatenate((BOS_frame_x, com_frame_xyz_dict[current_foot][start_frame:, 0]))
        else:
            end_frame = BOS_frame_list[index+1]
            BOS_frame_x = np.concatenate((BOS_frame_x, com_frame_xyz_dict[current_foot][start_frame:end_frame, 0])) #why does concatenating not work???
    
    return BOS_frame_x



def main():
    session_id = "4stepsequence_session5_10_5_22"
    freemocap_data_folder_path = Path("/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data")
    session_info = FreemocapSession(session_id, freemocap_data_folder_path)
    print(session_info.path_dict["data_arrays_folder"])

    BOS_frame_list = [0, 3371, 4371]
    starting_foot = "left"
    BOS_frame_x = construct_BOS_array(session_info.path_dict, BOS_frame_list, starting_foot)
    print(BOS_frame_x.shape)



if __name__ == "__main__": 
    main()