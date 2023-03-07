# Hof 2007
**The ‘extrapolated center of mass’ concept suggests a simple control of balance in walking**

---

**Tags:** #locomotion #gait #biomechanics #control #COM #inverted_pendulum #extrapolatedCOM #dynamic_balance 

---

**Related:** [[N-Step Capturability - Koolen Et Al. 2012]]

---

## Key Definitions

**Extrapolated COM (XcoM):** Projected COM (onto groundplane) plus the COM velocity divided by a constant related to stature (x + v_x/w_o).

**w_0**: constant related to stature - equal to the (angular) eigenfrequency of a hanging, non- inverted, pendulum of length l and it has the dimension of time^-1

**x**: Projected COM location

**u_x:** COP location


---

## Key Takeaways
1. Balance is often studied by inspecting the COM, acted on by gravity, and the COP, acted on by the ground reaction force. But it has been shown that the relative position of the extrapolated COM, XcoM, and the COP can predict balance. With stable walking defined, the paper will show how XcoM can be used to define simple control strategies for stable walking.
2. The stable walking criteria used are:
	1. COP should not be beyond reach of foot placement
	2. Walker should be able to follow a well defined course (straight or curved)
	3. Forward speed should not fluctuate more than 20%
	4. Step length should not be greater than leg length
3. Two properties were derived that are necessary for control: 
	1. A stable XcoM trajectory is sufficient for a stable COM trajectory
	2. At any point the tangent to the trajectory of the XcoM runs through the COP
4. The above properties show that walking can be controlled by controlling the XcoM instead of the COM directly.
	1. With a constant COP within a step, the XcoM trajectory consists of a series of straight lines
	2. The goal of the control law is then to get the step duration and COP position for each step as a function of the XcoM position at time of foot contact. Doing this in a way that gives a stable XcoM trajectory will give a stable COM trajectory
5. This was simulated based on the derived equations with rounds of 50 steps, each starting from standstill with a left step (left steps are odd, right are even). In some cases a disturbance was added at step 20, either to the XcoM (push to the walker) or in the COP (remove available footholds). 
	1. In forward control without feedback, the gait was unstable because the distances between XcoM and COP increases exponentially
		1. Adding feedback on step timing results in a stable gait, but does not allow locomotion to start spontaneously from standstill and disturbances result in a persistent change of speed
		2. Adding simple feedback on control in addition to step time yields a completely stable gait. This allows for reactions to disturbances in both step time and step length, but still result in persistent speed changes
	2. In lateral control, a simple control law of keeping the left/right offsets in relation to the XcoM equal yields a stable gait. but after a disturbance, even though the path is still in the right direction, it is shifted to the side that was corrected towards.
		1. this can be corrected by adding proportional control, when the shift sideways is corrected in a few steps. Steps are now offset in relation to the "middle of the road."
	3. To start walking the COP is moved behind the XcoM, and to stop walking the COP should be placed at exactly the XcoM. 
	4. Turning is achieved by rotating the step offsets about an angle according to the turn.
6. The laws that are based solely on the inverted pendulum model and the definition of COM apply to anywhere the inverted pendulum model holds, and so are likely to apply to human movement since the IP model describes human balance well. However, the control laws based on offsets to achieve stable gaits are just useful control principles, and do not seem to describe human walking
---

## Limitations

1. The effects of foot rollover are neglected
	1. The model described may be a good approximation if average COP across the step time is taken
2. No double contact phase is considered, and foot placement is constant and changes instantaneously between steps
3. Humans don't appear to walk similarly to the control laws described by offsetting steps. Humans tend to take many quick, short steps when their movement is perturbed, rather than one long step while keeping step time constant.