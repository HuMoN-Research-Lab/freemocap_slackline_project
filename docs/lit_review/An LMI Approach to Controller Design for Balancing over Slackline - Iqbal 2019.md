# Iqbal 2019
**An LMI Approach to Controller Design for Balancing over Slackline**

---

**Tags:** #control #slackline #balance #dynamic_balance 

---

**Related:** [[Balancing on tightropes and slacklines - Paoletti Mahadevan 2012]]

---

## Key Definitions
1. **Linear Matrix Inequality (LMI):** A linear expression of matrices with efficient numerical methods that is used to solve optimization problems.

---

## Key Takeaways
1. Author extends the simple inverted pendulum studied in [[Balancing on tightropes and slacklines - Paoletti Mahadevan 2012]] by adding an internal stabilizing torque generation method previously studied in the context of bar balancing.
	1. The model resembles a standard linear inverted pendulum but with a crossbeam representing the arms, giving the whole model a cross like appearance
	2. Assume vestibular sensing of absolute body rotation rate, and the estimation of everything else is handled by a minimal order estimator.
	3. Design their "neural stabilizing" controller with LMI techniques
	4. "utilize Lyapunov energy functions to ensure stability of the closed-loop system."
2. The model is based on a cart on a circular pendulum
	1. The arms are represented by a single bar segment that is "normally" at 90 degrees to the body 
	2. The body angle is measured relative to the tangent of the curve, not to gravity
	3. Use $\phi$ to denote angle of slackline deflection (angular deflection from resting state of line) and $\theta$ to denote angle of body orientation relative to $\phi$ 
	4. The only force acting on the slackliner is the slackline reaction force (and presumably gravity)
3. Had to construct a linear model of the slackliner to use LMI methods
4. The state estimation inputs made little difference on the controller performance
5. Concluded simple inverted pendulum is inadequate to capture body mechanics of slacklining
	1. Even calls this more complicated model a "gross oversimplification" of the actual phenomenon
6. Compared the LMI output to a Linear Quadratic Regular (LQR) and a Pole Placement Controller
	1. LMI performed similarly to LQR, and pole placement had significantly better dynamic stability to LMI and LQR
	2. LMI can guarantee stability, but provide minimal control over dynamic stability
---

## Limitations
1. Use the same "curved cart track" model design as the previous controller study
2. Vestibular based state estimator did not include delays, which is likely to have a large effect on the system
3. Mention a lot of technical choices leading to different results in the discussion section