import numpy as np


def default_params():
    params = {
          "mass_cart": 1, # mass pendulum * 0.14, kg, based on estimates here https://exrx.net/Kinesiology/Segments
          "mass_pendulum": 72.6, # appoximate weight, kg
          "length_pendulum": 1.206, # mean from data, m
          "spring_cart": 1,
          "gravity": 9.81    
    }   
    return params

def mass_matrix(params, x):
    M = np.zeros((3, 3))
    M[0, 0] = params["mass_cart"] + params["mass_pendulum"]
    M[0, 1] = - params["mass_pendulum"] * params["length_pendulum"] * np.cos(x[1])
    M[0, 2] = params["mass_arm"]
    M[1, 0] = - params["mass_pendulum"] * params["length_pendulum"] * np.cos(x[1])
    M[1, 1] = params["mass_pendulum"] * params["length_pendulum"]**2
    M[1, 2] = - params["mass_pendulum"] * params["length_pendulum"] * np.cos(x[1])
    M[2, 0] = params["mass_arm"]
    M[2, 1] = - params["mass_pendulum"] * params["length_pendulum"] * np.cos(x[1])
    M[2, 2] = params["mass_arm"]
    return M

def coriolis(params, x, qDot=None):
    # hacky: we're assuming x input if qDot is None, and (q, qDot) otherwise.
    C = np.zeros(3)
    if qDot is None:
        C[0] = params["mass_pendulum"] * params["length_pendulum"] * np.cos(x[1]) * x[3] ** 2
        C[1] = - params["mass_pendulum"] * params["gravity"] * params["length_pendulum"] * np.sin(x[1])
        C[2] = 0
    else:
        C[0] = params["mass_pendulum"] * params["length_pendulum"] * np.cos(x[1]) * qDot[1] ** 2
        C[1] = - params["mass_pendulum"] * params["gravity"] * params["length_pendulum"] * np.sin(x[1])
        C[2] = 0
    return C

def forces(params, x):
    F = np.zeros(3)
    F[0] = - params["spring_cart"] * x[0]
    F[2] = 0 #TODO: this should represent the control input
    return F

def potential_energy(params, x):
    spring_energy = 0.5 * params["spring_cart"] * x[0]**2
    gravitational_energy = (params["mass_pendulum"] * params["gravity"]
                            * params["length_pendulum"] * np.cos(x[1]))
    return spring_energy + gravitational_energy

def kinetic_energy(params, x):
    cart_energy = params["mass_cart"]/2. * x[2]**2
    pendulum_energy = (params["mass_pendulum"]/2.
                       * ((params["length_pendulum"] * x[3])**2
                          + x[2]**2
                          + 2*params["length_pendulum"]*x[2]*x[3]*np.sin(x[1])))
    return cart_energy + pendulum_energy

def dxdt(t, x, params):
    M = mass_matrix(params, x)
    C = coriolis(params, x)
    F = forces(params, x)
    acceleration = np.linalg.lstsq(M, F - C, rcond=None)[0]
    # or
    # acceleration = np.matmul(np.linalg.pinv(M), (F - C))
    return np.concatenate((x[2:], acceleration))