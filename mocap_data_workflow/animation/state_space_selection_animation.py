from statistics import mean, stdev
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import cv2
from pathlib import Path

class SlackAnimation:
    def __init__(self):

        self.save_video = False # set to True to save video
        self.starting_frame = 2750 # these could be parameters to init
        self.ending_frame = 3250

        # load in all of the data
        # set session folder path
        self.session_folder_path = Path("/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data/4stepsequence_session2_10_5_22")
        print(f"Animating state space for {self.session_folder_path}...")
        data_arrays_path = self.session_folder_path / "DataArrays"

        # get 3d skeleton data path and load it
        #mediapipe_file_name = "mediaPipeSkel_3d_origin_aligned.npy"
        mediapipe_file_name = "mediaPipeSkel_3d_filtered.npy"
        #mediapipe_file_name = "mediapipe_body_3d_xyz_transformed.npy" # use for data rotated in blender 
        mediapipe_3d_data_path = data_arrays_path / mediapipe_file_name
        self.skeleton_frame_joint_xyz = np.load(mediapipe_3d_data_path)
        print(self.skeleton_frame_joint_xyz.shape)

        # get total body com data path and load it
        COM_file_name = "totalBodyCOM_frame_XYZ.npy"
        #COM_file_name = "totalBodyCOM_frame_XYZ_transformed.npy" # use for data rotated in blender
        total_body_com_data_path = data_arrays_path / COM_file_name
        self.total_body_com_frame_xyz = np.load(total_body_com_data_path)
        print(self.total_body_com_frame_xyz.shape)

        # get segment com data path and load it
        segment_COM_file_name = "segmentedCOM_frame_joint_XYZ.npy"
        #segment_COM_file_name = "segmentedCOM_frame_joint_XYZ_transformed.npy" # use for data rotated in blender
        segment_com_data_path = data_arrays_path / segment_COM_file_name
        self.segment_com_frame_joint_xyz = np.load(segment_com_data_path)
        print(self.segment_com_frame_joint_xyz.shape)

        # pick camera to be shown in videos
        camera = 2

        # get video paths
        synced_videos_path = self.session_folder_path / "SyncedVideos"
        video_name = "synced_Cam" + str(camera) + ".MP4"
        COM_video_name = "synced_Cam" + str(camera) + "_skeleton.MP4"
        video_path = synced_videos_path / video_name
        self.COM_video_path = self.session_folder_path / COM_video_name 
        skeleton_video_name = "simple_skeleton_animation.mp4"
        self.skeleton_video_path = self.session_folder_path / skeleton_video_name

        # get COM data for points we're particularly interested in
        self.Rfoot_COM_frame_xyz = self.segment_com_frame_joint_xyz[:,12,:]
        self.Lfoot_COM_frame_xyz = self.segment_com_frame_joint_xyz[:,13,:]

        # set length of traces in frames
        self.BOS_trace_length = 100 # frames
        self.state_space_trace_length = 50 # frames

        # create base of support data based on which foot I'm standing on
        # TODO: change this to read in from session
        self.BOS_frame_x = np.concatenate((self.Lfoot_COM_frame_xyz[:3371,0], self.Rfoot_COM_frame_xyz[3371:4371,0], self.Lfoot_COM_frame_xyz[4371:,0]))

        # create COM - BOS data for plotting difference in balance
        self.relative_COM_frame_x = self.total_body_com_frame_xyz[:,0] - self.BOS_frame_x
        self.relative_COM_frame_x_velocity = np.diff(self.pad_array(self.relative_COM_frame_x)) # array must be padded to keep it the same length

        self.data_length = len(self.total_body_com_frame_xyz[:,0])
        print("There are {} frames".format(self.data_length))

        self.setup_video_captures()
        self.initialize_figure()
        self.create_subplot1()
        self.create_subplot2()
        self.create_subplot3()
        self.create_subplot4()


    def pad_array(self,array):
        '''Duplicates the first item of an array to preserve array size while differentiating.'''
        padded_array = array.copy()

        return np.insert(padded_array,0,array[0])

    def initialize_figure(self):
        self.fig = plt.figure(constrained_layout=True)
        #if self.save_video:
        #    self.fig.set_size_inches(18, 21)
        #else:
        #    self.fig.set_size_inches(6, 7)
        self.fig.set_size_inches(12,8)
        if self.save_video:
            self.fig.set_dpi(1000)
        self.spec = self.fig.add_gridspec(7, 7) # gridspec allows us to have one plot span multiple plot grids

        self.plotmin = 0 - stdev(self.total_body_com_frame_xyz[:,0])
        self.plotmax = 0 + stdev(self.total_body_com_frame_xyz[:,0])

        self.fig.suptitle('Slackline Center of Mass and Base of Support')

    def create_subplot1(self):
        self.ax1 = self.fig.add_subplot(self.spec[0:5, 0:4])

        self.ax1.set_title("3d Animation")
        self.ax1.xaxis.set_visible(False) #turn off axis ticks and tick labels for video
        self.ax1.yaxis.set_visible(False)

        self.skeleton_cap.set(cv2.CAP_PROP_POS_FRAMES, self.starting_frame)

    def create_subplot2(self):
        self.ax2 = self.fig.add_subplot(self.spec[5, :]) # this spans two columns

        self.ax2.set_title("Base of Support Position")
        self.ax2.set_xlim(self.plotmin, self.plotmax) 
        self.ax2.set_ylim(-100, 100)
        self.ax2.set_xlabel("Distance (mm)")
        self.ax2.set_ylabel("Frames")

        # create second set of line graphs to show active trace
        self.frame_index_list = range(0, self.data_length)

        self.scatter_relative_COM = self.ax2.scatter(0, 0, s=325, color="green", marker="*", label="COM - BOS") 

        # create vertical center line that will track total body COM
        self.BOS_center_line = self.ax2.axvline(0, ls='-', color='purple', lw=1, zorder=10, label="Base of Support")

        #create plots and trace plots for relative COM animation
        self.plot_relative_COM, = self.ax2.plot(self.relative_COM_frame_x,self.frame_index_list, color="lightgreen")
        self.relative_COM_trace, = self.ax2.plot(self.relative_COM_frame_x,self.frame_index_list, color="green")

    def create_subplot3(self):
        self.ax3 = self.fig.add_subplot(self.spec[0:5, 4:])
        self.ax3.set_title("Mediapipe Video")
        self.ax3.xaxis.set_visible(False) #turn off axis ticks and tick labels for video
        self.ax3.yaxis.set_visible(False)

        self.mediapipe_cap.set(cv2.CAP_PROP_POS_FRAMES, self.starting_frame)

    def create_subplot4(self):
        self.ax4 = self.fig.add_subplot(self.spec[6, :]) # this spans two columns

        self.ax4.set_title("State Space")

        self.ax4.set_xlim(-50, 50)
        self.ax4.set_ylim(-10, 10)
        self.ax4.set_xlabel("Distance (mm)")
        self.ax4.set_ylabel("Velocity")

        #! this needs to be changed for each video
        self.plot_state_space_shadow, = self.ax4.plot(self.relative_COM_frame_x[self.starting_frame:self.ending_frame], self.relative_COM_frame_x_velocity[self.starting_frame:self.ending_frame], zorder=1, color="plum")
        self.state_space_center_line = self.ax4.axvline(0, ls='-', color='black', lw=1, zorder=1, label="Base of Support")
        self.plot_state_space_trace, = self.ax4.plot(self.relative_COM_frame_x[0], self.relative_COM_frame_x_velocity[0], zorder=2, color="purple")
        self.scatter_state_space = self.ax4.scatter(self.relative_COM_frame_x[0], self.relative_COM_frame_x_velocity[0], zorder=3, color="purple")
        

    def setup_video_captures(self):
        # setup video captures
        self.mediapipe_cap = cv2.VideoCapture(str(self.COM_video_path))
        self.skeleton_cap = cv2.VideoCapture(str(self.skeleton_video_path))

        self.frame_rate = self.skeleton_cap.get(cv2.CAP_PROP_FPS)
        self.frame_interval = 1/(self.frame_rate * 0.001)

    def release_video_captures(self):
        self.mediapipe_cap.release()
        self.skeleton_cap.release()

    def animation_frame(self,i):
        '''Animate the videos and plots, called for every frame'''
        # maintain counter for keeping track of video progress every 100 frames
        if i % 100 == 0:
            print("Currently on frame: {}".format(i))

        # display 3d skeleton video in top left subplot
        self.ax1.clear()
        skeleton_ret, skeleton_frame = self.skeleton_cap.read() #getting an image from feed, 'frame' is our video feed variable
        if skeleton_ret:
            skeleton_image = cv2.cvtColor(skeleton_frame, cv2.COLOR_BGR2RGBA) #recolor image into the RGB format (for matplotlib)
            cropped_skeleton_image =  skeleton_image[100:-150,200:-50]
            self.ax1.imshow(cropped_skeleton_image)

        # display mediapipe video in top right subplot
        self.ax3.clear()
        mediapipe_ret, mediapipe_frame = self.mediapipe_cap.read() #getting an image from feed, 'frame' is our video feed variable
        if mediapipe_ret:
            mediapipe_image = cv2.cvtColor(mediapipe_frame, cv2.COLOR_BGR2RGBA) #recolor image into the RGB format (for matplotlib)
            cropped_mediapipe_image = mediapipe_image[:1900,500:3350] #[700:1900,1000:2850]
            self.ax3.imshow(cropped_mediapipe_image)

            
        # update COM and foot point data for frame
        self.scatter_relative_COM.set_offsets((self.relative_COM_frame_x[i],i))
        self.scatter_state_space.set_offsets((self.relative_COM_frame_x[i], self.relative_COM_frame_x_velocity[i]))

        # update data in trace plots for new frame
        self.relative_COM_trace.set_xdata(self.relative_COM_frame_x[i-self.BOS_trace_length:i+1])
        self.relative_COM_trace.set_ydata(self.frame_index_list[i-self.BOS_trace_length:i+1])
        self.plot_state_space_trace.set_xdata(self.relative_COM_frame_x[i-self.state_space_trace_length:i+1])
        self.plot_state_space_trace.set_ydata(self.relative_COM_frame_x_velocity[i-self.state_space_trace_length:i+1])

        # set moving axis to show BOS_trace_length frames of time on either side
        self.ax2.set_ylim(i-self.BOS_trace_length, i+self.BOS_trace_length)

        # update vertical line x position for frame to track total COM
        #self.vert_line.set_xdata((0,0))

    def run_animation(self):
        self.ax2.legend(loc = 'upper right', fontsize = 'medium')
        self.anim = FuncAnimation(self.fig, func=self.animation_frame, frames=np.arange(self.starting_frame, self.ending_frame, 1), interval=self.frame_interval, save_count=(self.ending_frame-self.starting_frame))

def main():
    slack_animation = SlackAnimation()
    slack_animation.run_animation()

    if slack_animation.save_video:
        animation_name = "StateSpaceAnimation-" + str(slack_animation.starting_frame) + "-" + str(slack_animation.ending_frame) + ".mp4"
        animation_path = slack_animation.session_folder_path / animation_name
        video_writer = animation.FFMpegWriter(fps=60, bitrate=-1)
        slack_animation.anim.save(str(animation_path), writer=video_writer)

    else:
        plt.show()

    slack_animation.release_video_captures()

if __name__ == "__main__":
    main()

