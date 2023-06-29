from statistics import mean, stdev
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import cv2
from pathlib import Path


class ArmCOMPlots:
    def __init__(self, session_data_dict, session_path_dict, start_frame):
        self.session_data_dict = session_data_dict
        self.session_path_dict = session_path_dict
        self.start_frame = start_frame

        self.total_body_com_frame_xyz = np.load(self.session_path_dict["total_body_COM_frame_xyz"])

    def create_plots(self):
        # parameters:
        self.fps = 60
        self.length_of_data_seconds = 15
        self.length_of_data_frames = self.length_of_data_seconds * self.fps
        self.initial_offset_seconds = 0
        self.initial_offset_frames = self.initial_offset_seconds * self.fps

        self.initialize_figure()
        self.create_subplot1()
        self.create_subplot2()
        self.create_subplot3()

    def initialize_figure(self):
        self.fig = plt.figure(constrained_layout=True)
        self.fig.set_size_inches(7, 8)
        # self.fig.set_dpi(300)
        self.spec = self.fig.add_gridspec(
            3, 1
        )  # gridspec allows us to have one plot span multiple plot grids

        self.fig.suptitle(f"Arm COM vs total body COM")

    def create_subplot1(self):
        self.ax1 = self.fig.add_subplot(self.spec[0, 0])

        self.ax1.set_title("X values")
        self.ax1.set_xlabel(f"Time (frames)")
        self.ax1.set_ylabel(f"X value [mm]")

        axis_index = 0

        start_frame = self.start_frame + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        self.ax1.plot(self.session_data_dict["arm_com_frame_xyz"][start_frame:, axis_index])
        self.ax1.plot(self.total_body_com_frame_xyz[start_frame:, axis_index])

    def create_subplot2(self):
        self.ax2 = self.fig.add_subplot(self.spec[1, 0])

        self.ax2.set_title("Y values")
        self.ax2.set_xlabel(f"Time (frames)")
        self.ax2.set_ylabel(f"Y value [mm]")

        axis_index = 1

        start_frame = self.start_frame + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        self.ax2.plot(self.session_data_dict["arm_com_frame_xyz"][start_frame:, axis_index])
        self.ax2.plot(self.total_body_com_frame_xyz[start_frame:, axis_index])

    def create_subplot3(self):
        self.ax3 = self.fig.add_subplot(self.spec[2, 0])

        self.ax3.set_title("Z values")
        self.ax3.set_xlabel(f"Time (frames)")
        self.ax3.set_ylabel(f"Z value [mm]")

        axis_index = 2

        start_frame = self.start_frame + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        self.ax3.plot(self.session_data_dict["arm_com_frame_xyz"][start_frame:, axis_index])
        self.ax3.plot(self.total_body_com_frame_xyz[start_frame:, axis_index])


def main():
    freemocap_data_folder_path = Path(
        "/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data"
    )
    session_id = session_id = "4stepsequence_session5_10_5_22"

    if session_id == "4stepsequence_session2_10_5_22":
        start_frame = 2400
    elif session_id == "4stepsequence_session3_10_5_22":
        start_frame = 3900
    elif session_id == "4stepsequence_session4_10_5_22":
        start_frame = 3450
    elif session_id == "4stepsequence_session5_10_5_22":
        start_frame = 3540

    session_folder_path = freemocap_data_folder_path / session_id
    path_dict_file_name = "session_path_dict.npy"
    path_dict_file_path = session_folder_path / path_dict_file_name
    session_info_dict_name = "session_info_dict.npy"
    session_info_dict_path = session_folder_path / session_info_dict_name

    path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
    session_info_dict = np.load(session_info_dict_path, allow_pickle=True).item()

    slack_plots = ArmCOMPlots(
        session_data_dict=session_info_dict,
        session_path_dict=path_dict,
        start_frame=start_frame,
    )
    slack_plots.create_plots()
    plt.show()


if __name__ == "__main__":
    main()
