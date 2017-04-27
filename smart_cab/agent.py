from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

from collections import defaultdict #for the q-Table
from itertools import product #for the q-Table
import random #for choosing an agent's action
import csv #debug


# initialize a Q-Table
qTable = defaultdict(int)

valid_lights = ['green','red']
valid_waypoints = [None, 'forward', 'left', 'right']
valid_actions = [None, 'forward', 'left', 'right']

all_states=[dict(zip(('light','waypoint','oncoming','left','right'), (i,j,k,l,m))) for i,j,k,l,m in product(valid_lights,valid_waypoints,valid_actions,valid_actions,valid_actions)]
for i in range(len(all_states)):
    for j in range(len(valid_actions)):
        qTable[str(all_states[i]),valid_actions[j]]

# global vars
epsilon = 0.50 #exploration rate
successes = 0 #counter for successful trial


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = {'light': self.env.sense(self)['light'], 'waypoint': self.planner.next_waypoint(), 'oncoming': self.env.sense(self)['oncoming'], 'left': self.env.sense(self)['left'], 'right': self.env.sense(self)['right']}
        previous_state = self.state
        
        # TODO: Select action according to your policy
        global epsilon 
        epsilon -= epsilon/250 #logarithmic exploration degradation

        q = [qTable[str(self.state), action] for action in self.env.valid_actions]
        max_q = max(q)
        r = random.random()
        
        if r < epsilon:
            action = random.choice(self.env.valid_actions)
        else:
            options = [i for i in range(len(self.env.valid_actions)) if q[i] == max_q]
            action = valid_actions[random.choice(options)]

        # Execute action and get reward
        reward = self.env.act(self, action)

        # Update state
        current_state = {'light': self.env.sense(self)['light'], 'waypoint': self.planner.next_waypoint(), 'oncoming': self.env.sense(self)['oncoming'], 'left': self.env.sense(self)['left'], 'right': self.env.sense(self)['right']}

        # TODO: Learn policy based on state, action, reward
        alpha = 0.50 #learning rate
        gamma = 0.001 #look ahead reinforcement rate
        qTable[str(previous_state), action] = ( (1-alpha) * qTable[str(previous_state), action]  ) + alpha * (reward + gamma * max( [qTable[str(current_state), ab] for ab in self.env.valid_actions] ) )

        #debug: print "previous state: deadline = {}, inputs = {}, action = {}, waypoint = {}, reward = {}".format(deadline, inputs, action, self.next_waypoint, reward)  # [debug]
        #debug: print "previous q ", qTable[str(previous_state), action]
        #debug: print "current q ", qTable[str(current_state), action]
        #debug: print "epsilon ", epsilon, r
        global successes #debug
        if deadline >= 0 and reward >= 8: #debug
            successes += 1 #debug
        
        print successes #debug



def run():
    """Run the agent for a finite number of trials."""


    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=.001)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit

    with open('test.csv', 'wb') as f:  # Just use 'w' mode in 3.x #debug
        w = csv.DictWriter(f, qTable.keys()) #debug: 
        w.writeheader() #debug: 
        w.writerow(qTable) #debug: 


if __name__ == '__main__':
    run()

