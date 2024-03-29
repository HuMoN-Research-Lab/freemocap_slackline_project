import logging
import numpy as np
from pathlib import Path

from extract_state_information import (
    get_state_information,
    get_virtual_pendulum_angle_array,
    save_state_information,
    pendulum_arms_state_information,
)

logging.basicConfig(level=logging.INFO)

"""Gets session data using session_read_in.py, and puts it into any processing/visualizing functions"""


def main(session_id, freemocap_data_folder_path):
    session_folder_path = freemocap_data_folder_path / session_id
    path_dict_file_name = "session_path_dict.npy"
    path_dict_file_path = session_folder_path / path_dict_file_name
    session_info_dict_name = "session_info_dict.npy"
    session_info_dict_path = session_folder_path / session_info_dict_name

    path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
    session_info_dict = np.load(session_info_dict_path, allow_pickle=True).item()

    # simple cartpole state information:
    # BOS_trajectories_frame_xyz = session_info_dict["BOS_frame_xyz"]
    # com_trajectories_frame_xyz = np.load(path_dict["total_body_COM_frame_xyz"])
    # pendulum_angle_frame = get_virtual_pendulum_angle_array(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz)

    # state_information = get_state_information(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz, pendulum_angle_frame)
    # logging.info("State information succesfully extracted")
    # logging.info("Saving state information...")
    # save_state_information(path_dict, state_information, start_frame=2350, end_frame=3301)

    # pendulum arms state information:
    BOS_trajectories_frame_xyz = session_info_dict["BOS_frame_xyz"]
    com_trajectories_frame_xyz = np.load(path_dict["total_body_COM_frame_xyz"])
    pendulum_angle_frame = get_virtual_pendulum_angle_array(
        BOS_trajectories_frame_xyz, com_trajectories_frame_xyz
    )
    arm_displacement_frame = session_info_dict["arm_displacement_frame_x"]

    (state_q, state_qdot, state_qddot) = pendulum_arms_state_information(
        BOS_trajectories_frame_xyz, pendulum_angle_frame, arm_displacement_frame
    )
    np.save(session_folder_path / "pendulum_arms_state_q.npy", state_q)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'pendulum_arms_state_q.npy'}"
    )
    np.save(session_folder_path / "pendulum_arms_state_qdot.npy", state_qdot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'pendulum_arms_state_qdot.npy'}"
    )
    np.save(session_folder_path / "pendulum_arms_state_qddot.npy", state_qddot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'pendulum_arms_state_qddot.npy'}"
    )


if __name__ == "__main__":
    main(
        session_id="4stepsequence_session2_10_5_22",
        freemocap_data_folder_path=Path(
            "/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data"
        ),
    )
