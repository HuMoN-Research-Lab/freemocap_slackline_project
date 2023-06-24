import numpy as np
import matplotlib.pyplot as plt
from utils import euler_forward, rk4
from models import cartpole as model

ode_solver = "rk4"

x = np.array([0, 0.01, 0, 0])

params = model.default_params()
params["spring_cart"] = 1
dt = 0.005
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

plt.figure(1)
plt.title("Cart position and velocity")
plt.plot(x_trajectory[:, 0], x_trajectory[:, 2])
plt.scatter(x_trajectory[0, 0], x_trajectory[0, 2], c="r")
plt.xlabel("cart position")
plt.ylabel("cart velocity")
plt.figure(2)
plt.title("Pole position and velocity")
plt.plot(x_trajectory[:, 1], x_trajectory[:, 3])
plt.scatter(x_trajectory[0, 1], x_trajectory[0, 3], c="r")
plt.xlabel("pole position")
plt.ylabel("pole velocity")
# plt.show()


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
print(f"Energy error: {(energy_traj[-1] - energy_traj[0])/energy_traj.mean()*100:.5f} %")

# q: how do I save the simulated data (x_trajectory) to a file with pickle

# save x_trajectory to a pickle file
import pickle
import os

filename = 'simulated_cartpole_data.pickle'

# if not os.path.exists(path_to_file):
#     os.makedirs(path_to_file)

accelerations = np.diff(x_trajectory[:, 2:], axis=0)/dt
q = x_trajectory[:-1, :2]
qDot = x_trajectory[:-1, 2:]
qDotDot = accelerations[:, :]

data_to_save = {"positions": q, "velocities": qDot, "accelerations": qDotDot}

with open(filename, 'wb') as outfile:
    pickle.dump(data_to_save, outfile)
outfile.close()

# to load this data, do:
# infile = open(filename, 'rb')
# data = pickle.load(infile)
# infile.close()