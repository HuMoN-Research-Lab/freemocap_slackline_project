import math
import logging
import numpy as np
from pathlib import Path

from normalize_BOS_trajectories import normalize_BOS_trajectories
from utilities.pendulum_angles import get_virtual_pendulum_angle_array
from utilities.array_checks import check_arrays_have_same_shape, pad_array

logging.basicConfig(level = logging.INFO)

def get_state_information(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz, pendulum_angle_frame):
    '''
    Puts trajectories into state format to conform with the structure of ODEint, scipy's ODE solver
    [BOS location, BOS velocity, COM location, COM velocity, angle, angular velocity]
    '''
    BOS_frame_x = BOS_trajectories_frame_xyz[:,0]
    BOS_velocity = np.diff(pad_array(BOS_frame_x))

    com_frame_x = com_trajectories_frame_xyz[:,0]
    com_velocity = np.diff(pad_array(com_frame_x))
    logging.debug(f"Shape of pendulum angle array is: {pendulum_angle_frame.shape}")
    pendulum_velocity = np.diff(pad_array(pendulum_angle_frame))

    if check_arrays_have_same_shape([BOS_frame_x, BOS_velocity, com_frame_x, com_velocity, pendulum_angle_frame, pendulum_velocity]):
        state_information = []
        for frame in range(BOS_frame_x.shape[0]):
            this_frame_state = np.array([BOS_frame_x[frame], BOS_velocity[frame], com_frame_x[frame], com_velocity[frame], pendulum_angle_frame[frame], pendulum_velocity[frame]])
            state_information.append(this_frame_state)

        return np.array(state_information)

    else:
        logging.error("Input arrays must have same length")

def pendulum_arms_state_information(
    BOS_trajectories_frame_xyz: np.ndarray,
    pendulum_angle_frame: np.ndarray,
    arm_displacement_frame: np.ndarray,
    start_frame: int,
    end_frame: int
):
    '''
    Returns state information for a pendulum with arms
    q: [BOS location,  angle, arm displacement]
    qdot: [BOS velocity, angular velocity, arm velocity]
    qddot: [BOS acceleration, angular acceleration, arm acceleration]
    '''

    BOS_frame_x = BOS_trajectories_frame_xyz[:, 0]
    print(f"Shape of BOS frame x array is: {BOS_frame_x.shape}")
    BOS_velocity = np.diff(pad_array(BOS_frame_x))
    print(f"Shape of BOS velocity array is: {BOS_velocity.shape}")
    BOS_acceleration = np.diff(pad_array(BOS_velocity))
    print(f"Shape of BOS acceleration array is: {BOS_acceleration.shape}")

    print(f"Shape of pendulum angle array is: {pendulum_angle_frame.shape}")
    pendulum_velocity = np.diff(pad_array(pendulum_angle_frame))
    print(f"Shape of pendulum velocity array is: {pendulum_velocity.shape}")
    pendulum_acceleration = np.diff(pad_array(pendulum_velocity))
    print(f"Shape of pendulum acceleration array is: {pendulum_acceleration.shape}")

    print(f"Shape of arm displacement array is: {arm_displacement_frame.shape}")
    arm_velocity = np.diff(pad_array(arm_displacement_frame))
    print(f"Shape of arm velocity array is: {arm_velocity.shape}")
    arm_acceleration = np.diff(pad_array(arm_velocity))
    print(f"Shape of arm acceleration array is: {arm_acceleration.shape}")

    assert check_arrays_have_same_shape(
        [
            BOS_frame_x,
            BOS_velocity,
            BOS_acceleration,
            pendulum_angle_frame,
            pendulum_velocity,
            pendulum_acceleration,
            arm_displacement_frame,
            arm_velocity,
            arm_acceleration,
        ]
    ), "Input arrays must have same length"

    q = []
    qdot = []
    qddot = []
    for frame in range(start_frame, end_frame):
        this_frame_q = np.array(
            [
                BOS_frame_x[frame],
                pendulum_angle_frame[frame],
                arm_displacement_frame[frame],
            ]
        )
        q.append(this_frame_q)
        this_frame_qdot = np.array(
            [BOS_velocity[frame], pendulum_velocity[frame], arm_velocity[frame]]
        )
        qdot.append(this_frame_qdot)
        this_frame_qddot = np.array(
            [BOS_acceleration[frame], 
            pendulum_acceleration[frame],
            arm_acceleration[frame]]
        )
        qddot.append(this_frame_qddot)


    print(f"Shape of q array is: {np.array(q).shape}")
    print(f"Shape of qdot array is: {np.array(qdot).shape}")
    print(f"Shape of qddot array is: {np.array(qddot).shape}")
    return (np.array(q), np.array(qdot), np.array(qddot))

