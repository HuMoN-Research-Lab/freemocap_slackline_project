import os
import numpy as np
from pathlib import Path

from construct_BOS_array import construct_BOS_array

class FreemocapSession:
    def __init__(self, session_id: str, freemocap_data_folder_path: Path):
        # check if dictionary exists in session folder
        # if dictionary exists, load it and set it to self.path_dict
        # if dictionary doesn't exist, run construct_path_dict
        self.construct_path_dict(session_id, freemocap_data_folder_path)


    def construct_path_dict(self, session_id: str, freemocap_data_folder_path: Path):
        self.path_dict = {}
        self.path_dict["session_id"] = session_id
        self.path_dict["freemocap_data_folder"] = freemocap_data_folder_path
        self.path_dict["session_folder"] = freemocap_data_folder_path / session_id
        self.path_dict["data_arrays_folder"] = self.path_dict["session_folder"] / "DataArrays"
        self.path_dict["synced_videos_folder"] = self.path_dict["session_folder"] / "SyncedVideos"
        self.path_dict["mediapipe_blender_rotated"] = self.path_dict["data_arrays_folder"] / "mediaPipeSkel_3d_filtered.npy"
        self.path_dict["total_body_COM_frame_xyz"] = self.path_dict["data_arrays_folder"] / "totalBodyCOM_frame_XYZ.npy"
        self.path_dict["segment_COM_frame_xyz"] = self.path_dict["data_arrays_folder"] / "segmentedCOM_frame_joint_XYZ.npy"

    def save_path_dict(self):
        path_dict_file_name = "session_path_dict.npy"
        path_dict_file_path = self.path_dict["session_folder"] / path_dict_file_name
        np.save(path_dict_file_path, self.path_dict)

    def construct_session_info_dict(self, BOS_frame_list: list, starting_foot: str, good_a_pose_frame_number: int):
        self.session_info_dict = {}
        self.session_info_dict["BOS_frame_list"] = BOS_frame_list
        self.session_info_dict["starting_foot"] = starting_foot
        self.session_info_dict["BOS_array"] = construct_BOS_array(self.path_dict, BOS_frame_list, starting_foot)
        self.session_info_dict["good_a_pose_frame_number"] = good_a_pose_frame_number



    


def main():
    session_id = "4stepsequence_session5_10_5_22"
    freemocap_data_folder_path = Path("/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data")
    session_info = FreemocapSession(session_id, freemocap_data_folder_path)
    session_info.save_path_dict()
    

if __name__ == "__main__":
    main()