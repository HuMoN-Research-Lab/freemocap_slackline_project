import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation

from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

mpl.use('tkagg') # had to add this because plt.show() was crashing due to "segmentation fault:11" 

'''Identical to 'CartAndPendulum.py', but with added horizontal spring attached to cart to try to force the cart location to 0.
'''

class Pendulum:
    def __init__(self):
        # set length of simulation
        self.simulation_length = 10 #s

        # set parameters:
        self.length = 2 # m
        self.gravity = 9.8 # m/s**2
        self.time = 0 # s
        self.time_interval = 0.05  # s
        self.pendulum_angle = np.radians(10) # angle from vertical, enter in degrees
        self.angular_velocity = -1 # m/s
        self.cart_position = 1 # m from origin
        self.desired_cart_position = 0 # m from origin
        self.cart_velocity = -3 # m/s
        self.mass = 50 # kg
        self.spring_constant = 150 # N/m


        # create time array
        self.time_array = np.arange(0.0, self.simulation_length, self.time_interval)

        # create state variable
        self.state = np.array([self.pendulum_angle, self.angular_velocity, self.cart_position, self.cart_velocity])

        # initialize PID settings
        self.set_pid_gains()
        
        # find solutions to differential equation
        self.ode_solution = odeint(self.derivatives, self.state, self.time_array)

        self.parse_ode_solution()

        self.initialize_figure()

    def initialize_figure(self):
        # create figure and axis
        self.fig = plt.figure(constrained_layout=True, figsize=(9,4))
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_aspect('equal')
        self.ax1.set_xlim(-self.length*5, self.length*5)
        self.ax1.set_ylim(-self.length*0.5, self.length*1.5)
        self.fig.suptitle(f'Cart and Pendulum\n\n\
            Starting Angle {np.degrees(self.pendulum_angle):.1f} Degrees\n\
            Starting Cart Position of {self.cart_position:.1f} m\n\
            Starting Cart Velocity of {self.cart_velocity:.1f} m/s\n\
            Spring Constant of {self.spring_constant:.1f} N/m\n\
            Mass of {self.mass:.1f} kg')
        self.ax1.set_title("0 Seconds")

        self.pendulum_line, = self.ax1.plot([self.cart_positions_array[0], self.pendulum_xs[0]], [0, self.pendulum_ys[0]], 'o-', c='salmon')
        self.cart_scatter = self.ax1.scatter(self.cart_positions_array[0], 0, zorder=20)
        self.spring_line, = self.ax1.plot([0, self.cart_positions_array[0]], [0, 0], ls=':', c='gold')

        # set display parameters for visualizing spring
        self.spring_display_scale = 5
        self.spring_line.set_linewidth(self.spring_display_scale/(abs(self.cart_positions_array[0])+1))



    def set_pid_gains(self):
        # good defaults provided in inline comments

        # gains for pendulum angle
        self.proportional_gain_pendulum_angle = 30 #30
        self.derivative_gain_pendulum_angle = 10 #10

        # gains for cart position
        self.proportional_gain_cart_position = 4 #1
        self.derivative_gain_cart_position = 2 #3

    def calculate_pid_outputs(self, current_pendulum_angle, current_angular_velocity, current_cart_position, current_cart_velocity):
        
        # calculate PID controller outputs
        proportional_output = (self.proportional_gain_pendulum_angle * current_pendulum_angle) + (self.proportional_gain_cart_position * (current_cart_position - self.desired_cart_position))
        derivative_output = (self.derivative_gain_pendulum_angle * current_angular_velocity) + (self.derivative_gain_cart_position * current_cart_velocity)
        
        # return sum of sub outputs
        return proportional_output + derivative_output

    def calculate_spring_acceleration(self, current_cart_position):
        '''Return the spring acceleration, calculated by substituting F=ma into Hooke's Law
        Hooke's Law: F = kx (Force = spring constant * distance from equilibrium)
        '''
        return (self.spring_constant * current_cart_position)/self.mass

    def derivatives(self, state, t):
        # create empty array to store derivative values
        derivative_array = np.zeros_like(state)

        # pull out values from state
        current_pendulum_angle = state[0]
        current_angular_velocity = state[1]
        current_cart_position = state[2]
        current_cart_velocity = state[3]

        pid_controller_output = self.calculate_pid_outputs(current_pendulum_angle, current_angular_velocity, current_cart_position, current_cart_velocity)
        spring_acceleration = self.calculate_spring_acceleration(current_cart_position)

        # derivative of pendulum angle (angular velocity)
        derivative_array[0] = current_angular_velocity
        # derivative of angular velocity (angular acceleration)
        derivative_array[1] = (self.gravity * np.sin(current_pendulum_angle) - (pid_controller_output - spring_acceleration) * np.cos(current_pendulum_angle)) / self.length
        # derivative of cart position (cart velocity)
        derivative_array[2] = current_cart_velocity
        # derivative of cart velocity (cart acceleration)
        derivative_array[3] = pid_controller_output - spring_acceleration

        return derivative_array

    def parse_ode_solution(self):
        # get pendulum angles from differential equation solution
        self.pendulum_angles_array = self.ode_solution[:, 0]
        self.cart_positions_array = self.ode_solution[:, 2]

        # get x and y values from pendulum angles
        self.pendulum_xs = self.length * np.sin(self.pendulum_angles_array) + self.cart_positions_array
        self.pendulum_ys = self.length * np.cos(self.pendulum_angles_array)

    def animate_frame(self, i):
        self.ax1.set_title(f"{i * self.time_interval:.1f} Seconds")

        this_x = [self.cart_positions_array[i], self.pendulum_xs[i]]
        this_y = [0, self.pendulum_ys[i]]

        self.pendulum_line.set_data(this_x, this_y)
        self.cart_scatter.set_offsets((self.cart_positions_array[i], 0))
        self.spring_line.set_data([0, self.cart_positions_array[i]], [0, 0])

        # animate spring width
        self.spring_line.set_linewidth(self.spring_display_scale/(abs(self.cart_positions_array[i])+1))
    
    def animate(self):
        # call animation function
        self.anim = FuncAnimation(self.fig, self.animate_frame, frames=np.arange(0, len(self.time_array)), interval=self.time_interval, save_count=int(self.simulation_length/self.time_interval))
        

def main(display_bool = True, save_video_bool = False):
    pendulum = Pendulum()
    pendulum.animate()

    if display_bool:
        plt.show()
    if save_video_bool:
        animation_path = "/Users/Philip/Documents/GitHub/Learning/Videos/spring_cart_pendulum_animation.mp4"
        video_writer = animation.FFMpegWriter(fps=1/pendulum.time_interval, bitrate=500)
        pendulum.anim.save(animation_path, writer=video_writer)

if __name__ == "__main__":
    #main(display_bool=True, save_video_bool=False)
    main(display_bool=False, save_video_bool=True)
