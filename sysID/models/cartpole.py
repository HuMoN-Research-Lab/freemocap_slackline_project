import numpy as np


# class CartPole:

    # def __init__():
    #     pass
        # .params = .default_params()

def default_params():
    params = {
        "mass_cart": 1.0,
        "mass_pendulum": 0.5,
        "length_pendulum": 0.5,
        "gravity": 9.81,
        "spring_cart": 0.,
    }
    return params


def mass_matrix(params, x):
    M = np.zeros((2, 2))
    M[0, 0] = params["mass_cart"] + params["mass_pendulum"]
    M[0, 1] = - params["mass_pendulum"] * params["length_pendulum"] * np.cos(x[1])
    M[1, 0] = - params["mass_pendulum"] * params["length_pendulum"] * np.cos(x[1])
    M[1, 1] = params["mass_pendulum"] * params["length_pendulum"]**2

    # assert (np.transpose(M) == M).all(), "M is not symmetric: {}".format(M)
    # assert (np.linalg.det(M) > 0.), "M is not positive definite: {}".format(M)

    return M

# * attempt by GPT to vectorize mass_matrix, left in here for fun for now
# def mass_matrix(params, x):
#     n = x.shape[1]
#     M = np.zeros((2, 2, n))
#     M[0, 0, :] = params["mass_cart"] + params["mass_pendulum"]
#     M[0, 1, :] = params["mass_pendulum"] * params["length_pendulum"] * np.sin(x[1, :])
#     M[1, 0, :] = M[0, 1, :]
#     M[1, 1, :] = params["mass_pendulum"] * params["length_pendulum"]**2
#     return np.transpose(M, (2, 0, 1))


def coriolis(params, x, qDot=None):
    # hacky: we're assuming x input if qDot is None, and (q, qDot) otherwise.
    C = np.zeros(2)
    if qDot is None:
        C[0] = params["mass_pendulum"] * params["length_pendulum"] * np.sin(x[1]) * x[3] ** 2
        C[1] = - params["mass_pendulum"] * params["gravity"] * params["length_pendulum"] * np.sin(x[1])
    else:
        C[0] = params["mass_pendulum"] * params["length_pendulum"] * np.sin(x[1]) * qDot[1] ** 2
        C[1] = - params["mass_pendulum"] * params["gravity"] * params["length_pendulum"] * np.sin(x[1])
    return C


def forces(params, x):
    F = np.zeros(2)
    F[0] = - params["spring_cart"] * x[0]
    return F


def potential_energy(params, x):
    spring_energy = 0.5 * params["spring_cart"] * x[0]**2
    gravitational_energy = (params["mass_pendulum"] * params["gravity"]
                            * params["length_pendulum"] * (np.cos(x[1]) + 1))
    return spring_energy + gravitational_energy


def kinetic_energy(params, x):
    cart_energy = params["mass_cart"]/2. * x[2]**2
    pendulum_energy = (params["mass_pendulum"]/2.
                       * ((params["length_pendulum"] * x[3])**2
                          + x[2]**2
                          - 2*params["length_pendulum"]*x[2]*x[3]*np.cos(x[1])))
    return cart_energy + pendulum_energy


def dxdt(t, x, params):
    M = mass_matrix(params, x)
    C = coriolis(params, x)
    F = forces(params, x)
    acceleration = np.linalg.lstsq(M, F - C, rcond=None)[0]
    # or
    # acceleration = np.matmul(np.linalg.pinv(M), (F - C))
    assert (x.size/2 == acceleration.size)
    n_dofs = x.size//2
    return np.concatenate((x[n_dofs:], acceleration))
