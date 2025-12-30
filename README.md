## Introduction
This project is in accordance with Johns Hopkins Introduction to Machine Learning course number 605.649. 

## Problem Statement
Given a track represented as a 2D array of strings, we were tasked with developing a reinforcement learning based racecar that would optimally traverse the track. 

The racecar has an ($x_t$, $y_t$) position correlating with the track coordinate, a ($v_{xt}$, $v_{yt}$) velocity vector bound by (±5, ±5) and an ($a_{xt}$, $a_{yt}$) acceleration vector. 

The agent can control the racecar only by altering the acceleration vector where each component can be either -1, 0, or 1. Hitting the wall allows resets the racecar to either the closest track position to the impacted wall or the starting line depending on whether a flag is set. 

## Methodologies
Three racecar controlling agents were implemented. A value iteration, Q learner and a SARSA based learner. We also had to test our racecar on the provided L, O, R and W race track text files provided. 

## Results
We determined that the value iteration algorithm resultedin the quickest race times during testing. Q learning based algorithm was sometimes quicker but the variability of this algorithm's runtime generally swayyed as slower than the value iteration algorithm. Finally the SARSA training model was the slowest. Additional results and analysis can be found in the report pdf. 