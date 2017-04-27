# Training a Smartcab How to Drive

This repository contains an implementation of Q-Learning in the training of a driving agent as a Markov decision process.  The environment in which the smartcab operates is built in the pygame library.  

## The Game
The static environment is build in pygame with `smart_cab/environment.py`.  The Python file `smart_cab/simulator.py` "runs" the game and makes the environment dynamic.  

### Environment
The environment is a small, idealized grid-like city, with roads going North-South and East-West. Other vehicles may be present on the roads, but no pedestrians. There is a traffic light at each intersection that can be in one of two states: North-South open or East-West open:

![alt text](http://i.imgur.com/a8svi88.jpg)

US right-of-way rules apply: On a green light, you can turn left only if there is no oncoming traffic at the intersection coming straight. On a red light, you can turn right if there is no oncoming traffic turning left or traffic from the left going straight.

### Inputs to the Smartcab
`smart_cab/planner.py` assigns a route to the smartcab, assigning it waypoints at each intersection. In this world, time is quantized- at any instant, the smartcab is at some intersection. The next waypoint is therefore always either one block straight ahead, one block left, one block right, one block back or exactly there (the cab has reached the destination).

The smartcab only has an egocentric view of the intersection it is currently at. It is able to sense whether the traffic light is green for its direction of movement (heading), and whether there is another car at the intersection on each of the incoming roadways (and which direction they are trying to go).

In addition to this, each trip has an associated timer that counts down every time step. If the timer is at 0 and the destination has not been reached, the trip is over, and a new one may start.

### Outputs of the Smartcab
At any instant, the smartcab can either stay put at the current intersection, move one block forward, one block left, or one block right (no backward movement).

### Rewards
The smartcab receives a reward for each successfully completed trip. A trip is considered “successfully completed” if the cab arrives at the desired destination (some intersection) within a pre-specified time bound.

The cab also receives a small reward for each correct move executed at an intersection. It receives a small penalty for an incorrect move, and a large penalty for violating traffic rules and/or causing an accident.

### Goal
The goal is to design the AI driving agent for the smartcab.  The cab receives the above-mentioned inputs at each time step t, and generates an output move. Based on the rewards and penalties it gets, the agent should learn an optimal policy for driving on city roads, obeying traffic rules correctly, and trying to reach the destination within a goal time.

## Tasks
- Implement a basic driving agent
- Identify and update state
- Implement Q-Learning
- Enhance the driving agent


## Software and Library Requirements
* Python 2.7.11
* Jupyter Notebook 4.2.2
* Numpy 1.11.2
* scikit-image 0.12.3
* matplotlib 1.5.2
* [pygame library](https://www.pygame.org/wiki/GettingStarted)


## Code Organization

File | Purpose
------------ | -------------
smart_cab/agent.py | Runs 'main()' and defines the learning behavior of the smartcab.
smart_cab/environment.py | Builds the static environment within which all agents operate.
smart_cab/planner.py | Route planner for all driving agents.
smart_cab/simulator.py | PyGame-based simulator to run the dynamic environment.
images/ | PNG graphics for all driving agents.


## Getting up and running

Make sure you are in the top-level project directory `smart_cab/`. Then run:

> python smart_cab/agent.py
