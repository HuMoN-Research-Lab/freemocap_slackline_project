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

        self.session2_data_dict = self.load_data(self.freemocap_data_path, self.session2_id)
        self.session3_data_dict = self.load_data(self.freemocap_data_path, self.session3_id)
        self.session4_data_dict = self.load_data(self.freemocap_data_path, self.session4_id)
        self.session5_data_dict = self.load_data(self.freemocap_data_path, self.session5_id)

        #parameters:
        self.fps = 60
        self.length_of_data_seconds = 15
        self.length_of_data_frames = self.length_of_data_seconds * self.fps
        self.initial_offset_seconds = 0
        self.initial_offset_frames = self.initial_offset_seconds * self.fps

        self.axis_of_interest = "Z"
        if self.axis_of_interest == "X":
            self.axis_index = 0
        if self.axis_of_interest == "Y":
            self.axis_index = 1
        if self.axis_of_interest == "Z":
            self.axis_index = 2


        self.initialize_figure()
        self.create_subplot1(self.session2_data_dict)
        self.create_subplot2(self.session3_data_dict)
        self.create_subplot3(self.session4_data_dict)
        self.create_subplot4(self.session5_data_dict)


    def load_data(self, freemocap_data_path, session):
        session_folder_path = freemocap_data_path / session
        data_arrays_path = session_folder_path / "DataArrays"

        # get 3d skeleton data path and load it
        mediapipe_file_name = "mediaPipeSkel_3d_origin_aligned.npy"
        mediapipe_3d_data_path = data_arrays_path / mediapipe_file_name
        skeleton_frame_joint_xyz = np.load(mediapipe_3d_data_path)

        left_hand_frame_xyz = skeleton_frame_joint_xyz[:,15,:]
        right_hand_frame_xyz = skeleton_frame_joint_xyz[:,16,:]

        # create base of support data based on which foot I'm standing on
        #! this has to be changed for each video
        if session == "4stepsequence_session2_10_5_22":
            start_frame = 2400
        elif session == "4stepsequence_session3_10_5_22":
            start_frame = 3900
        elif session == "4stepsequence_session4_10_5_22":
            start_frame = 3450
        elif session == "4stepsequence_session5_10_5_22":
            start_frame = 3540

        session_data_dict = {"left_hand_frame_xyz": left_hand_frame_xyz,
                             "right_hand_frame_xyz": right_hand_frame_xyz,
                             "start_frame": start_frame}

        return session_data_dict

    def initialize_figure(self):
        self.fig = plt.figure(constrained_layout=True)
        self.fig.set_size_inches(7,8)
        #self.fig.set_dpi(300)
        self.spec = self.fig.add_gridspec(2, 2) # gridspec allows us to have one plot span multiple plot grids

        self.fig.suptitle(f'Hand Motion Patterns \nFor Left Foot Standing on a Slackline for {self.length_of_data_seconds} Seconds')

    def create_subplot1(self, session_data_dict):
        self.ax1 = self.fig.add_subplot(self.spec[0, 0]) 

        self.ax1.set_title("Session 2 (Subject 2)")
        self.ax1.set_xlabel(f"Right Hand {self.axis_of_interest} [mm]")
        self.ax1.set_ylabel(f"Left Hand {self.axis_of_interest} [mm]")

        start_frame = session_data_dict["start_frame"] + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        #! this needs to be changed for each video
        self.plot_state_space_shadow, = self.ax1.plot(session_data_dict["right_hand_frame_xyz"][start_frame:end_frame, self.axis_index], session_data_dict["left_hand_frame_xyz"][start_frame:end_frame, self.axis_index], zorder=1, color="plum")

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
        self.ax2.set_xlabel(f"Right Hand {self.axis_of_interest} [mm]")
        self.ax2.set_ylabel(f"Left Hand {self.axis_of_interest} [mm]")

        start_frame = session_data_dict["start_frame"] + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        #! this needs to be changed for each video
        self.plot_state_space_shadow, = self.ax2.plot(session_data_dict["right_hand_frame_xyz"][start_frame:end_frame, self.axis_index], session_data_dict["left_hand_frame_xyz"][start_frame:end_frame, self.axis_index], zorder=1, color="plum")

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
        self.ax3.set_xlabel(f"Right Hand {self.axis_of_interest} [mm]")
        self.ax3.set_ylabel(f"Left Hand {self.axis_of_interest} [mm]")

        start_frame = session_data_dict["start_frame"] + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        #! this needs to be changed for each video
        self.plot_state_space_shadow, = self.ax3.plot(session_data_dict["right_hand_frame_xyz"][start_frame:end_frame, self.axis_index], session_data_dict["left_hand_frame_xyz"][start_frame:end_frame, self.axis_index], zorder=1, color="plum")

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
        self.ax4.set_xlabel(f"Right Hand {self.axis_of_interest} [mm]")
        self.ax4.set_ylabel(f"Left Hand {self.axis_of_interest} [mm]")

        start_frame = session_data_dict["start_frame"] + self.initial_offset_frames
        end_frame = start_frame + self.length_of_data_frames

        self.plot_state_space_shadow, = self.ax4.plot(session_data_dict["right_hand_frame_xyz"][start_frame:end_frame, self.axis_index], session_data_dict["left_hand_frame_xyz"][start_frame:end_frame, self.axis_index], zorder=1, color="plum")
 
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