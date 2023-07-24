import logging
import numpy as np
from pathlib import Path

from construct_arm_displacement_frame_x import (
    construct_arm_displacement_frame_x,
    calculate_arm_center_of_mass,
)
from construct_BOS_frame_xyz import construct_BOS_frame_xyz
from construct_inertia_frame import construct_inertia_frame
from session_setup_info.session_setup_info import (
    session_2_setup_dict,
    session_3_setup_dict,
    session_4_setup_dict,
    session_5_setup_dict
)


logging.basicConfig(level=logging.INFO)


class FreemocapSession:
    def __init__(self, session_id: str, freemocap_data_folder_path: Path):
        self.session_folder_path = freemocap_data_folder_path / session_id
        self.session_path_dict_name = "session_path_dict.npy"
        self.session_info_dict_name = "session_info_dict.npy"

        self.path_dict_file_path = (
            self.session_folder_path / self.session_path_dict_name
        )
        self.session_info_dict_path = (
            self.session_folder_path / self.session_info_dict_name
        )

        if self.path_dict_file_path.exists():
            logging.info("loading pre-saved path dictionary...")
            self.load_path_dict(self.path_dict_file_path)
        else:
            logging.info("creating path dictionary...")
            self.construct_path_dict(session_id, freemocap_data_folder_path)
            logging.info("saving path dictionary to file...")
            self.save_path_dict(self.path_dict_file_path)

    def construct_path_dict(self, session_id: str, freemocap_data_folder_path: Path):
        logging.info("creating path dictionary")
        self.path_dict = {}
        self.path_dict["session_id"] = session_id
        self.path_dict["freemocap_data_folder"] = freemocap_data_folder_path
        self.path_dict["session_folder"] = freemocap_data_folder_path / session_id
        self.path_dict["data_arrays_folder"] = (
            self.path_dict["session_folder"] / "DataArrays"
        )
        self.path_dict["synced_videos_folder"] = (
            self.path_dict["session_folder"] / "SyncedVideos"
        )
        self.path_dict["mediapipe_blender_rotated"] = (
            self.path_dict["data_arrays_folder"] / "mediaPipeSkel_3d_filtered.npy"
        )
        self.path_dict["total_body_COM_frame_xyz"] = (
            self.path_dict["data_arrays_folder"] / "totalBodyCOM_frame_XYZ.npy"
        )
        self.path_dict["segment_COM_frame_xyz"] = (
            self.path_dict["data_arrays_folder"] / "segmentedCOM_frame_joint_XYZ.npy"
        )

    def save_path_dict(self, path_dict_file_path):
        np.save(path_dict_file_path, self.path_dict)
        logging.info("path dictionary saved")

    def load_path_dict(self, path_dict_file_path):
        self.path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
        logging.info("path dictionary saved")

    def construct_session_info_dict(
        self, BOS_frame_list: list, starting_foot: str, good_a_pose_frame_number: int
    ):
        logging.info("creating info dictionary")
        self.session_info_dict = {}
        self.session_info_dict["BOS_frame_list"] = BOS_frame_list
        self.session_info_dict["starting_foot"] = starting_foot
        self.session_info_dict["BOS_frame_xyz"] = construct_BOS_frame_xyz(
            self.path_dict, BOS_frame_list, starting_foot
        )
        self.session_info_dict["good_a_pose_frame_number"] = good_a_pose_frame_number
        self.session_info_dict["arm_com_frame_xyz"] = calculate_arm_center_of_mass(
            np.load(self.path_dict["segment_COM_frame_xyz"])
        )
        self.session_info_dict[
            "arm_displacement_frame_x"
        ] = construct_arm_displacement_frame_x(self.path_dict)
        self.session_info_dict["flywheel_inertia_frame"] = construct_inertia_frame(
            self.path_dict
        )

    def save_info_dict(self, session_info_dict_file_path):
        np.save(session_info_dict_file_path, self.session_info_dict)
        logging.info("info dictionary saved")

    def load_info_dict(self, session_info_dict_file_path):
        self.session_info_dict = np.load(
            session_info_dict_file_path, allow_pickle=True
        ).item()
        logging.info("info dictionary loaded")


def main():
    session_setup_dict = session_2_setup_dict
    session_id = session_setup_dict["session_id"]
    freemocap_data_folder_path = session_setup_dict["freemocap_data_folder_path"]
    session_info = FreemocapSession(session_id, freemocap_data_folder_path)

    BOS_frame_list = session_setup_dict["BOS_frame_list"]
    starting_foot = session_setup_dict["starting_foot"]
    good_a_pose_frame_number = session_setup_dict["good_a_pose_frame_number"]
    session_info.construct_session_info_dict(
        BOS_frame_list, starting_foot, good_a_pose_frame_number
    )
    session_info.save_info_dict(session_info.session_info_dict_path)


if __name__ == "__main__":
    main()
