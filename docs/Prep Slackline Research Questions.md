# Prep Slackline Project Research Question

## Comparison to Physical Models/Simulations

### Free Body Diagram of Slackliner Standing

![Slacklining Free Body Diagram](https://i.imgur.com/ewEGpD3.jpg)

The forces on the COM of the slackliner include the downward force of gravity, and whatever stabilising force the slackliner is able to enact with their body (through leg muscles, repositioning other limbs to move the COM, torque). There is also a spring restoring force on the line, with both a vertical component counteracting the force of gravity on the COM, and a horizontal component trying to recenter the line between the anchors.

The breakdown of the restoring force on the slackline is shown below in more detail, from http://slackbro.pythonanywhere.com/duffing/

![Slackline Free Body Diagram](https://i.imgur.com/Tng9MgL.png)



### Compare Simple Model From Data to Pendulum Models

Simple leg model, where there is some control signal adjusting for the error from `COM-BOS = 0`. !Write more here about pendulums!

Is this the right model, at least for this level of understanding?

One means of comparison is comparing the state space of the model to the state space of the collected slackline data. 
 - Do they have the same attractors/repellers? Bifurcations? 
 - Is it possible to get an idea of the vector field of each, and how do they compare?

Another means of comparison would be taking the model parameters from actual data, and applying them to the model.
- Can the model balance starting at the parameters from an arbitrary point in the data?
- Does putting in the parameters from sufficiently close to a fall (in real data) also cause the model to fall?

## Spinal Level Reflexes

How much, if any of the "work" of balancing being done by spinal level reflexes vs. by "the brain" (could be broken down to more parts).

Do Fourier analysis on data to see if frequencies match the frequencies seen in spinal level reflexes.
- Having trouble implementing numpy fft on the data.
- How many peaks might the FFT give from the COM-BOS signal? How many of those are from properties of the line (spring properties, resonance) vs from the slackliner?

Talk to Kylie more about this.

How much is voluntary control?

H Reflex:
 - Hoffman Reflex
- How to sense gain of muscle proprioceptors - How strong does a signal have to be to initiate a reflex for corrective movement?
- Study on how people walk on beams - reflex gain is lower when walking on a beam vs a treadmill - time spent in swing phase was reduced compared to normal walking
- H Reflex could be found in the beginner slackline models

 
Reflex Frequencies:
- Fusimotor Drive: Proprioceptive (afferent) Gamma Motor Neuron (1a), H Reflex (1a meets contracting (efferent) motor neuron), Tendon Reflexes (1b)
- Reflexes split into Muscle Reflexes, Tendon Reflexes, Cutaneous 

Kiley couldn't cite specific frequencies.

## Reaction vs Anticipation

How much of balancing on a slackline is reaction to the current state of the system, and how much is anticipating what the line will do and how the body will respond?

How can we tell what is reactive vs anticipatory?