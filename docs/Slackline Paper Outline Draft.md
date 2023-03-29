# Slackline Outline Draft

## Introduction

A comprehensive literature review can be found at: [slackline lit review](https://humon-research-lab.github.io/freemocap_slackline_project/lit_review_notes/Slackline%20Literature%20Survey/). The relevant sections are 'Slackline Control Theory', 'Slacklining Balance Strategies', and 'Slacklining Performance Indicators and Measures of Stability'.

## Results 

https://user-images.githubusercontent.com/24758117/228618561-11e0ed58-4a15-4393-ac8b-4063404f5764.mp4
- Screenshot from left foot standing session showing 2d motion capture overlay, 3d motion capture animation, distance of center of mass from base of support in the mediolateral direction, and the state space (distance vs. velocity) of the mediolateral distance between the center of mass and base of support.

![Left foot standing time series](https://i.imgur.com/dXkyLmF.png)
- Time series of four sessions of left foot standing, each showing the mediolateral distance between the center of mass and base of support.

![Left foot standing state space](https://i.imgur.com/UNHYSVN.png)
- The state space (distance vs. veclocity) of the mediolateral distance between the center of mass and base of support for 12 seconds of left foot standing

https://user-images.githubusercontent.com/24758117/228621799-c3abc50d-1990-457d-8d54-f4847e04958e.mp4
- Overlay of the virtual pendulum from the base of support to the center of mass, displayed over animation of motion capture data.

![Hand Coordination Mediolateral](https://i.imgur.com/SO7zEGd.png)
- Right vs left hand motions in the mediolateral direction. Investigating the claim from [[Performance indicators for stability of slackline balancing]] that hand coordination is an indicator of slackline expertise.

![Hand Coordination Vertical](https://i.imgur.com/XwvD6wq.png)
- Right vs left hand motions in the vertical direction. Investigating the claim from [[Performance indicators for stability of slackline balancing]] that hand coordination is an indicator of slackline expertise.

![Foot motion patterns in mediolateral plane](https://i.imgur.com/r7K8XBF.png)
- Foot motion patterns on the mediolateral plane, investigating the modeling from [[Balancing on tightropes and slacklines - Paoletti Mahadevan 2012]] and [[An LMI Approach to Controller Design for Balancing over Slackline - Iqbal 2019]] that model the "slackliners" foot as traveling along a circular track rather than on a springed horizontal track.


## Materials and Methods

### Slackline Protocol

We recorded motion capture of X skilled slackliners performing the same balance protocol while standing on a slackline. The balance protocol involved X seconds of single leg standing on the right foot, X seconds of single leg standeng on the right foot, and X seconds of tandem stance standing with the subject's preferred foot forward. The slackline used was X meters long, had Y kN of tension on it, and the webbing was a flat weave made of polyester. 

### Motion Capture

We recorded the motion capture using Freemocap's markerless motion capture software, with 2D pose estimation performed by Google's Mediapipe Holistic model. We used four GoPro Hero 7 Black cameras to record the video in 2.7K at a framerate of 60Hz. The recordings were made outside with the subjects wearing normal street clothes. 
