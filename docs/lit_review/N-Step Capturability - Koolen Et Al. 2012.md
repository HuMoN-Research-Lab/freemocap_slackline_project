# Koolen Et Al. 2012
 **Capturability-based analysis and control of legged locomotion, Part 1: Theory and application to three simple gait models** 

---

**Tags:** #inverted_pendulum #n-step_capturability #robotics #locomotion #control #dynamic_balance 

---

**Related:** [[Extrapolated COM - Hof 2007]] [[The Condition for Dynamic Stability - Hof Et Al 2005]] [[Six Determinants and Inverted Pendulum - Kuo 2007]]

---


## Key Definitions
**N-Step Capturability:** the ability of a legged system to come to a stop without falling by taking N or fewer steps

**N-Step Capture Region:** Set of points to which a legged system in a given state can step to become (N-1)-step capturable

**N-Step Capturability Margin:** the size of the N-step capture region

**N-Step Viability Basin:** The set of all capturable states

**Viability Kernel:** The set of all states from which failed states can be avoided

**Captured:** The system has come to a stop

**Gait sensitivity Norm:** the sensitivity of a given gait measure, such as step time, to a given disturbance type, such as a step-down in terrain, using a simulated model or experimental data.

--- 

## Key Takeaways
1.  **Main goal** is to avoid a fall - refigured for computational simplicity in order ensure ability to come to a stop in a given number of steps
	1. application of goal is computationally tractable controller design
	2. effectively quantifying closeness to falling is a known problem
2. Create simple models that can serve as approximations for control of legged locomotion - models based on inverted pendulum
	1. with simple point foot
	2. with finite sized foor capable of exerting pressure
	3. with finite sized foot and reaction mass capable of exerting hip torque (lunging)
3. The ability to perform rapid steps is most important to remain capturable.
	1.  The instantaneous capture point moves on the line through the point foot and itself, away from the point foot, at a velocity proportional to its distance from the point foot.
4. Attempts to quantify human locomotion having more capturable states than legged robot locomotion
	1. Hypothesis that nearly all human legged locomotion takes place in a 3-step viable capture basin
	2. Hypothesis that all 3D bipedal robot locomotion demonstrated to date likely falls in a 2-step viable capture basin
	3. Above hypotheses are unargued

---

## Limitations 
1. Models are highly simplified
	1. Vertical displacement of COM ignored
	2. Internal forces of leg dynamics ignored
	3. Slippage of foot was ignored
	4. Double support phase was excluded
	5. Complex terrain was ignored
2. Chaotic dynamics may lead to uncomputable capturability


