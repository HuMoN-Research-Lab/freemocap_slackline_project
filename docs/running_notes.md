# FreeMoCap Slackline Project

[![hackmd-github-sync-badge](https://hackmd.io/Asg3k1u2Sm6Bkgxb0uUdAw/badge)](https://hackmd.io/Asg3k1u2Sm6Bkgxb0uUdAw)


## 2022-08-15
 pq wrote -

> Playing around with an "optical flow" style visualization. The goal is to get an animation that really shows the "rotational about the COM" nature of slackline balance. Currently using traces made from scatter plots, but feeling like there could be a better visual from a disappearing line (just not sure how to create that). I also think it would be cool to make this without the skeleton, and maybe also tracking with the COM, so you just see the rotation.

> From an analysis perspective, trying to isolate the rotation like this shows the rotation, which is cool, but it also makes it obvious the COM is moving quite a bit, i.e. the balance isn't just coming from torque about the COM - there's additional effects from the line moving




- Talking about what philip calls the 'optical flow' version of the skeleton
    - Not technically optical flow: optic flow is detection of visual motion in an image
    - Inspired by cv2 tutorial on optical flow - wanted similar look, but using already tracked points instead of optical flow motion detection
    - Call it traces instead
    - Will clean up trace methodology later - using numpy indexing instead of maintaining a list
    - Draw line between dots instead of scatter plots
    - Put in Full body COM - it's different than torso segment com - add it with new color and different symbol
    - Analysis will start with point mass model of slacklining
        - linear inverted pendulum
        - linear momentum
        - f = ma
    - deal with rotation, momentum, torques later - linear and angular momentums are separate things
        - Angular aspects of COM- 
            - "reduced mass pendulum"
                - https://techtv.mit.edu/videos/b62e2f98e776486a891fa9decb312779/
                - https://www.researchgate.net/publication/224705816_Reaction_Mass_Pendulum_RMP_An_explicit_model_for_centroidal_angular_momentum_of_humanoid_robots

 - Research question
     - Beautiful machine type project: "look at this beautiful machine and (grounded in theory) describe how it works"
     - A theoretically grounded mechanical description of the stategy used to maintain balance. By describing outside mechanics, get some glimpse at the inside
     - An alternative to hypothesis testing type approach
     - Building towards acrobot, start with simple cart and pendulum and PD/PID controller
     - ** Experimental task**
         - level 0 - stand on slackline with one foot attempting to maintian 'perfec' stillness
             - i.e. maintain 'static equilibrium'
                 - with impossible goal that COM is direclty above BOS (i.e. COM_vertical_projection - BOX_vertical_projection = 0, so COM_dot_dot = 0)
         - level A - stand on slackine on one foot, while wiggle wiggling
             - i.e. maintain 'dynamic equilibrium'
                 - that is, you're BOS-COM is not zero, but it sums to zero
                 - practically speaking - you don't fall over within "X amount of time"
         - level 1 - Walking on the slackline
             - ie. another form of 'dynamic equilibrium' 

    - characterize COM vs. BOS across those three levels - start with newtonian mechanics before pd controller - where does energy go while moving (i.e. when we calm everything down)?
    - eventually, we will also look at learning too - how does it differ with skill level
    - Three forces in a simulated physical model: COM position, BOS position, Spring restoring force (unstable, chaotic system)
    - First make a simulated model (modified cart and pendulum), then make a controller for it. Then can you take starting points from physical data and then balance from there
    - start by making ballistic simulation in python

study 0 is make a simulated model of balance on 1 foot on a slackline ()

physical modelling - 
    - from intial conditions (position and velocity)
    - calculate acceleration on each frame 
        - acc - delta vel
    - if you X(position), delta X (velocity), Delta Delta X(aka delta vel, akaacceleration, )
        - then if you know the intial conditions, you can predict those conditions on the next frame and then you can know where THING will be in the future
        - people use "ODE" solvers for that (google things like '`ode45`')

 - model a cannon ball (projectile motion)
 - model a simple pendulum

**Resources for physical modelling in python**
 - https://physics.weber.edu/schroeder/scicomp/PythonManual.pdf