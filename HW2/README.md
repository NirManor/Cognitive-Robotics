COGROB HOMEWORK 2: The Dyson Swarm Adventure
Introduction
This repository contains the documentation and code for COGROB Homework 2, titled "The Dyson Swarm Adventure." The assignment revolves around designing and simulating a Dyson Swarm Adventure with the goal of capturing 90% of the sun's Irradiance by the year 2100. The primary objective is to maximize energy capture within the constraints of solar panel efficiency. The assignment entails gathering and analyzing engineering data from the web to formulate the physical properties of the challenge and make informed predictions about its future potential.

Preliminary Knowledge
It takes about 2,000kWh to create a 1,000-watt solar panel, corresponding to 1 solar panel on Earth.
NASA's MESSENGER spacecraft took approximately 6.5 years to complete its journey from launch to orbit insertion at Mercury.
The maximal theoretical efficacy of solar panels is 68.7%, and it is estimated to reach 30% in Mercury orbit.
Formulas and Equations
Satellite energy efficiency with respect to distance:


eeff(dorbit2sun) = e𝑠 / (dorbit2sun − 𝑑𝑚𝑒𝑟2𝑠𝑢𝑛) + 𝑒𝑠
The surface area required to capture the sun’s power output:


𝑆𝑜𝑟𝑏𝑖𝑡 = 0.9 ⋅ 4π(dorbit2sun)2
Energy that falls on each satellite with respect to the distance from the sun:


Isolar−panel(dorbit2sun) = Isolar / 4π(dorbit2sun)2
Total energy received from all satellites:


Etotal(dorbit2sun) = eeff(r) ⋅ Nsat ⋅ Ss ⋅ Isolar / 4π(dorbit2sun)2
Numerical Assumptions
The efficacy in Mercury orbit is estimated to be 30% based on the solar panel’s maximal theoretical efficacy.
Producing satellites on Mercury is assumed to be 20 times 'cheaper' in energy terms compared to Earth.
Future space travel is assumed to have shorter durations, with rocket velocities 10 times faster in 10 years.
Implementation
To achieve the goal, it is assumed that an autonomous crew deployed on Mercury and an initial number of energy-harvesting satellites in orbit will lead to stable actions and predictable exponential growth. PDDL is used to plan the initial mission stage, and once stability is reached, a Python script predicts growth and energy absorption.

Results and Conclusions
While challenges were encountered in solving the PDDL part, the Python script successfully approximates energy intake over time. Conclusions highlight the mission's complexity, the use of simplifications, and relaxed assumptions to construct a simple model. The chosen approach involves PDDL for the initial stage and a Python script for predicting growth and energy absorption post-stability.

This README provides an overview of the assignment, covering objectives, preliminary knowledge, formulas and equations, numerical assumptions, the implementation plan, and conclusions.






