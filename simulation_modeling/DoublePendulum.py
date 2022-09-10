import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

mpl.use('tkagg') # had to add this because plt.show() was crashing due to "segmentation fault:11" 

'''Double pendulum simulation made using scipy's ODE solver. Main structure taken from ODEPendulum.py.
Code draws heavily from matplotlib's 'double_pendulum.py' example: https://matplotlib.org/3.5.0/gallery/animation/double_pendulum.html
'''

class DoublePendulum:
    def __init__(self):
        # set length of simulation and time interval
        self.simulation_length = 10 # s
        self.time_interval = 0.05  # s
        self.time = 0 # s

        # set parameters:
        self.gravity = 9.8 # m/s**2
        self.pendulum_1_length = 1 # m
        self.pendulum_2_length = 3 # m
        self.total_length = self.pendulum_1_length + self.pendulum_2_length
        self.pendulum_1_mass = 1 # kg
        self.pendulum_2_mass = 1 # kg
        self.pendulum_1_angle = np.radians(180) # angle from vertical (0 is hanging down), enter in degrees
        self.pendulum_2_angle = np.radians(179) # angle from vertical (0 is hanging down), enter in degrees
        self.pendulum_1_angular_velocity = np.radians(0) # enter in degrees per second
        self.pendulum_2_angular_velocity = np.radians(0) # enter in degrees per second


        # create time array
        self.time_array = np.arange(0.0, self.simulation_length, self.time_interval)

        # create state variable
        self.state = np.array([self.pendulum_1_angle, self.pendulum_1_angular_velocity, self.pendulum_2_angle, self.pendulum_2_angular_velocity])
        
        # find solutions to differential equation
        self.ode_solution = odeint(self.derivatives, self.state, self.time_array)

        self.parse_ode_solution()

        self.initialize_figure()

    def initialize_figure(self):
        # create figure and axis
        self.fig = plt.figure(constrained_layout=True, figsize=(9,4))
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_aspect('equal')
        axis_scale_factor = 1.2
        self.ax1.set_xlim(-self.total_length*axis_scale_factor, self.total_length*axis_scale_factor)
        self.ax1.set_ylim(-self.total_length*axis_scale_factor, self.total_length*axis_scale_factor)
        self.fig.suptitle(f'Double Pendulum')
        self.ax1.set_title("0 Seconds")

        self.pendulum_line, = self.ax1.plot([], [], 'o-', c='salmon')

    def derivatives(self, state, t):
        # create empty array to store derivative values
        derivative_array = np.zeros_like(state)

        # pull out values from state
        current_pendulum_1_angle = state[0]
        current_pendulum_1_angular_velocity = state[1]
        current_pendulum_2_angle = state[2]
        current_pendulum_2_angular_velocity = state[3]

        delta = current_pendulum_2_angle - current_pendulum_1_angle
        # calculate derivatives
        derivative_array[0] = current_pendulum_1_angular_velocity
        denominator_1 = (self.pendulum_1_mass+self.pendulum_2_mass) * self.pendulum_1_length - self.pendulum_2_mass * self.pendulum_1_length * np.cos(delta) * np.cos(delta)
        derivative_array[1] = ((self.pendulum_2_mass * self.pendulum_1_length * state[1] * state[1] * np.sin(delta) * np.cos(delta)
                    + self.pendulum_2_mass * self.gravity * np.sin(current_pendulum_2_angle) * np.cos(delta)
                    + self.pendulum_2_mass * self.pendulum_2_length * current_pendulum_2_angular_velocity * current_pendulum_2_angular_velocity * np.sin(delta)
                    - (self.pendulum_1_mass+self.pendulum_2_mass) * self.gravity * np.sin(current_pendulum_1_angle))
                    / denominator_1)
        derivative_array[2] = current_pendulum_2_angular_velocity
        denominator_2 = (self.pendulum_2_length/self.pendulum_1_length) * denominator_1
        derivative_array[3] = ((- self.pendulum_2_mass * self.pendulum_2_length * state[3] * state[3] * np.sin(delta) * np.cos(delta)
                + (self.pendulum_1_mass+self.pendulum_2_mass) * self.gravity * np.sin(current_pendulum_1_angle) * np.cos(delta)
                - (self.pendulum_1_mass+self.pendulum_2_mass) * self.pendulum_1_length * current_pendulum_1_angular_velocity * current_pendulum_1_angular_velocity * np.sin(delta)
                - (self.pendulum_1_mass+self.pendulum_2_mass) * self.gravity * np.sin(current_pendulum_2_angle))
               / denominator_2)

        return derivative_array

    def parse_ode_solution(self):
        # get pendulum x and y values from ode solution
        self.pendulum_1_xs = self.pendulum_1_length * np.sin(self.ode_solution[:, 0])
        self.pendulum_1_ys = -self.pendulum_1_length * np.cos(self.ode_solution[:, 0])

        self.pendulum_2_xs = self.pendulum_2_length * np.sin(self.ode_solution[:, 2]) + self.pendulum_1_xs
        self.pendulum_2_ys = -self.pendulum_2_length * np.cos(self.ode_solution[:, 2]) + self.pendulum_1_ys

    def animate_frame(self, i):
        self.ax1.set_title(f"{i * self.time_interval:.1f} Seconds")

        this_x = [0, self.pendulum_1_xs[i], self.pendulum_2_xs[i]]
        this_y = [0, self.pendulum_1_ys[i], self.pendulum_2_ys[i]]

        self.pendulum_line.set_data(this_x, this_y)
    
    def animate(self):
        # call animation function
        self.anim = FuncAnimation(self.fig, self.animate_frame, frames=np.arange(0, len(self.time_array)), interval=self.time_interval, save_count=int(self.simulation_length/self.time_interval))
        

def main(display_bool = True, save_video_bool = False):
    pendulum = DoublePendulum()
    pendulum.animate()

    if display_bool:
        plt.show()
    if save_video_bool:
        animation_path = "/Users/Philip/Documents/GitHub/Learning/Videos/double_pendulum_animation.mp4"
        video_writer = animation.FFMpegWriter(fps=1/pendulum.time_interval, bitrate=500)
        pendulum.anim.save(animation_path, writer=video_writer)

if __name__ == "__main__":
    main(display_bool=True, save_video_bool=False)
    #main(display_bool=False, save_video_bool=True)