def pendulum_flywheel_state_information(
    BOS_trajectories_frame_xyz: np.ndarray,
    pendulum_angle_frame: np.ndarray,
    flywheel_inertia_frame: np.ndarray,
    start_frame: int,
    end_frame: int
):
    '''
    Returns state information for a pendulum with arms
    q: [BOS location,  angle, flywheel inertia]
    qdot: [BOS velocity, angular velocity, flywheel velocity]
    qddot: [BOS acceleration, angular acceleration, flywheel acceleration]
    '''

    BOS_frame_x = BOS_trajectories_frame_xyz[:, 0]
    print(f"Shape of BOS frame x array is: {BOS_frame_x.shape}")
    BOS_velocity = np.diff(pad_array(BOS_frame_x))
    print(f"Shape of BOS velocity array is: {BOS_velocity.shape}")
    BOS_acceleration = np.diff(pad_array(BOS_velocity))
    print(f"Shape of BOS acceleration array is: {BOS_acceleration.shape}")

    print(f"Shape of pendulum angle array is: {pendulum_angle_frame.shape}")
    pendulum_velocity = np.diff(pad_array(pendulum_angle_frame))
    print(f"Shape of pendulum velocity array is: {pendulum_velocity.shape}")
    pendulum_acceleration = np.diff(pad_array(pendulum_velocity))
    print(f"Shape of pendulum acceleration array is: {pendulum_acceleration.shape}")

    print(f"Shape of flywheel inertia array is: {flywheel_inertia_frame.shape}")
    flywheel_inertia_velocity = np.diff(pad_array(flywheel_inertia_frame))
    print(f"Shape of flywheel velocity array is: {flywheel_inertia_velocity.shape}")
    flywheel_inertia_acceleration = np.diff(pad_array(flywheel_inertia_velocity))
    print(f"Shape of flywheel acceleration array is: {flywheel_inertia_acceleration.shape}")

    assert check_arrays_have_same_shape(
        [
            BOS_frame_x,
            BOS_velocity,
            BOS_acceleration,
            pendulum_angle_frame,
            pendulum_velocity,
            pendulum_acceleration,
            flywheel_inertia_frame,
            flywheel_inertia_velocity,
            flywheel_inertia_acceleration,
        ]
    ), "Input arrays must have same length"

    q = []
    qdot = []
    qddot = []
    for frame in range(start_frame, end_frame):
        this_frame_q = np.array(
            [
                BOS_frame_x[frame],
                pendulum_angle_frame[frame],
                flywheel_inertia_frame[frame],
            ]
        )
        q.append(this_frame_q)
        this_frame_qdot = np.array(
            [BOS_velocity[frame], pendulum_velocity[frame], flywheel_inertia_velocity[frame]]
        )
        qdot.append(this_frame_qdot)
        this_frame_qddot = np.array(
            [BOS_acceleration[frame], 
            pendulum_acceleration[frame],
            flywheel_inertia_acceleration[frame]]
        )
        qddot.append(this_frame_qddot)


    print(f"Shape of q array is: {np.array(q).shape}")
    print(f"Shape of qdot array is: {np.array(qdot).shape}")
    print(f"Shape of qddot array is: {np.array(qddot).shape}")
    return (np.array(q), np.array(qdot), np.array(qddot))

