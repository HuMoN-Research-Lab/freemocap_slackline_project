import numpy as np
import matplotlib.pyplot as plt
from utils import euler_forward, rk4
from models import cartpole_arm_flywheel as model

ode_solver = "rk4"

x = np.array([0.,  # cart position
              0.01,  # pendulum position
              0.,  # arm position
              0.,  # flywheel position
              0.,  # cart velocity
              0.,  # pendulum velocity
              0.,  # arm velocity
              0.]) # flywheel velocity

params = model.default_params()
dt = 0.001
sim_time = 10

timesteps = int(sim_time/dt)

x_trajectory = np.zeros((timesteps, x.size))

if ode_solver == "euler_forward":
    for i in range(timesteps):
        x = euler_forward(params, model, x, dt=dt)
        x_trajectory[i, :] = x
elif ode_solver == "rk4":
    t = np.linspace(0, sim_time, timesteps)
    x_trajectory = np.array(rk4(model.dxdt, x, t, params))

potential = np.zeros(timesteps)
kinetic = np.zeros(timesteps)
for i in range(timesteps):
    potential[i] = model.potential_energy(params, x_trajectory[i, :])
    kinetic[i] = model.kinetic_energy(params, x_trajectory[i, :])

energy_traj = potential + kinetic
plt.figure(3)
plt.plot(energy_traj)
plt.xlabel('timesteps')
plt.ylabel('Energy [joules]')
plt.title('Total energy')
plt.figure(4)
plt.title("Kinetic and Potential energy")
plt.plot(potential)
plt.plot(kinetic)
plt.xlabel('timesteps')
plt.ylabel('Energy [joules]')
plt.legend(['potential energy', 'kinetic energy'])
plt.show()
print(f"Energy error: {(np.max(energy_traj) - np.min(energy_traj))/energy_traj.mean()*100:.5f} %")

# q: how do I save the simulated data (x_trajectory) to a file with pickle

# save x_trajectory to a pickle file
import pickle
import os

filename = 'simulated_arm_flywheel_data.pickle'

# if not os.path.exists(path_to_file):
#     os.makedirs(path_to_file)
n_dofs = x.size//2
accelerations = np.diff(x_trajectory[:, n_dofs:], axis=0)/dt
q = x_trajectory[:-1, :n_dofs]
qDot = x_trajectory[:-1, n_dofs:]
qDotDot = accelerations[:, :]

data_to_save = {"positions": q, "velocities": qDot, "accelerations": qDotDot}

with open(filename, 'wb') as outfile:
    pickle.dump(data_to_save, outfile)
outfile.close()

# to load this data, do:
# infile = open(filename, 'rb')
# data = pickle.load(infile)
# infile.close()