# Springed Cart and Pendulum Justification
## Deriving the Effect of the Spring
In order to add a horizontal spring to the PID controlled cart and pendulum simulation in 'CartAndPendulum.py', we use Hooke's Law which describes the restoring force from a linear spring. Hooke's Law states that F = -kx , or that the restoring force is equal to the spring constant k times the distance from equilibrium x. We are interested in how the spring affects the cart's acceleration, so we need to substitute the right hand side of Newton's Law F = ma into Hooke's Law to turn our restoring force into an acceleration term. This gives us ma = -kx, which rearranges to give us a = -kx/m, or in words, acceleration = -(spring constant times distance to equilibrium) / mass. The spring is attached to the cart, so this acceleration only directly affects the acceleration of the cart. The total acceleration of the cart then affects the angular acceleration of the pendulum, as shown by the free body diagram below:

![CartAndPendulumFreeBody](https://user-images.githubusercontent.com/24758117/189792820-dbcfd5b7-f9f7-453f-a3f1-1574754c8a75.jpg)

The angular acceleration of the pendulum is found by taking the vertical component of the acceleration (due to gravity) times the sine of the pendulum angle, and the horizontal component of the acceleration (the total acceleration of the cart) times the cosine of the pendulum angle, and then dividing both by the pendulum length. As long as we include the acceleration due to the spring whenever we write the total acceleration of the cart, we will have handled any effect the spring has on the pendulum.

## Turning it into Code
The original code for our cart and pendulum derivatives is as follows:

```# derivative of pendulum angle (angular velocity)
derivative_array[0] = current_angular_velocity

# derivative of angular velocity (angular acceleration)
derivative_array[1] = (self.gravity * np.sin(current_pendulum_angle) - pid_controller_output * np.cos(current_pendulum_angle)) / self.length

# derivative of cart position (cart velocity)
derivative_array[2] = current_cart_velocity

# derivative of cart velocity (cart acceleration)
derivative_array[3] = pid_controller_output
```

In this case, the only cart acceleration was due to the output of our PID controller. This means to factor in the spring acceleration, we can replace our pid_controller_output with (pid_controller_output - spring_acceleration), where spring_acceleration = (self.spring_constant * current_cart_position)/self.mass. This gives us the updates derivatives below:

```# derivative of pendulum angle (angular velocity)
derivative_array[0] = current_angular_velocity

# derivative of angular velocity (angular acceleration)
derivative_array[1] = (self.gravity * np.sin(current_pendulum_angle) - (pid_controller_output - spring_acceleration) * np.cos(current_pendulum_angle)) / self.length

# derivative of cart position (cart velocity)
derivative_array[2] = current_cart_velocity

# derivative of cart velocity (cart acceleration)
derivative_array[3] = pid_controller_output - spring_acceleration
```
