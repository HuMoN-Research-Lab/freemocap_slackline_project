# Freemocap Slackline Project

This is the repo for the project that will do biomechanical analysis of slackline data, especially looking at the relationship between Center of Mass (CoM) and Base of Support (BoS). Possibly using 'cart and pendulum,' 'PD' controller types of approaches.

## ODEPendulum.py 

Models and displays/saves an animation of a simple pendulum. Uses Scipy's ODE solver and an object-oriented structure in order to make it a solid jumping off point for more complex pendulum modeling and animations, including cart and pendulum and double pendulums.

The initial parameters, including simulation length, pendulum angle and velocity, and force of gravity, can all be changed in the ```__init__``` function of the ```Pendulum``` class.

https://user-images.githubusercontent.com/24758117/188958046-3e8bcb5d-9923-43c9-8f8a-59e73c5bc310.mp4

## CartAndPendulum.py

Models and animates and cart and pendulum controlled by a PID controller. It is built off of the structure of ODEPendulum.py, and is able to balance the pendulum from a range of initial conditions within 5 seconds. It must start with a roughly upright pendulum - it is not able to perform a swing-up operation.

The initial parameters, including simulation length, pendulum angle and velocity, cart position and velocity, and desired cart position, can all be changed in the ```__init__``` function of the ```Pendulum``` class. The PID controller can be altered by changing the gains in the ```set_pid_gains``` function of the ```Pendulum``` class. The animation can be displayed, saved, or both by changing the parameters of the ```main``` function.

https://user-images.githubusercontent.com/24758117/188962309-ee423378-844a-433e-910a-6b273f161ebf.mp4