def pendulum_flywheel_arms_state_information(
    BOS_trajectories_frame_xyz: np.ndarray,
    pendulum_angle_frame: np.ndarray,
    flywheel_inertia_frame: np.ndarray,
    arm_displacement_frame: np.ndarray,
    start_frame: int,
    end_frame: int
):
    '''
    Returns state information for a pendulum with arms
    q: [BOS location,  angle, arm displacement, flywheel inertia]
    qdot: [BOS velocity, angular velocity, arm velocity, flywheel velocity]
    qddot: [BOS acceleration, angular acceleration, arm acceleration, flywheel acceleration]
    '''

    BOS_frame_x = BOS_trajectories_frame_xyz[:, 0]
    print(f"Shape of BOS frame x array is: {BOS_frame_x.shape}")
    BOS_velocity = np.diff(pad_array(BOS_frame_x))
    print(f"Shape of BOS velocity array is: {BOS_velocity.shape}")
    BOS_acceleration = np.diff(pad_array(BOS_velocity))
    print(f"Shape of BOS acceleration array is: {BOS_acceleration.shape}")

    print(f"Shape of pendulum angle array is: {pendulum_angle_frame.shape}")
    pendulum_velocity = np.diff(pad_array(pendulum_angle_frame))
    print(f"Shape of pendulum velocity array is: {pendulum_velocity.shape}")
    pendulum_acceleration = np.diff(pad_array(pendulum_velocity))
    print(f"Shape of pendulum acceleration array is: {pendulum_acceleration.shape}")

    print(f"Shape of flywheel inertia array is: {flywheel_inertia_frame.shape}")
    flywheel_inertia_velocity = np.diff(pad_array(flywheel_inertia_frame))
    print(f"Shape of flywheel velocity array is: {flywheel_inertia_velocity.shape}")
    flywheel_inertia_acceleration = np.diff(pad_array(flywheel_inertia_velocity))
    print(f"Shape of flywheel acceleration array is: {flywheel_inertia_acceleration.shape}")

    print(f"Shape of arm displacement array is: {arm_displacement_frame.shape}")
    arm_velocity = np.diff(pad_array(arm_displacement_frame))
    print(f"Shape of arm velocity array is: {arm_velocity.shape}")
    arm_acceleration = np.diff(pad_array(arm_velocity))
    print(f"Shape of arm acceleration array is: {arm_acceleration.shape}")

    assert check_arrays_have_same_shape(
        [
            BOS_frame_x,
            BOS_velocity,
            BOS_acceleration,
            pendulum_angle_frame,
            pendulum_velocity,
            pendulum_acceleration,
            flywheel_inertia_frame,
            flywheel_inertia_velocity,
            flywheel_inertia_acceleration,
            arm_displacement_frame,
            arm_velocity,
            arm_acceleration,
        ]
    ), "Input arrays must have same length"

    q = []
    qdot = []
    qddot = []
    for frame in range(start_frame, end_frame):
        this_frame_q = np.array(
            [
                BOS_frame_x[frame],
                pendulum_angle_frame[frame],
                arm_displacement_frame[frame],
                flywheel_inertia_frame[frame],
            ]
        )
        q.append(this_frame_q)
        this_frame_qdot = np.array(
            [BOS_velocity[frame], 
            pendulum_velocity[frame], 
            arm_velocity[frame],
            flywheel_inertia_velocity[frame]]
        )
        qdot.append(this_frame_qdot)
        this_frame_qddot = np.array(
            [BOS_acceleration[frame], 
            pendulum_acceleration[frame],
            arm_acceleration[frame],
            flywheel_inertia_acceleration[frame]]
        )
        qddot.append(this_frame_qddot)


    print(f"Shape of q array is: {np.array(q).shape}")
    print(f"Shape of qdot array is: {np.array(qdot).shape}")
    print(f"Shape of qddot array is: {np.array(qddot).shape}")
    return (np.array(q), np.array(qdot), np.array(qddot))

