# Ryu Kuo 2021
**An optimality principle for locomotor central pattern generators**

---

**Tags:** #central_pattern_generators #CPG #reflex #reflex_circuit #neuroscience #locomotion #gait #fictive_locomotion #control 

---

**Related:** [[Six Determinants and Inverted Pendulum - Kuo 2007]] [[Human Central Pattern Generator - Does it Exist? Minassian 2017]]

---

## Key Definitions
**Central Pattern Generator:** Neural circuit that generates pre-programmed, rhythmically timed motor commands

**Reflex Circuit:** Neural circuit that produces motor patterns triggered by sensory feedback

**Feedforward Control:** Rhythm/time based control with no sensory input/awareness 

**Feedback Control:** Control based on sensory feedback/awareness of current limb state

**State Estimation:** an internal model of the body is used to predict the expected state and sensory information/feedback from sensors is used to correct the state estimate

**Process Noise:** Represents disturbances and uncertainty in the environment or internal model

**Fictive Locomotion:** Production of locomotive motor commands in the absence of movement

**Sensory Feedback Gain:** Model parameter in the controller to set the relative amount of influence feedforward and feedback components had, ranges from 0 (no feedback) to infinity (no feedforward)


---

## Key Takeaways
1. CPGs and reflex circuits can each independently control locomotion, and operate on opposing types feedback/input. Yet, they appear to work together to control normal locomotion. The central question is *how their control authority is optimally shared*.
	- CPGs function with no sensory feedback and tonic (slow) descending input. they are capable of controlling locomotion through pure feedforward control.
	- Reflex circuits however, operate through full feedback control, acting responsively to sensory feedback
	- Controllers exist that combine these feedforward and feedback models, with the benefits of increasing robustness (e.g. in uneven terrain) from feedback control and the ability to vary walking speed, adjust inter-limb coordination, enhance stability from feedforward control. However, these designs are typically *ad hoc,* making it difficult to compare models or generalize findings
2. Optimization principles gives quantitative and objective performance measures for the models balance of feedforward and feedback controls, preferable to prior ad hoc methods
3. With state estimation, an internal model of the body if used to predict the expected state (provided by feedforward CPGS) which is then corrected by feedback from sensory information (provided by reflex circuits).
	- State estimation is required because a system's state can only be known imperfectly 
4. This study tests a state estimator based CPG controller on a dynamic walking model
	- The model optimized not for walking performance like prior ad hoc methods. Rather it optimized for accurate state estimation
	- An alterable sensory feedback gain was added to change the relative influence feedforward and feedback control had across tests
5. Feedforward and feedback systems are susceptible to/robust against different types of noise, and thus a mix of both can have optimal performance in situations where both types of noise are present. They have complementary weaknesses and strengths.
	- Full feedforward systems are incapable of dealing with excess process noise, and will fall if perturbed too much during their normal gait due to inability to respond to change in conditions. Full feedback systems are robust in these conditions.
	- Full feedback systems are incapable of dealing with excess signal noise. When the system is incorrect about current limb states, it provides erroneous motor commands which leads to a fall. Full feedforward systems are unaffected by sensor noise because they ignore sensor inputs. 
	- The theoretically predicted optimal feedback gain, balancing feedforward and feedback control in relation to process and sensor noise, yielded the best walking performance as well (in economy of transport, step length variability, and number of falls)
		- Changing the sensory feedback gain to higher or lower than the predicted optimum led to worse walking performance, as well as an incorrect state estimate
		- Relative changes in the amount of sensor and process noise change the optimal sensory feedback gain
		- Full removal of sensors, and thus feedback, yielded fictive locomotion that was interpreted as a side effect of incorrect state estimation. This explains fictive locomotion as an emergent behavior 
6. The state estimator model created can be separated from control, allowing one optimal state estimator to be used across various control systems
	- "It is better to control with state rather than time"
	- State estimation may be suitable for other movements than locomotion
7. Reconciled optimal control and estimation with biological CPGs
	- Showed how biological CPG can be interpreted as a state estimator without changing neural circuitry
	- Provide a model where CPGs and sensory feedback work together to optimally interact with a noisy world

---

## Limitations
1. Model places few constraints on neural representation, because there are many ways to achieve estimation function - i.e. it does not do much to inform us about what is actually going on in human locomotion control
2. State estimation is less important in systems with damped limb dynamics and inherently stable body postures
3. Model may both over and under complicate actual neural circuitry
	- Task constraints, especially speed, may favor pure feedback or pure feedforward control in some animals
	- On the other hand, much neural circuitry is more complex than the given model, and animals have far more degrees of freedom than this model accounts for
4. Simplified model of walking was used
	- Limited degrees of freedom in the model
	- Control was limited to simple hip torque, instead of trailing leg push off