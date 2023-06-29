import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
from pathlib import Path

class SimpleSkeletonAnimation:

    def __init__(self, session_folder_path,skeleton_data, additional_points):
        self.session_folder_path = session_folder_path

        self.animation_path = self.session_folder_path / "simple_skeleton_animation.mp4"

        self.additional_points = additional_points

        self.skel_fr_mar_xyz = skeleton_data

        # mediapipe has 33 pose markers for the body
        self.num_pose_markers = 33

        # define video parameters
        self.number_of_frames = self.skel_fr_mar_xyz.shape[0]
        self.frame_interval = 16.6667 # this corresponds to 60fps, and will eventually be inherited as part of fmc pipeline

        # define skeleton connections for drawing
        self.skeleton_connection_dict = {
            "eyes": [8, 6, 5, 4, 0, 1, 2, 3, 7],
            "mouth": [10, 9],
            "torso": [11, 23, 24, 12, 11], #repeated start values to close loop
            "rArm": [12, 14, 16],
            "lArm": [11, 13, 15],
            "rHand": [16, 18, 20, 16, 22], #repeated start values to close loop
            "lHand": [15, 17, 19, 15, 21], #repeated start values to close loop
            "rLeg": [24, 26, 28],
            "lLeg": [23, 25, 27],
            "rFoot": [28, 30, 32, 28], #repeated start values to close loop
            "lFoot": [27, 29, 31, 27], #repeated start values to close loop
        }

        # set up figure:
        self.fig = plt.figure(constrained_layout=True)
        self.fig.set_size_inches(7, 7)
        self.fig.suptitle('FreeMoCap')

        # create first axis
        self.ax1 = self.fig.add_subplot(111, projection='3d')
        self.title = self.ax1.set_title('Full Extent')
        self.ax1.set_xlabel("X")
        self.ax1.set_ylabel("Y")
        self.ax1.set_zlabel("Z")
        # uncomment to remove axis tick labels
        # self.ax1.set_xticklabels([])
        # self.ax1.set_yticklabels([])
        # self.ax1.set_zticklabels([])

        # set axis limits:
        ax1_limit_dict = self.get_ax_limits(scale_factor = 2)

        self.ax1.set_xlim(ax1_limit_dict['x_min'], ax1_limit_dict['x_max'])
        self.ax1.set_ylim(ax1_limit_dict['y_min'], ax1_limit_dict['y_max'])
        self.ax1.set_zlim(ax1_limit_dict['z_min'], ax1_limit_dict['z_max'])  

        # initialize skeleton within figure:
        # create spatial variables
        self.tracked_point_x, self.tracked_point_y, self.tracked_point_z = self.get_frame_data(0, self.skel_fr_mar_xyz)
        additional_point_x, additional_point_y, additional_point_z = self.additional_points[0]

        # plot initial joint data
        self.tracked_point_graph = self.ax1.scatter(self.tracked_point_x, self.tracked_point_y, self.tracked_point_z, color="salmon") #plots all 33 tracked points from mediapipe

        self.additional_point_graph = self.ax1.scatter([additional_point_x], [additional_point_y], [additional_point_z], color="green")

        # plot initial skeleton data
        self.create_initial_skeleton(self.tracked_point_x, self.tracked_point_y, self.tracked_point_z)

    def get_ax_limits(self, scale_factor):
        '''Finds dictionary of axis limits based around a certain number of standard deviations (set by scale factor) from the median.'''
        # get median position
        self.median_pose_across_frames = np.nanmedian(self.skel_fr_mar_xyz[:, :self.num_pose_markers, :], axis = 0)
        self.median_pose_global = np.nanmedian(self.median_pose_across_frames, axis = 0)

        self.median_body_x = self.median_pose_global[0]
        self.median_body_y = self.median_pose_global[1]
        self.median_body_z = self.median_pose_global[2]

        # get max and min values for x,y,zlim
        self.skel_pose_stddev = np.nanstd(self.skel_fr_mar_xyz[:, :self.num_pose_markers, :], axis = (0,1,2))

        ax_limits_dict = {}

        ax_limits_dict['x_max'] = self.median_body_x + scale_factor * self.skel_pose_stddev
        ax_limits_dict['y_max'] = self.median_body_y + scale_factor * self.skel_pose_stddev
        ax_limits_dict['z_max'] = self.median_body_z + scale_factor * self.skel_pose_stddev

        ax_limits_dict['x_min'] = self.median_body_x - scale_factor * self.skel_pose_stddev
        ax_limits_dict['y_min'] = self.median_body_y - scale_factor * self.skel_pose_stddev
        ax_limits_dict['z_min'] = self.median_body_z - scale_factor * self.skel_pose_stddev

        return ax_limits_dict

    def get_frame_data(self, frame, mediapipe_skel_fr_mar_xyz):
        '''Given a frame number, get 3 arrays containing x, y, z data'''
        single_frame_x_data = []
        single_frame_y_data = []
        single_frame_z_data = []

        for tracked_point in mediapipe_skel_fr_mar_xyz[frame][:33]: #only interested in 33 body points, not hand and face points
            single_frame_x_data.append(tracked_point[0]) 
            single_frame_y_data.append(tracked_point[1])
            single_frame_z_data.append(tracked_point[2])
            
        return single_frame_x_data, single_frame_y_data, single_frame_z_data
    

    def body_segment_data(self, x, y, z, segment_key):
        '''Creates body segment data for a body segment given by the segment_key, based on the joints given in the skeleton_connection_dict.
        Returns separate XYZ lists, as packed tuple, in proper format for plotting.'''
        x_connections, y_connections, z_connections = [], [], []

        for joint in self.skeleton_connection_dict[segment_key]:
            x_connections.append(x[joint])
            y_connections.append(y[joint])
            z_connections.append(z[joint])

        return x_connections, y_connections, z_connections

    def create_initial_skeleton(self, x, y, z):
        # create eyes
        eyes_x, eyes_y, eyes_z = self.body_segment_data(x, y, z, "eyes")
        self.eye_line, = self.ax1.plot(eyes_x, eyes_y, eyes_z, color = "cornflowerblue")

        # create mouth
        mouth_x, mouth_y, mouth_z = self.body_segment_data(x, y, z, "mouth")
        self.mouth_line, = self.ax1.plot(mouth_x, mouth_y, mouth_z, color = "cornflowerblue")

        # create torso
        torso_x, torso_y, torso_z = self.body_segment_data(x, y, z, "torso")
        self.torso_line, = self.ax1.plot(torso_x, torso_y, torso_z, color = "cornflowerblue")

        # create arms
        rArm_x, rArm_y, rArm_z = self.body_segment_data(x, y, z, "rArm")
        self.rArm_line, = self.ax1.plot(rArm_x, rArm_y, rArm_z, color = "cornflowerblue")

        lArm_x, lArm_y, lArm_z = self.body_segment_data(x, y, z, "lArm")
        self.lArm_line, = self.ax1.plot(lArm_x, lArm_y, lArm_z, color = "cornflowerblue")

        # create hands
        rHand_x, rHand_y, rHand_z = self.body_segment_data(x, y, z, "rHand")
        self.rHand_line, = self.ax1.plot(rHand_x, rHand_y, rHand_z, color = "cornflowerblue")

        lHand_x, lHand_y, lHand_z = self.body_segment_data(x, y, z, "lHand")
        self.lHand_line, = self.ax1.plot(lHand_x, lHand_y, lHand_z, color = "cornflowerblue")

        # create legs
        rLeg_x, rLeg_y, rLeg_z = self.body_segment_data(x, y, z, "rLeg")
        self.rLeg_line, = self.ax1.plot(rLeg_x, rLeg_y, rLeg_z, color = "cornflowerblue")

        lLeg_x, lLeg_y, lLeg_z = self.body_segment_data(x, y, z, "lLeg")
        self.lLeg_line, = self.ax1.plot(lLeg_x, lLeg_y, lLeg_z, color = "cornflowerblue")

        # create feet
        rFoot_x, rFoot_y, rFoot_z = self.body_segment_data(x, y, z, "rFoot")
        self.rFoot_line, = self.ax1.plot(rFoot_x, rFoot_y, rFoot_z, color = "cornflowerblue")

        lFoot_x, lFoot_y, lFoot_z = self.body_segment_data(x, y, z, "lHand")
        self.lFoot_line, = self.ax1.plot(lFoot_x, lFoot_y, lFoot_z, color = "cornflowerblue")


    def update_skeleton(self, x, y, z):
        # update eyes
        eyes_x, eyes_y, eyes_z = self.body_segment_data(x, y, z, "eyes")
        self.eye_line.set_data_3d(eyes_x, eyes_y, eyes_z)

        # update mouth
        mouth_x, mouth_y, mouth_z = self.body_segment_data(x, y, z, "mouth")
        self.mouth_line.set_data_3d(mouth_x, mouth_y, mouth_z)

        # update torso
        torso_x, torso_y, torso_z = self.body_segment_data(x, y, z, "torso")
        self.torso_line.set_data_3d(torso_x, torso_y, torso_z)

        # update arms
        rArm_x, rArm_y, rArm_z = self.body_segment_data(x, y, z, "rArm")
        self.rArm_line.set_data_3d(rArm_x, rArm_y, rArm_z)

        lArm_x, lArm_y, lArm_z = self.body_segment_data(x, y, z, "lArm")
        self.lArm_line.set_data_3d(lArm_x, lArm_y, lArm_z)

        # update hands
        rHand_x, rHand_y, rHand_z = self.body_segment_data(x, y, z, "rHand")
        self.rHand_line.set_data_3d(rHand_x, rHand_y, rHand_z)

        lHand_x, lHand_y, lHand_z = self.body_segment_data(x, y, z, "lHand")
        self.lHand_line.set_data_3d(lHand_x, lHand_y, lHand_z)

        # update legs
        rLeg_x, rLeg_y, rLeg_z = self.body_segment_data(x, y, z, "rLeg")
        self.rLeg_line.set_data_3d(rLeg_x, rLeg_y, rLeg_z)

        lLeg_x, lLeg_y, lLeg_z = self.body_segment_data(x, y, z, "lLeg")
        self.lLeg_line.set_data_3d(lLeg_x, lLeg_y, lLeg_z)

        # update feet
        rFoot_x, rFoot_y, rFoot_z = self.body_segment_data(x, y, z, "rFoot")
        self.rFoot_line.set_data_3d(rFoot_x, rFoot_y, rFoot_z)

        lFoot_x, lFoot_y, lFoot_z = self.body_segment_data(x, y, z, "lFoot")
        self.lFoot_line.set_data_3d(lFoot_x, lFoot_y, lFoot_z)

        #would love to do all of this programatically... 

    def animate_frame(self, i):
        # set title to frame number
        self.ax1.set_title('Frame ' + str(i))

        # update tracked point variables
        tracked_point_x, tracked_point_y, tracked_point_z = self.get_frame_data(i, self.skel_fr_mar_xyz)
        additional_point_x, additional_point_y, additional_point_z = self.additional_points[i]

        # update tracked point plotting
        self.tracked_point_graph._offsets3d = (tracked_point_x, tracked_point_y, tracked_point_z)

        self.additional_point_graph._offsets3d = ([additional_point_x], [additional_point_y], [additional_point_z])

        # update skeleton plotting
        self.update_skeleton(tracked_point_x, tracked_point_y, tracked_point_z)

    def animate(self):
        # call animation function
        self.anim = FuncAnimation(self.fig, self.animate_frame, frames=np.arange(0, self.number_of_frames, 1), interval=self.frame_interval, save_count=self.number_of_frames)

