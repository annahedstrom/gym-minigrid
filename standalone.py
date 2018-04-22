#!/usr/bin/env python3

from __future__ import division, print_function

import sys
import numpy
import gym
import time
from optparse import OptionParser

import gym_minigrid
import expert
import inverse_agent

def main():
    
    basic_mode = True
    expert_mode = True
    inverse_mode = False
    risk_mode = True
    
    parser = OptionParser()
    parser.add_option(
        "-e",
        "--env-name",
        dest="env_name",
        help="gym environment to load",
        default='MiniGrid-CaptureTheFlag-Static-v0',
        #default='MiniGrid-CaptureTheFlag-Test-v0',
    )
    (options, args) = parser.parse_args()

    # trajectory data parameters
    tau_num = 100; # number of trajectories
    tau_len = 10; # length of each trajectories
    
    # Load the gym environment
    test_env_name = 'MiniGrid-CaptureTheFlag-Test-v0'
    env = gym.make(options.env_name)
    test_env = gym.make(test_env_name)

    env.maxSteps = tau_len; # maximum time for an episode = length of our trajectory

    # Load expert agent / inverse learner
    q_expert = expert.ExpertClass(env,tau_num,tau_len)

    maxent_learner = inverse_agent.InverseAgentClass(env, test_env, tau_num,tau_len, risk_mode)

    ## expert_mode: get expert trajectories

    #renderer = env.render('human')

    for episode in range(100):
        for t in range(tau_len):
            
            if(q_expert.update(env,episode,False)):
                q_expert.reset(env)
                break
            #env.render('human')
            #time.sleep(0.1)

        if(episode%10==0):
            print('Training expert episode:',episode)
                        
    q_expert.reset(env)
        
    for episode in range(tau_num):
        for t in range(tau_len):
            if(q_expert.update(env,episode,True)):
                q_expert.reset(env)
                break
            #env.render('human')
            #time.sleep(0.1)
            
        #print('Storing expert trajectory:',episode)
            
    ## get traj    
    TAU = q_expert.get_tau(PRINT=False);
    
    ## inverse RL mode: learn MaxEnt IRL from trajectories

    maxent_learner.store_trajectories(TAU);
    if risk_mode == True:
        maxent_learner.sensor_uncertainty(env)
        maxent_learner.env_check(env, test_env)

    maxent_learner.update(env,test_env, PRINT=True)

if __name__ == "__main__":
    main()
