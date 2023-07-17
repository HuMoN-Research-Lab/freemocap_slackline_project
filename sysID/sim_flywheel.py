import numpy as np
import matplotlib.pyplot as plt
from utils import euler_forward, rk4
from models import cartpole_flywheel as model

ode_solver = "rk4"

x = np.array([0, 3.14, 0, 0, 0, 0])

params = model.default_params()
params["spring_cart"] = 1
params["inertia_flywheel"] = 50.
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

plt.figure(1)
plt.title("Cart position and velocity")
plt.plot(x_trajectory[:, 0], x_trajectory[:, 3])
plt.scatter(x_trajectory[0, 0], x_trajectory[0, 3], c="r")
plt.xlabel("cart position")
plt.ylabel("cart velocity")
plt.figure(2)
plt.title("Flywheel position and velocity")
plt.plot(x_trajectory[:, 5])
# plt.scatter(x_trajectory[0, 2], x_trajectory[0, 5], c="r")
plt.plot(x_trajectory[:, 4], c='g')
# plt.scatter(x_trajectory[0, 1], x_trajectory[0, 4], c="g")
plt.xlabel("flywheel position")
plt.ylabel("flywheel velocity")
# plt.figure(3)
# plt.title("Pendulum position and velocity")
# plt.plot(x_trajectory[:, 1], x_trajectory[:, 4])
# plt.scatter(x_trajectory[0, 1], x_trajectory[0, 4], c="r")
# plt.xlabel("Pendulum position")
# plt.ylabel("Pendulum velocity")
# plt.show()
# plt.close()


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

filename = 'simulated_flywheel_data.pickle'

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