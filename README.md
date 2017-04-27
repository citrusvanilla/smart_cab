# Training a Smartcab How to Drive with Reinforcement Learning

This repository contains an implementation of Q-Learning in the training of a smartcab in a Markov decision process, and outlines the incremental steps taken to build an efficient AI program for the agent.  The environment in which the smartcab operates is built in the `pygame` library.  

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

The following tasks outline the implemenation of the final AI agent and codebase in this repository.

### Implementing a basic driving agent
We can first implement a driving agent by setting `action = random.choice(self.env.valid_actions)`.  This effectively turns our smartcab into the realization of a ‘random walk’ in two dimensions. Its actions are random and the previously-realized state/action pair has no bearing on the present state/action pair as the agent has no memory.

### Identifying and updating the state
We implement a "memory" in our AI agent by capturing its state/action pair and storing its reward to a table.  We do this by looking at all available inputs to the smartcab, and choose to represent the `light`, `waypoint`, and intersection traffic (`left`, `oncoming`, `right`) as the agent’s state, notably omitting the `deadline` environmental variable as its inclusion blows up our state space into a size in which learning cannot feasibly occur.  We identify state in `agent.py` with the following: 

> current_state = {'light': self.env.sense(self)['light'], 'waypoint': self.planner.next_waypoint(), 'oncoming': self.env.sense(self)['oncoming'], 'left': self.env.sense(self)['left'], 'right': self.env.sense(self)['right']}

### Implementing Q-Learning
We can implement learning based on memory by utilizing a Q-table.  We select a basic Q-learning equation, and update our agent's table based on state/action pairs.  Our choice of Q function is:
> ((1-alpha) * Q + alpha * (reward + (gamma * maxQ’)))

On initial trials, we choose a constant, non-degrading exploration value (epsilon = 0.25), a standard learning rate (alpha = 0.25), and a standard look- ahead value/rate (gamma = 0.25). In several trials of 100 runs each, we observed an average successful run (non-negative deadline upon the agent reaching the goal) rate of about 80% (that is, in 100 trials, the agent reaches the goal 80 times).

The Q-table is implemented in `agent.py` as:
> `qTable[str(previous_state), action] = ((1-alpha)*qTable[str(previous_state), action]) + alpha * (reward + gamma*max( [qTable[str(current_state), ab] for ab in self.env.valid_actions]))`

### Enhancing the driving agent
We optimize the agent's behavior by varying the paramaters of the Q-learning equation and comparing the effects.  To guard against a suboptimal policy being learned by the agent, we increase our learning rate (alpha = 0.50), and we increase the initial exploration value (epsilon = 0.50) so that more state/action states are visited at first.

We observe that our agent has learned an optimal policy early on in the trials, and thus we choose to degrade the exploration value very quickly (logarithmically), so that the agent is effectively executing the optimal action as determined by its q-value 90% of the time by the 10th trial, and 99% of the time by the 50th trial (ensured by choosing to reduce epsilon by 1/250th of its value at each step of the simulation). 

Finally, we observe that the discount factor (gamma) has no appreciable effect on the overall success rate of the simulation, so we are indifferent to its value (we set it to 0.001 in our final trial). With these adjustments made, we can increase our overall success rate for a 100-run simulation to >95%.

![alt text](http://i.imgur.com/gWYvjfU.jpg)



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
