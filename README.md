# Freemocap Slackline Project

https://humon-research-lab.github.io/freemocap_slackline_project/

This is the repo for the project that will do biomechanical analysis of slackline data, especially looking at the relationship between Center of Mass (CoM) and Base of Support (BoS). Possibly using 'cart and pendulum,' 'PD' controller types of approaches.

## ODEPendulum.py 

Models and displays/saves an animation of a simple pendulum. Uses Scipy's ODE solver and an object-oriented structure in order to make it a solid jumping off point for more complex pendulum modeling and animations, including cart and pendulum and double pendulums.

The initial parameters, including simulation length, pendulum angle and velocity, and force of gravity, can all be changed in the ```__init__``` function of the ```Pendulum``` class. The animation can be displayed, saved, or both by changing the parameters of the ```main``` function.

https://user-images.githubusercontent.com/24758117/188958046-3e8bcb5d-9923-43c9-8f8a-59e73c5bc310.mp4

## CartAndPendulum.py

Models and animates a cart and pendulum controlled by a PID controller. It is built off of the structure of ODEPendulum.py, and is able to balance the pendulum from a range of initial conditions within 5 seconds. It must start with a roughly upright pendulum - it is not able to perform a swing-up operation.

The initial parameters, including simulation length, pendulum angle and velocity, cart position and velocity, and desired cart position, can all be changed in the ```__init__``` function of the ```Pendulum``` class. The PID controller can be altered by changing the gains in the ```set_pid_gains``` function of the ```Pendulum``` class. The animation can be displayed, saved, or both by changing the parameters of the ```main``` function.

https://user-images.githubusercontent.com/24758117/188962309-ee423378-844a-433e-910a-6b273f161ebf.mp4

## DoublePendulum.py

Models and animates a double pendulum without a controller or any friction force. It is built off of the structure of ODEPendulum.py, and shows the highly chaotic nature of double pendulums.

The initial parameters, including simulation length, pendulum angles, lengths, masses, and velocities, can all be changed in the ```__init__``` function of the ```DoublePendulum``` class. The animation can be displayed, saved, or both by changing the parameters of the ```main``` function.

https://user-images.githubusercontent.com/24758117/189504545-333fe709-f0cd-4343-ad4a-5de4c7616d99.mp4

## SpringedCartAndPendulum.py

A very similar cart and pendulum system to CartAndPendulum.py, but with a horizontal spring attached to the cart, which pulls on the cart back towards the origin. The cart is controlled with a PD controller, and within a range of spring constants is still able to balance the pendulum. A derivation of simulation parameters related to the spring is given in SpringedCartAndPendulumJustification.md. 

The initial parameters, including spring constant, system mass, pendulum angle and velocity, cart position and velocity, and desired cart position, can all be changed in the ```__init__``` function of the ```Pendulum``` class. The PID controller can be altered by changing the gains in the ```set_pid_gains``` function of the ```Pendulum``` class. The animation can be displayed, saved, or both by changing the parameters of the ```main``` function.

https://user-images.githubusercontent.com/24758117/189793095-8fa1844b-6de6-453a-bd30-e3aaa5d63fc9.mp4
