import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation

from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

mpl.use('tkagg') # had to add this because plt.show() was crashing due to "segmentation fault:11" 

'''Simple pendulum animation made using scipy's ODE solver. 
Made as a class to be a solid jumping off point for more complex pendulums, like cart and pendulum or double pendulums.
'''

class Pendulum:
    def __init__(self):
        # set length of simulation
        self.simulation_length = 5 #s

        # set parameters:
        self.length = 1 #m
        self.gravity = 9.8 #m/s**2
        self.time = 0 #s
        self.time_interval = 0.01  #s
        self.pendulum_angle = np.radians(110) # angle from vertical
        self.angular_velocity = 0

        # create time array
        self.time_array = np.arange(0.0, self.simulation_length, self.time_interval)

        # create state variable
        self.state = np.array([self.pendulum_angle, self.angular_velocity])
        
        # find solutions to differential equation
        self.ode_solution = odeint(self.derivatives, self.state, self.time_array)

        self.parse_ode_solution()

        self.initialize_figure()

    def initialize_figure(self):
        # create figure and axis
        self.fig = plt.figure(constrained_layout=True)
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_aspect('equal')
        self.ax1.set_xlim(-self.length*1.1,self.length*1.1)
        self.ax1.set_ylim(-self.length*1.1-0.5,self.length*1.1-0.5)
        self.fig.suptitle(f"Simple Pendulum with Angle {np.degrees(self.pendulum_angle):.1f} Degrees")
        self.ax1.set_title("0 Seconds")

        self.line, = self.ax1.plot([0, self.pendulum_xs[0]], [0, self.pendulum_ys[0]], 'o-', c='salmon')

    def derivatives(self, state, t):
        # create empty array to store derivative values
        derivative_array = np.zeros_like(state)

        # pull out values from state
        current_pendulum_angle = state[0]
        current_angular_velocity = state[1]

        # calculate derivatives
        derivative_array[0] = current_angular_velocity
        derivative_array[1] = (self.gravity * np.sin(current_pendulum_angle)) / self.length

        return derivative_array

    def parse_ode_solution(self):
        # get pendulum angles from differential equation solution
        self.pendulum_angles_array = self.ode_solution[:, 0]

        # get x and y values from pendulum angles
        self.pendulum_xs = self.length * np.sin(self.pendulum_angles_array)
        self.pendulum_ys = self.length * np.cos(self.pendulum_angles_array)

    def animate_frame(self, i):
        if i * self.time_interval % 1 == 0:
            self.ax1.set_title(f"{int(i * self.time_interval)} Seconds")

        this_x = [0, self.pendulum_xs[i]]
        this_y = [0, self.pendulum_ys[i]]

        self.line.set_data(this_x, this_y)
    
    def animate(self):
        # call animation function
        self.anim = FuncAnimation(self.fig, self.animate_frame, frames=np.arange(0, len(self.time_array)), interval=self.time_interval, save_count=int(self.simulation_length/self.time_interval))
        

def main(display_bool = True, save_video_bool = False):
    pendulum = Pendulum()
    pendulum.animate()

    if display_bool:
        plt.show()
    if save_video_bool:
        animation_path = "/Users/Philip/Documents/GitHub/Learning/Videos/ode_simple_pendulum_animation.mp4"
        video_writer = animation.FFMpegWriter(fps=1/pendulum.time_interval, bitrate=500)
        pendulum.anim.save(animation_path, writer=video_writer)

if __name__ == "__main__":
    main(display_bool=True, save_video_bool=False)
    #main(display_bool=False, save_video_bool=True)