def main(display_video_bool, save_video_bool):
    start_timer = time.time()

    freemocap_data_folder_path = Path(
        "/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data"
    )
    session_id = "4stepsequence_session2_10_5_22"

    session_folder_path = freemocap_data_folder_path / session_id
    path_dict_file_name = "session_path_dict.npy"
    path_dict_file_path = session_folder_path / path_dict_file_name
    session_info_dict_name = "session_info_dict.npy"
    session_info_dict_path = session_folder_path / session_info_dict_name

    session_path_dict = np.load(path_dict_file_path, allow_pickle=True).item()
    session_info_dict = np.load(session_info_dict_path, allow_pickle=True).item()

    skeleton_data = np.load(session_path_dict["mediapipe_blender_rotated"])

    arm_com_frame_xyz = session_info_dict["arm_com_frame_xyz"]

    animation_object = SimpleSkeletonAnimation(
        session_folder_path=freemocap_data_folder_path / session_id,
        skeleton_data=skeleton_data,
        additional_points=arm_com_frame_xyz
    )
    animation_object.animate()

    # display plot if parameter set to true
    if display_video_bool:
        plt.show()

    # save video if parameter set to true
    if save_video_bool:
        video_writer = animation.FFMpegWriter(fps=60, bitrate=500)
        animation_object.anim.save(animation_object.animation_path, writer=video_writer)

    end_timer = time.time()
    time_elapsed = end_timer - start_timer
    print(f"Processing took {time_elapsed} seconds")

if __name__ == "__main__":
    # uncomment to display
    main(display_video_bool=True, save_video_bool=False)

    # uncomment to save
    # main(display_video_bool=False, save_video_bool=True)