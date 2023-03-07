# Darici Kuo 2022
**Humans plan for the near future to walk economically on uneven terrain**

---

**Tags:** #locomotion #gait #biomechanics #control #inverted_pendulum 

---

**Related:** 

---

## Key Definitions
**Curse of Dimensionality:** Exponentially increasing computational complexity of planning ahead an increasing number of steps.

**Persistence Distance:** The amount of steps it takes for one steps forward momentum to dissipate.

**Reactive Control:** Control strategy that attempts to minimize work without anticipating upcoming terrain. Instead, it merely compensates for disturbances as best it can after they happen. This is the *no planning* option. 
*Later this is referred to as Reactive Compensation (page 13).*

**Tight Regulation:** Control strategy that looks one step ahead and tries to restore the nominal speed for that step regardless of the energy expenditure required to do so. This is *maintain speed* option.

**Minimum Energy:** Control strategy that looks at the entire path ahead to plan a minimum energy expenditure path. This is the *minimize energy costs* option.

---

## Key Takeaways
1. Uneven ground interrupts the periodic and low energy expenditure nature of level ground walking. This makes control strategies difficult, especially as optimal control may depend on the total terrain shape that may be faced. It is unknown whether humans plan for uneven steps, and there could be different things to maximize for, like consistent speed or minimum energy expenditure.
2. Humans are known to look forward to plan a route, and adjust their momentum prior to a single uneven step like going up or down a curb. But with multiple uneven steps, the optimal strategy for one step depends on what occurs before or after, and calculating this across many steps has exponentially increasing computational complexity. This leaves two possibilities for control in uneven terrain:
	1. Some way of planning for optimal trajectories despite the computational complexity
	2. A suboptimal heuristic compensation
3. The existence of a **persistence distance**, a limited amount of steps which it takes for one step's forward momentum to dissipate, means it may not be necessary to plan for an infinite number of steps at once. The persistence distance may describe a horizon past which there is no need/advantage to plan.
4. The goal of the study is to test whether humans optimize compensations while crossing uneven terrain. The structure of the study is:
	1. Optimized a pendulum like walking model to predict speed fluctuation trajectories across different uneven terrain profiles.
	2. Considered whether a limited planning horizon could yield similar predictions.
	3. Performed human experiments to see if optimal compensations from the models predicted human behavior on similar terrain profiles.
5. Three alternative control strategies are compared:
	1. **Reactive Control:** Does not anticipate upcoming terrain, merely compensates for disturbances after they happen. Its goal is to minimize work.
	2. **Tight Regulation:** Looks one step ahead and tries to restore speed for that step regardless of energy expenditure.
	3. **Minimum Energy:** Minimizes overall energy expenditure by planning ahead for the full horizon. 
6. The minimum energy strategy uses the least work (followed by tight regulation and reactive control respectively), and is able to perform less work than the gravitational potential energy of the terrain profile. 
	- This seems in theory possible, if some of that work is done prior to reaching the pyramid (or, if we’re starting at a certain speed, we’re ignoring the work required to get to that speed). But it’s unintuitive, and could potentially be an indicator the model is doing something wrong.
	- The minimum energy model will be tested against human performance, with the expectation of predicting human speed fluctuations across the terrain, regardless of self-selected walking speed and step length. 
7. The minimum energy strategy was also investigated with finite horizons. Shorter horizons take more work, and are thus less optimal. But horizons around 7-8 steps begin to asymptotically approach the full horizon condition, thus showing there is little advantage to a full horizon in comparison to a sufficiently long finite horizon. 
8. Results:
	1. There was no significant difference in walking speed over different complexity terrains.
	2. The speed fluctuation pattern was significantly consistent for each terrain profile
	3. Humans showed both anticipatory and recovery compensations. The anticipatory compensations do not support the Reactive Control or Tight Regulation control theories, and the recovery compensation do not support Tight Regulation.
	4. Human speed fluctuations were significantly similar to model predictions. They were furthest from model predictions on the more complex terrain, and closer to model predictions on shorter and simpler terrain. 
	5. While human speed fluctuations generally correlated, there were specific steps across different terrains where the human behavior differed from predicted. The general agreement does not apply evenly across every step of every terrain.
	6. Finite planning horizon of about 8 steps is sufficient, and there was no evidence humans plan beyond about 8 steps.
9. Results may indicate humans are able to reason about the energetics, dynamics, and timing of their locomotion. This would mean human have an internal model of walking in their central nervous system that enables them to plan for locomotion economy. 
	1. This internal model is hypothesized to be an intermediate level of control. It is slower than low level feedback mediated at the spinal cord, and faster than high level conscious planning. 
---

## Limitations
1. Model correlations with human experiments are significant, but only moderately predictive. 
2. Human walking is noisy, in that there are differences across individuals
3. Larger terrain disturbances would better overcome the noise differences, but would make the dynamic pendulum model less applicable.
4. Uneven terrain in this case was discrete, flat steps, which is not as uneven or complex as real, outdoor uneven terrain.
5. Optimization hypothesis was tested with speed, but not metabolic energy or mechanical work. The test was too long to use force plates to measure ground reaction forces, but not long enough to get meaningful energetics measurements. 
6. The actual human experiments showed deviation from predictions consistent with humans breaking from inverted pendulum dynamics by deviating the placement of their COM. It is clear that humans eventually break fully from inverted pendulum dynamics with large enough terrain fluctuations that require use of our knees, and capturing these may require a more complex model than the simple linear inverted pendulum.
7. In general, humans have many more degrees of freedom than were modeled here, and it's not obvious how to extend optimization to all of these DOF.
8. The model predicted the best on shorter, simpler terrain, and worse on the longer and more complex terrains.