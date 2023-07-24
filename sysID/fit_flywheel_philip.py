import numpy as np
import matplotlib.pyplot as plt
from models import cartpole_flywheel as model

# Load the data
q = np.load('/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data/4stepsequence_session2_10_5_22/pendulum_flywheel_state_q.npy')
qDot = np.load('/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data/4stepsequence_session2_10_5_22/pendulum_flywheel_state_qdot.npy')
qDotDot = np.load('/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data/4stepsequence_session2_10_5_22/pendulum_flywheel_state_qddot.npy')

params = model.default_params()

# convert to meters
q[:, 0] = q[:, 0]/1000.

qDot[:, 0] = qDot[:, 0]/1000.

qDotDot[:, 0] = qDotDot[:, 0]/1000.

# convert angle to radians
q[:, 1] = q[:, 1]*np.pi/180.
qDot[:, 1] = qDot[:, 1]*np.pi/180.
qDotDot[:, 1] = qDotDot[:, 1]*np.pi/180.

# convert to meters squared
q[:, 2] = q[:, 2]/1000000.
qDot[:, 2] = qDot[:, 2]/1000000.
qDotDot[:, 2] = qDotDot[:, 2]/1000000.

# multiply by mass to get kg/m^2
q[:, 2] = q[:, 2] * params["mass_pendulum"]
qDot[:, 2] = qDot[:, 2] * params["mass_pendulum"]
qDotDot[:, 2] = qDotDot[:, 2] * params["mass_pendulum"]

# Plot the data
fig, axs = plt.subplots(3, 1, figsize=(8, 8))
axs[0].plot(q[:, 0], qDot[:, 0], color='orange')
axs[0].set_xlabel('Position [m]')
axs[0].set_ylabel('Velocity [m/s]')
axs[0].set_title('Phase Portrait: Cart')
axs[1].plot(q[:, 1], qDot[:, 1], color='orange')
axs[1].set_xlabel('Position [rad]')
axs[1].set_ylabel('Velocity [rad/s]')
axs[1].set_title('Phase Portrait: Pole 1')
axs[2].plot(q[:, 2], qDot[:, 2], color='orange')
axs[2].set_xlabel('Position [m]')
axs[2].set_ylabel('Velocity [m/s]')
axs[2].set_title('Phase Portrait: flywheel')
plt.tight_layout()
plt.show()

# * let's try to fitting for the arm force


# * unknowns:
# k: the spring coefficient of the cart
# F_a[t]: the force applied to the arms at time t


def inertial_and_coriolis_forces(params, q, qDot, qDotDot):
    f = model.mass_matrix(params, q)@qDotDot + model.coriolis(params, q, qDot)
    return np.atleast_2d(f).T

num_datapoints = q.shape[0]
b = np.zeros((2*num_datapoints, 1))
A = np.zeros((2*num_datapoints, 1+num_datapoints))
for index in range(num_datapoints):

    A[2*index, 0] = q[index, 0]
    A[2*index+1, index+1] = 1

    b[2*index, :] = inertial_and_coriolis_forces(params,
                                               q[index, :],
                                               qDot[index, :],
                                               qDotDot[index, :])[0, 0]
    b[2*index+1, :] = inertial_and_coriolis_forces(params,
                                               q[index, :],
                                               qDot[index, :],
                                               qDotDot[index, :])[2, 0]

K, residuals, rank, singular_values = np.linalg.lstsq(A, b, rcond=None)

spring_stiffness = K[0, 0]
flywheel_force_trajectory = K[1:, 0]
# print(f"Feedback gains: {K.T}")
print(f"residuals: {residuals}")
print(f"rank: {rank}")
# print(f"singular_values: {singular_values}")

# Let's try playing this back

# * let's now try fitting a feedback law instead.
# Let's hypothesize the feedback law is of the form:
# F_a[t] = K_a1 * x
# This would mean the arms are trying to counteract the cart motion
# through inertia. I think this is unlikely, but it's the simplest fit.

# * unknowns:
# k: the spring-stiffness
# K_a1: the feedback gain

num_datapoints = q.shape[0]
b = np.zeros((2*num_datapoints, 1))
A = np.zeros((2*num_datapoints, 2))
for index in range(num_datapoints):

    A[2*index, 0] = q[index, 0]
    A[2*index+1, 1] = q[index, 0]

    b[2*index, :] = inertial_and_coriolis_forces(params,
                                                 q[index, :],
                                                 qDot[index, :],
                                                 qDotDot[index, :])[0, 0]
    b[2*index+1, :] = inertial_and_coriolis_forces(params,
                                                   q[index, :],
                                                   qDot[index, :],
                                                   qDotDot[index, :])[2, 0]

K, residuals, rank, singular_values = np.linalg.lstsq(A, b, rcond=None)

spring_stiffness = K[0, 0]
flywheel_feedback = K[1, 0]
print(f"Feedback gains: {K.T}")
print(f"residuals: {residuals}")
print(f"rank: {rank}")
print(f"singular_values: {singular_values}")

# * Okay, let's simulate with these feedback gains and see how well it works

# * overload the forces function with the control law
def forces(params, x):
    F = params["feedback_gain"] @ x
    return F

model.forces = forces

n_dof = q.shape[1]

# let's add the feedback law to the params
feedback_gain = np.zeros((n_dof, 2*n_dof))
feedback_gain[0, 0] = spring_stiffness
feedback_gain[2, 0] = flywheel_feedback
params["feedback_gain"] = feedback_gain

# * now let's simulate it

from utils import euler_forward, rk4
ode_solver = "rk4"
x0 = np.stack((q[0, :], qDot[0, :])).flatten()

dt = 0.001
sim_time = 10
timesteps = int(sim_time/dt)
x_trajectory = np.zeros((timesteps, x0.size))

t = np.linspace(0, sim_time, timesteps)
x_trajectory = np.array(rk4(model.dxdt, x0, t, params))

# # Plot actual data first
fig, axs = plt.subplots(3, 1, figsize=(8, 8))
axs[0].plot(q[:, 0], qDot[:, 0], color='orange')
axs[0].plot(x_trajectory[:, 0], x_trajectory[:, 3], color='blue')
axs[0].set_xlabel('Position [m]')
axs[0].set_ylabel('Velocity [m/s]')
axs[0].set_title('Phase Portrait: Cart')

axs[1].plot(q[:, 1], qDot[:, 1], color='orange')
axs[1].plot(x_trajectory[:, 1], x_trajectory[:, 4], color='blue')
axs[1].set_xlabel('Position [rad]')
axs[1].set_ylabel('Velocity [rad/s]')
axs[1].set_title('Phase Portrait: Pole 1')

axs[2].plot(q[:, 2], qDot[:, 2], color='orange')
axs[2].plot(x_trajectory[:, 2], x_trajectory[:, 5], color='blue')
axs[2].set_xlabel('Position [m]')
axs[2].set_ylabel('Velocity [m/s]')
axs[2].set_title('Phase Portrait: flywheel')
plt.tight_layout()
plt.show()

print("end")