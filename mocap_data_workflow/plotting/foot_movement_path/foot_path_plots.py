from statistics import mean, stdev
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import cv2
from pathlib import Path

class LeftFootPlots:
    def __init__(self):
        pass

    def create_plots(self):
        # load in all of the data
        # set session folder path
        self.freemocap_data_path = Path("/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data")
        self.session2_id = "4stepsequence_session2_10_5_22"
        self.session3_id = "4stepsequence_session3_10_5_22"
        self.session4_id = "4stepsequence_session4_10_5_22"
        self.session5_id = "4stepsequence_session5_10_5_22"

        self.session3_info_dict = self.load_data(self.freemocap_data_path, self.session3_id)
        self.session4_info_dict = self.load_data(self.freemocap_data_path, self.session4_id)
        self.session2_info_dict = self.load_data(self.freemocap_data_path, self.session2_id)
        self.session5_info_dict = self.load_data(self.freemocap_data_path, self.session5_id)

        #parameters:
        self.fps = 60
        self.length_of_data_seconds = 15
        self.length_of_data_frames = self.length_of_data_seconds * self.fps
        self.initial_offset_seconds = 0
        self.initial_offset_frames = self.initial_offset_seconds * self.fps


        self.initialize_figure()
        self.create_subplot1(self.session2_info_dict)
        self.create_subplot2(self.session3_info_dict)
        self.create_subplot3(self.session4_info_dict)
        self.create_subplot4(self.session5_info_dict)


    def load_data(self, freemocap_data_path, session):
        session_folder_path = freemocap_data_path / session
        info_dict_file_path = session_folder_path / "session_info_dict.npy"

        # load base of support data based on which foot I'm standing on
        if session == "4stepsequence_session2_10_5_22":
            start_frame = 2400
            info_dict = np.load(info_dict_file_path, allow_pickle=True).item()
        elif session == "4stepsequence_session3_10_5_22":
            start_frame = 3900
            info_dict = np.load(info_dict_file_path, allow_pickle=True).item()
        elif session == "4stepsequence_session4_10_5_22":
            start_frame = 3450
            info_dict = np.load(info_dict_file_path, allow_pickle=True).item()
        elif session == "4stepsequence_session5_10_5_22":
            start_frame = 3540
            info_dict = np.load(info_dict_file_path, allow_pickle=True).item()

        info_dict["start_frame"] = start_frame

        return info_dict

    def initialize_figure(self):
        self.fig = plt.figure(constrained_layout=True)
        self.fig.set_size_inches(7,8)
        #self.fig.set_dpi(300)
        self.spec = self.fig.add_gridspec(2, 2) # gridspec allows us to have one plot span multiple plot grids

        self.fig.suptitle(f'Foot Motion Patterns \nFor Left Foot Standing on a Slackline for {self.length_of_data_seconds} Seconds')

    def create_subplot1(self, session_data_dict):
        self.ax1 = self.fig.add_subplot(self.spec[0, 0]) 
        self.ax1.set_aspect('equal')
        self.ax1.set_adjustable('box')


        self.ax1.set_title("Session 2 (Subject 2)")
        self.ax1.set_xlabel(f"Base of Support X [mm]")
        self.ax1.set_ylabel(f"Base of Support Z [mm]")


        start_frame = session_data_dict["start_frame"] + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        self.plot_foot_movement_shadow, = self.ax1.plot(session_data_dict["BOS_frame_xyz"][start_frame:end_frame, 0], session_data_dict["BOS_frame_xyz"][start_frame:end_frame, 2], zorder=1, color="plum")

        self.ax1.set_aspect('equal', adjustable='box')

        x_limits = self.ax1.get_xlim()
        y_limits = self.ax1.get_ylim()

        x_range = x_limits[1] - x_limits[0]
        y_range = y_limits[1] - y_limits[0]

        max_range = max(x_range, y_range)

        x_new_limits = ((x_limits[0] + x_limits[1] - max_range) / 2, (x_limits[0] + x_limits[1] + max_range) / 2)
        y_new_limits = ((y_limits[0] + y_limits[1] - max_range) / 2, (y_limits[0] + y_limits[1] + max_range) / 2)

        self.ax1.set_xlim(x_new_limits)
        self.ax1.set_ylim(y_new_limits)

    def create_subplot2(self, session_data_dict):
        self.ax2 = self.fig.add_subplot(self.spec[0, 1]) 

        self.ax2.set_title("Session 3 (Subject 3)")
        self.ax2.set_xlabel(f"Base of Support X [mm]")
        self.ax2.set_ylabel(f"Base of Support Z [mm]")

        start_frame = session_data_dict["start_frame"] + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        self.plot_foot_movement_shadow, = self.ax2.plot(session_data_dict["BOS_frame_xyz"][start_frame:end_frame, 0], session_data_dict["BOS_frame_xyz"][start_frame:end_frame, 2], zorder=1, color="plum")

        self.ax2.set_aspect('equal', adjustable='box')

        x_limits = self.ax2.get_xlim()
        y_limits = self.ax2.get_ylim()

        x_range = x_limits[1] - x_limits[0]
        y_range = y_limits[1] - y_limits[0]

        max_range = max(x_range, y_range)

        x_new_limits = ((x_limits[0] + x_limits[1] - max_range) / 2, (x_limits[0] + x_limits[1] + max_range) / 2)
        y_new_limits = ((y_limits[0] + y_limits[1] - max_range) / 2, (y_limits[0] + y_limits[1] + max_range) / 2)

        self.ax2.set_xlim(x_new_limits)
        self.ax2.set_ylim(y_new_limits)

    def create_subplot3(self, session_data_dict):
        self.ax3 = self.fig.add_subplot(self.spec[1, 0]) 


        self.ax3.set_title("Session 4 (subject 3)")
        self.ax3.set_xlabel(f"Base of Support X [mm]")
        self.ax3.set_ylabel(f"Base of Support Z [mm]")

        start_frame = session_data_dict["start_frame"] + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        self.plot_foot_movement_shadow, = self.ax3.plot(session_data_dict["BOS_frame_xyz"][start_frame:end_frame, 0], session_data_dict["BOS_frame_xyz"][start_frame:end_frame, 2], zorder=1, color="plum")

        self.ax3.set_aspect('equal', adjustable='box')

        x_limits = self.ax3.get_xlim()
        y_limits = self.ax3.get_ylim()

        x_range = x_limits[1] - x_limits[0]
        y_range = y_limits[1] - y_limits[0]

        max_range = max(x_range, y_range)

        x_new_limits = ((x_limits[0] + x_limits[1] - max_range) / 2, (x_limits[0] + x_limits[1] + max_range) / 2)
        y_new_limits = ((y_limits[0] + y_limits[1] - max_range) / 2, (y_limits[0] + y_limits[1] + max_range) / 2)

        self.ax3.set_xlim(x_new_limits)
        self.ax3.set_ylim(y_new_limits)

    def create_subplot4(self, session_data_dict):
        self.ax4 = self.fig.add_subplot(self.spec[1, 1])

        self.ax4.set_title("Session 5 (Subject 4)")
        self.ax4.set_xlabel(f"Base of Support X [mm]")
        self.ax4.set_ylabel(f"Base of Support Z [mm]")

        start_frame = session_data_dict["start_frame"] + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        self.plot_foot_movement_shadow, = self.ax4.plot(session_data_dict["BOS_frame_xyz"][start_frame:end_frame, 0], session_data_dict["BOS_frame_xyz"][start_frame:end_frame, 2], zorder=1, color="plum")

        self.ax4.set_aspect('equal', adjustable='box')

        x_limits = self.ax4.get_xlim()
        y_limits = self.ax4.get_ylim()

        x_range = x_limits[1] - x_limits[0]
        y_range = y_limits[1] - y_limits[0]

        max_range = max(x_range, y_range)

        x_new_limits = ((x_limits[0] + x_limits[1] - max_range) / 2, (x_limits[0] + x_limits[1] + max_range) / 2)
        y_new_limits = ((y_limits[0] + y_limits[1] - max_range) / 2, (y_limits[0] + y_limits[1] + max_range) / 2)

        self.ax4.set_xlim(x_new_limits)
        self.ax4.set_ylim(y_new_limits)


def main():
    slack_plots = LeftFootPlots()
    slack_plots.create_plots()
    plt.show()


if __name__ == "__main__":
    main()