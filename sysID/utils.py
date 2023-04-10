import numpy as np

def euler_forward(params, model, x, dt=0.001):
    M = model.mass_matrix(params, x)
    C = model.coriolis(params, x)
    F = model.forces(params, x)
    acceleration = np.linalg.lstsq(M, F - C, rcond=None)[0]
    # acceleration = np.matmul(np.linalg.pinv(M), (F - C))
    return x + np.concatenate((x[2:], acceleration))*dt

