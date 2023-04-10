import pickle
import numpy as np
import matplotlib.pyplot as plt
# from models import cartpole
from models import cartpole

filename = 'simulated_cartpole_data.pickle'

infile = open(filename, 'rb')
data = pickle.load(infile)
infile.close()

q = data["positions"]
qDot = data["velocities"]
qDotDot = data["accelerations"]

# * let's try to use the data to fit for a feedback gain on the cart only
# * using a least-squares fit, A@x = b, where b are the inertial and coriolis
# * forces, and A is the matrix of the form [q, qDot]

params = cartpole.default_params()

def inertial_and_coriolis_forces(params, q, qDot, qDotDot):
    f = cartpole.mass_matrix(params, q)@qDotDot + cartpole.coriolis(params, q, qDot)
    return np.atleast_2d(f).T

num_datapoints = q.shape[0]
b = np.zeros((num_datapoints, 1))
A = np.zeros((num_datapoints, 4))
for index in range(num_datapoints):
    A[index, :] = np.concatenate((q[index, :], qDot[index, :]))
    b[index, :] = inertial_and_coriolis_forces(params,
                                               q[index, :],
                                               qDot[index, :],
                                               qDotDot[index, :])[0, 0]

K, residuals, rank, singular_values = np.linalg.lstsq(A, b, rcond=None)

print(f"Feedback gains: {K.T}")
print(f"residuals: {residuals}")
print(f"rank: {rank}")
print(f"singular_values: {singular_values}")

# * Now let's try fitting it again, but allowing for feedback gains on both the cart and the pole

b_full_feedback = np.zeros((2*num_datapoints, 1))
A_full_feedback = np.zeros((2*num_datapoints, 8))

for index in range(num_datapoints):
    A_full_feedback[2*index, :4] = np.concatenate((q[index, :], qDot[index, :]))
    A_full_feedback[2*index+1, 4:] = np.concatenate((q[index, :], qDot[index, :]))
    b_full_feedback[2*index:2*index+2, :] = inertial_and_coriolis_forces(params,
                                                            q[index, :],
                                                            qDot[index, :],
                                                            qDotDot[index, :])

K_full_feedback, residuals_full_feedback, rank_full_feedback, singular_values_full_feedback = np.linalg.lstsq(A_full_feedback, b_full_feedback, rcond=None)

print(f"Feedback gains: {K_full_feedback.T}")