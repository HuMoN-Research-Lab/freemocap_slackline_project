import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation

from pathlib import Path
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

#plt.rcParams['animation.ffmpeg_path'] = '/Users/philipqueen/opt/anaconda3/lib/python3.9/site-packages'

mpl.use('tkagg') # had to add this because plt.show() was crashing due to "segmentation fault:11" 

'''Cart and pendulum simulation made using scipy's ODE solver. Main structure taken from ODEPendulum.py.
Based in part off of: https://github.com/zjor/inverted-pendulum/blob/master/python/controlled-cart-pendulum.py
Help understanding PID controller came from: https://pidexplained.com/pid-controller-explained/
'''

class Pendulum:
    def __init__(self):
        self.save_video = True
        # set length of simulation
        self.simulation_length = 10 #s

        # set parameters:
        self.length = 1 # m
        self.gravity = 9.8 # m/s**2
        self.time = 0 # s
        self.time_interval = 0.05  # s
        self.pendulum_angle = np.radians(1.61887251) # angle from vertical, enter in degrees
        self.angular_velocity = -0.0655983995 # m/s
        self.cart_position = 0.0360524181 # m from origin
        self.desired_cart_position = 0 # m from origin
        self.cart_velocity = 0.00235032545 # m/s
        self.mass = 73 # kg
        self.spring_constant = 75 # N/m

        self.fps = 1/self.time_interval


        # create time array
        self.time_array = np.arange(0.0, self.simulation_length, self.time_interval)

        # create state variable
        self.state = np.array([self.pendulum_angle, self.angular_velocity, self.cart_position, self.cart_velocity])

        # initialize PID settings
        self.set_pid_gains()
        self.integral_total = 0
        
        # find solutions to differential equation
        self.ode_solution = odeint(self.derivatives, self.state, self.time_array)

        self.parse_ode_solution()

        self.initialize_figure()

    def initialize_figure(self):
        # create figure and axis
        self.fig = plt.figure(constrained_layout=True, figsize=(9,4))
        self.ax1 = self.fig.add_subplot(211)
        self.ax1.set_aspect('equal')
        self.ax1.set_xlim(-self.length*5, self.length*5)
        self.ax1.set_ylim(-self.length*0.5, self.length*1.5)
        self.fig.suptitle(f'Cart and Pendulum\n\
            Starting conditions from Session 2, Frame 2640\n\
            Starting Angle {np.degrees(self.pendulum_angle):.1f} Degrees\n\
            Starting Cart Position of {self.cart_position:.1f} m\n\
            Starting Cart Velocity of {self.cart_velocity:.1f} m/s')
        self.ax1.set_title("0 Seconds")

        self.pendulum_line, = self.ax1.plot([self.cart_positions_array[0], self.pendulum_xs[0]], [0, self.pendulum_ys[0]], 'o-', c='salmon')
        self.cart_scatter = self.ax1.scatter(self.cart_positions_array[0], 0, zorder=20)
        self.spring_line, = self.ax1.plot([0, self.cart_positions_array[0]], [0, 0], ls=':', c='gold')

        # set display parameters for visualizing spring
        self.spring_display_scale = 5
        self.spring_line.set_linewidth(self.spring_display_scale/(abs(self.cart_positions_array[0])+1))

        self.ax2 = self.fig.add_subplot(212)
        self.ax2.set_aspect('equal')
        #self.ax2.set_xlim(-self.length*5, self.length*5)
        #self.ax2.set_ylim(-self.length*0.5, self.length*1.5)
        self.ax2.set_title("Pendulum State Space")

        self.state_space_trace_length = 20

        self.plot_state_space_shadow, = self.ax2.plot(self.pendulum_displacement[1:], self.pendulum_displacement_velocity[1:], zorder=1, color="plum")
        self.state_space_center_line = self.ax2.axvline(0, ls='-', color='black', lw=1, zorder=1, label="Base of Support (Cart Location)")
        self.plot_state_space_trace, = self.ax2.plot(self.pendulum_displacement[0], self.pendulum_displacement_velocity[0], zorder=2, color="purple")
        self.scatter_state_space = self.ax2.scatter(self.pendulum_displacement[0], self.pendulum_displacement_velocity[0], zorder=3, color="purple")

    def set_pid_gains(self):
        # good defaults provided in inline comments

        # gains for pendulum angle
        self.proportional_gain_pendulum_angle = 30 #30
        self.derivative_gain_pendulum_angle = 10 #10

        # gains for cart position
        self.proportional_gain_cart_position = 4 #1
        self.derivative_gain_cart_position = 2 #3

    def calculate_pid_outputs(self, current_pendulum_angle, current_angular_velocity, current_cart_position, current_cart_velocity):
        
        # calculate PD controller outputs
        proportional_output = (self.proportional_gain_pendulum_angle * current_pendulum_angle) + (self.proportional_gain_cart_position * (current_cart_position - self.desired_cart_position))
        derivative_output = (self.derivative_gain_pendulum_angle * current_angular_velocity) + (self.derivative_gain_cart_position * current_cart_velocity)
        
        # return sum of sub outputs
        pd_output = proportional_output + derivative_output
        print(pd_output)
        
        return pd_output

    def calculate_spring_acceleration(self, current_cart_position):
        '''Return the spring acceleration, calculated by substituting F=ma into Hooke's Law
        Hooke's Law: F = kx (Force = spring constant * distance from equilibrium)
        '''
        return (self.spring_constant * current_cart_position)/self.mass

    def generate_noise(self, noise_multiplier):
        random_number_generator = np.random.default_rng() 
        
        noise_array = random_number_generator.random(4) # an array of four fandom numbers created from the random number generator

        return noise_array * noise_multiplier
        

    def derivatives(self, state, t):
        # create empty array to store derivative values
        derivative_array = np.zeros_like(state)

        noise_array = self.generate_noise(0)

        # pull out values from state
        current_pendulum_angle = state[0] + noise_array[0]
        current_angular_velocity = state[1] + noise_array[1]
        current_cart_position = state[2] + noise_array[2]
        current_cart_velocity = state[3] + noise_array[3]

        pid_controller_output = self.calculate_pid_outputs(current_pendulum_angle, current_angular_velocity, current_cart_position, current_cart_velocity)
        spring_acceleration = self.calculate_spring_acceleration(current_cart_position)

        # calculate derivatives
        derivative_array[0] = current_angular_velocity
        derivative_array[1] = (self.gravity * np.sin(current_pendulum_angle) - (pid_controller_output - spring_acceleration) * np.cos(current_pendulum_angle)) / self.length
        derivative_array[2] = current_cart_velocity
        derivative_array[3] = pid_controller_output - spring_acceleration

        return derivative_array

    def parse_ode_solution(self):
        # get pendulum angles from differential equation solution
        self.pendulum_angles_array = self.ode_solution[:, 0]
        self.cart_positions_array = self.ode_solution[:, 2]

        # get x and y values from pendulum angles
        self.pendulum_displacement = self.length * np.sin(self.pendulum_angles_array) # position for state space
        self.pendulum_xs = self.pendulum_displacement + self.cart_positions_array
        self.pendulum_ys = self.length * np.cos(self.pendulum_angles_array)

        self.pendulum_displacement_velocity = np.diff(self.pad_array(self.pendulum_displacement)) # velocity for state space

    def pad_array(self,array):
        '''Duplicates the first item of an array to preserve array size while differentiating.'''
        padded_array = array.copy()

        return np.insert(padded_array,0,array[0])

    def animate_frame(self, i):
        self.ax1.set_title(f"{i * self.time_interval:.1f} Seconds")

        this_x = [self.cart_positions_array[i], self.pendulum_xs[i]]
        this_y = [0, self.pendulum_ys[i]]

        self.pendulum_line.set_data(this_x, this_y)
        self.cart_scatter.set_offsets((self.cart_positions_array[i], 0))
        self.spring_line.set_data([0, self.cart_positions_array[i]], [0, 0])

        # animate spring width
        self.spring_line.set_linewidth(self.spring_display_scale/(abs(self.cart_positions_array[i])+1))

        self.scatter_state_space.set_offsets((self.pendulum_displacement[i], self.pendulum_displacement_velocity[i]))
        trace_length = self.state_space_trace_length
        if i < self.state_space_trace_length+1:
            trace_length = i-1
        self.plot_state_space_trace.set_xdata(self.pendulum_displacement[i-trace_length:i+1])
        self.plot_state_space_trace.set_ydata(self.pendulum_displacement_velocity[i-trace_length:i+1])
    
    def animate(self):
        # call animation function
        self.anim = FuncAnimation(self.fig, self.animate_frame, frames=np.arange(0, len(self.time_array)), interval=self.time_interval, save_count=int(self.simulation_length/self.time_interval))
        

def main():
    pendulum = Pendulum()
    pendulum.animate()

    if pendulum.save_video:
        animation_path = Path("/Users/Philip/Documents/GitHub/Learning/Videos/anim.mp4")
        video_writer = animation.FFMpegWriter(fps=pendulum.fps)
        pendulum.anim.save(animation_path, writer=video_writer)

    else:
        plt.show()

        

if __name__ == "__main__":
    main()
