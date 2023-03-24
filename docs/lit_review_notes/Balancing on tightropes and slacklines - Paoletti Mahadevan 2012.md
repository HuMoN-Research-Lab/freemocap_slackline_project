# Paoletti Mahadevan 2012
**Balancing on tightropes and slacklines**

---

**Tags:** #control #slackline #dynamic_balance 

---

**Related:** 

---

## Key Definitions

---

## Key Takeaways
1.  Investigating rope balancing to see how the neuromechanical dynamics of the body couple with external dynamics of the reactive moving system. A key focus is understanding the ways the body is aware of or estimates its current position in space and relative to the system.
2. They propose a simple mechanical model for the body rope system, including a "plausible" sensory motor feedback control system based on the vestibular system.
	1. Model is a cart pole, where the tracks of the cart are circular.
	2. Humans balance by using their arms to generate torque.
	3. The scaled sag parameter determines if the line is a slackline or tight rope.
3. They analyze the linearized dynamics of their model and construct an optimal feedback controller for cases with limited information about the state space occupied.
	1. Claim it is unlikely humans can take separate measurements to determine the full state of the system, i.e. the values and velocity of both the angular displacement of the line and the rotation of the body.
	2. The visual system can provide precise information about the orientation of the body, but at a delay slower than seems necessary to make the balance corrections needed.
	3. Claim proprioception gives inaccurate information while balancing due to movement of the feet.
	4. Given the previous two points, only vestibular (inner ear) balance seems fast and accurate enough. 
	5. Assume that only accurate measurement of velocities is available for feedback control, as this can be provided by the vestibular system and is sufficient for balance
	6. Qualitative behavior of the system is relatively equivalent when allowing back in visual or proprioceptive awareness, or when varying the max producible torque by a factor of ten.
4. They are able to prove that their (linearized) model is completely controllable and observable, which means there is a non-unique feedback control strategy to stabilize the pendulum.
	1. This linearized control strategy was then simulated on the full nonlinear model
	2. When the distance R (stand in for body position along rope length, 0 when person is at anchor, approaches 0 when person is in the middle of arbitrarily long line, and also sag) approaches 0 it can get very unstable, and near infinite R is actually stable. There is an ideal range of r, near body height, where stabilization is fast and requires very low force and energy output.
5. The final section discusses special cases and additions to the model
	1. When mass has a large impact on sag (high stretch line), the model predictions still mostly hold.
	2. *When sag is smaller, vertical and horizontal oscillation s are uncoupled and the rope acts more like a a spring returning the cart to center, and the motion of the cart is primarily horizontal.* This describes roughly how we have modeled the system.

---

## Limitations
1. Model only has one degree of freedom for the body, which represents large scale postural control. Smaller limb movements are explicitly ignored.
2. Treat the rope primarily as a track for the "cart", i.e. they do not model any elastic feedback for the primary modeling
3. Dissipation and damping are assumed to be equal to the action of torque
4. Overestimate the reliance on vestibular control, based on experience of how much people rely on vision. They are correct it is apparently sufficient (probably plus proprioception), but not that it is the "normal" strategy
5. Generally seems a little misguided on understanding the realities of rope balancing, i.e. the last paragraph of the appendix.