def save_state_information(path_dict, state_information, start_frame, end_frame):
    save_name = path_dict["session_id"] + "_" + str(start_frame) + "_" + str(end_frame) + ".npy"
    save_path = path_dict["freemocap_data_folder"] / save_name
    
    np.save(save_path,state_information[start_frame:end_frame,:])
    logging.info(f"state information saved to file {save_path}")

def main():
    session_id="4stepsequence_session2_10_5_22"
    freemocap_data_folder_path=Path(
        "/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data"
    )

    start_frame = 2750
    end_frame = 3250 

    session_folder_path = freemocap_data_folder_path / session_id
    path_dict_file_name = "session_path_dict.npy"
    path_dict_file_path = session_folder_path / path_dict_file_name
    session_info_dict_name = "session_info_dict.npy"
    session_info_dict_path = session_folder_path / session_info_dict_name

    path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
    session_info_dict = np.load(session_info_dict_path, allow_pickle=True).item()

    BOS_trajectories_frame_xyz = session_info_dict["BOS_frame_xyz"]
    com_trajectories_frame_xyz = np.load(path_dict["total_body_COM_frame_xyz"])
    pendulum_angle_frame = get_virtual_pendulum_angle_array(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz)
    arm_displacement_frame = session_info_dict["arm_displacement_frame_x"]
    flywheel_inertia_frame = session_info_dict["flywheel_inertia_frame"]

    # comment this out if you don't want data shifted
    normalize_BOS_trajectories(BOS_trajectories_frame_xyz, start_frame, end_frame)


    # Simple State Information: 
    # state_information = get_state_information(BOS_trajectories_frame_xyz, com_trajectories_frame_xyz, pendulum_angle_frame)
    # np.save(session_folder_path / "state_information.npy", state_information)
    # logging.info(f"State information succesfully extracted to {session_folder_path / 'state_information.npy'}")

    # Pendulum with Arms:
    state_q, state_qdot, state_qddot = pendulum_arms_state_information(
        BOS_trajectories_frame_xyz, pendulum_angle_frame, arm_displacement_frame, start_frame, end_frame
    )
    np.save(session_folder_path / "pendulum_arms_state_q.npy", state_q)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_q.npy'}"
    )
    np.save(session_folder_path / "pendulum_arms_state_qdot.npy", state_qdot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_qdot.npy'}"
    )
    np.save(session_folder_path / "pendulum_arms_state_qddot.npy", state_qddot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_qddot.npy'}"
    )

    # Pendulum with Flywheel:
    state_q, state_qdot, state_qddot = pendulum_flywheel_state_information(
        BOS_trajectories_frame_xyz, pendulum_angle_frame, flywheel_inertia_frame, start_frame, end_frame
    )
    np.save(session_folder_path / "pendulum_flywheel_state_q.npy", state_q)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_q.npy'}"
    )
    np.save(session_folder_path / "pendulum_flywheel_state_qdot.npy", state_qdot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_qdot.npy'}"
    )
    np.save(session_folder_path / "pendulum_flywheel_state_qddot.npy", state_qddot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_qddot.npy'}"
    )

    # Pendulum with Arms and Flywheel:
    state_q, state_qdot, state_qddot = pendulum_flywheel_arms_state_information(
        BOS_trajectories_frame_xyz, pendulum_angle_frame, flywheel_inertia_frame, arm_displacement_frame, start_frame, end_frame
    )
    np.save(session_folder_path / "pendulum_flywheel_arms_state_q.npy", state_q)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_q.npy'}"
    )
    np.save(session_folder_path / "pendulum_flywheel_arms_state_qdot.npy", state_qdot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_qdot.npy'}"
    )
    np.save(session_folder_path / "pendulum_flywheel_arms_state_qddot.npy", state_qddot)
    logging.info(
        f"State information succesfully extracted to {session_folder_path / 'state_qddot.npy'}"
    )



if __name__ == "__main__":
    main()
