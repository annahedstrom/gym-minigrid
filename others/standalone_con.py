#!/usr/bin/env python3

from __future__ import division, print_function

import gym
import numpy
import sys
import time
from optparse import OptionParser

import gym_minigrid
from others import expert_con as expert, inverse_agent_risk as inverse_agent


def main():
    
    basic_mode = True
    expert_mode = True
    inverse_mode = False
    
    parser = OptionParser()
    parser.add_option(
        "-e",
        "--env-name",
        dest="env_name",
        help="gym environment to load",
        default='MiniGrid-CaptureTheFlag-Static-v0',
        #default='MiniGrid-LockedRoom-v0',
    )
    (options, args) = parser.parse_args()

    # trajectory data parameters
    tau_num = 100; # number of trajectories
    tau_len = 20; # length of each trajectories
    
    # Load the gym environment
    env = gym.make(options.env_name)
    env.maxSteps = tau_len; # maximum time for an episode = length of our trajectory
        
    # Load expert agent / inverse learner
    q_expert = expert.ExpertClass(env,tau_num,tau_len)
    maxent_learner = inverse_agent.InverseAgentClass(env,tau_num,tau_len)        

    ## expert_mode: get expert trajectories

    renderer = env.render('human')
    min_runs = 100
    runs = 0

    for episode in range(1000):
        for t in range(tau_len):
            
            if(q_expert.update(env,episode,False)):
                q_expert.reset(env)
                break

            env.render('human')
            time.sleep(0.01)

        #if runs > min_runs and q_expert.test_convergence() == True:
         #   break

        runs += 1

            
    q_expert.reset(env)
        
    for episode in range(tau_num):
        for t in range(tau_len):
            if(q_expert.update(env,episode,True)):
                q_expert.reset(env)
                break
            
            env.render('human')
            time.sleep(0.01)

    ## get traj
    TAU = q_expert.get_tau();
    print(TAU)
    
    ## inverse RL mode: learn MaxEnt IRL from trajectories

    maxent_learner.store_trajectories(TAU);
    
    maxent_learner.update(env) 

if __name__ == "__main__":
    main()
