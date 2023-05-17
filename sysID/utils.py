import numpy as np

def euler_forward(params, model, x, dt=0.001):
    M = model.mass_matrix(params, x)
    C = model.coriolis(params, x)
    F = model.forces(params, x)
    acceleration = np.linalg.lstsq(M, F - C, rcond=None)[0]
    # acceleration = np.matmul(np.linalg.pinv(M), (F - C))
    return x + np.concatenate((x[2:], acceleration))*dt

def rk4(f, y0, t, *args):
    dt = t[1] - t[0]
    y = [y0]
    
    for i in range(1, len(t)):
        ti = t[i - 1]
        yi = y[-1]
        
        k1 = f(ti, yi, *args)
        k2 = f(ti + dt / 2, yi + dt * k1 / 2, *args)
        k3 = f(ti + dt / 2, yi + dt * k2 / 2, *args)
        k4 = f(ti + dt, yi + dt * k3, *args)
        
        y_new = yi + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        y.append(y_new)
    
    return y