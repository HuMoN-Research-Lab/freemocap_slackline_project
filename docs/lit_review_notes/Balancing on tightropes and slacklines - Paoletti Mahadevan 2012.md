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

### Steve's comments on the limitations

1. I agree, though what they do is to some extent reasonable: they do not model the flywheel explicitly, but they do still model the torque that could be exerted by the flywheel (e.g. arms). Their control input $F^\alpha$ is not representing ankle torque, but the arm torque, simply transferred down to the pivot joint. This is correct, and a much simpler model that I should also have suggested as a first pass. So, what is lost by not modeling the actual flywheel state?
   - If you don't model the flywheel, you ignore the state of the flywheel. This is fine, if it is okay to ignore their position/velocity. But it means you cannot impose constraints on the flywheel (arm) maximum position or velocity, which I would argue is actually an important constraint. They actually talk about these points in appendix D (as you mention in point 5.). So one thing we probably want to show is that these constraints are indeed important. I think they are, though I don't know which constraint is the limiting one (or if both are). Identifying that could be interesting.
2. Not sure that's really a significant limitation: the gravitation force they have on $R$ will be very similar to the spring force that we've modeled. I think at this level of abstraction, neither is super "faithful" to a first-principles view of the system, and to decide which is better you'd have to look at data.
3. I didn't pick on this, where did you see that?
4. Yeah, I also think visual vs. vestibular might be the most interesting thing to look at.
   - can we model an estimator that uses both visual and vestibular feedback loops, each with their respecitve delays?
   - if yes, then we could compare the feedback gains with both, vs. feedback gains with just vestibular, see if it is very different (e.g. we have two contorl inputs, flywheel and arm-CoG. If you have vision, should you rely more on keeping the CoG centered, compared to if don't?), and then validate that prediction with a real-world experiment  (e.g. blindfolded).
5. You're the expert :)  
6. Aside: to me it seemed that their torque upperbound is rather high, but I don't have any real reasoning behind it. Do you have better thoughts on this?  
7. Their note in the appendix that "the qualitative behavior of the system is insensitive to the exact value for $F_{max}$$ is imho rather misleading, since they only checked for increasing this upper bound. I would guess (as discussed above) that the constraints are actually quite important, but of course if you actually enforce them, not if you relax them more.  