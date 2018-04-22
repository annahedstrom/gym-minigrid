#!/usr/bin/env python3

import sys
import numpy as np
import gym_minigrid
import gym
import time
from optparse import OptionParser
import ipdb
import random

import matplotlib.pyplot as plt

# -----------------------------
# ---MaxEnt Inverse RL agent---
# -----------------------------
class InverseAgentClass():
    
    def __init__(self, env, tau_num, tau_len):

        self.tau_num = tau_num; # number of trajectories
        self.tau_len = tau_len; # length of each trajectory
        self.gamma = 0.9; # discount factor
        self.alpha = 0.01; # learning rate
        
        self.gridSize = env.gridSize
        self.num_states = self.gridSize*self.gridSize # number of states
        self.num_actions = env.action_space.n # number of actions

        ## POLICY / value-FUNCTIONS
        #self.theta = np.round(np.random.rand(self.num_states,self.num_actions),2) # policy parameter theta # should we parametrize pi??
        self.pi = np.round(np.random.rand(self.num_states,self.num_actions),2)
        self.pi = (self.pi.T/np.sum(self.pi,1)).T
        self.value = np.zeros((self.num_states))

        ## REWARD
        self.psi = np.random.rand(self.num_states); # reward function parameter

    # store all trajectories data (states and actions seperately)
    def store_trajectories(self, TAU):
        self.TAU_S = TAU[0];
        self.TAU_A = TAU[1];
        print("self.TAU_S", self.TAU_S)


        # TODO. Open questions
        # How to reset and differ the environment a bit for what was trained and what is now the policy
        # e.g. q_expert.reset(env="Static") va maxent_learner.reset(env="Static") ?

        # TODO. Step 1. Sensoring
        # get the color type or other property of the expert trajectory states

        # TODO. Step 2. Check - can we trust it?
        # by coordiante check if the color type or other property is still correlated - is (1,0) from expert trajs still lava/ color = red?

        # TODO. Step 3. Trust threshold
        # by some Bayesian measure can we check similarity and therefore deciding
        # A. to follow policy
        # B. to divert from policy

        #self.type = type
        #self.color = color

    ## value-iteration
    ## perform value iteration with the current R(s;psi) and update pi(a|s;theta)
    def value_iteration(self,env):

        T_sas=0.01;

        while True:
            update_difference = -999;
            for s in range(self.num_states):
                old_value = self.value[s]
                self.value[s] = np.max([np.sum([ env.T_sas(s,a,s_prime)*(self.reward(s_prime)+self.gamma*self.value[s_prime]) for s_prime in range(self.num_states)]) for a in range(self.num_actions)])
                update_difference = max(update_difference, abs(old_value-self.value[s]))
            if(update_difference<0.01):
                break;

        print("Value iteration converged!: update_difference=", update_difference)
            
        #TODO: UPDATE POLICY FROM HERE!!

    ## get reward: r(s;psi)
    ## reward function is linear r(s;pi)= psi(i) phi(i)
    def reward(self,s):
        return self.psi[s];
                    
    # get policy: pi(a|s,theta)
    def policy(self,env,s,a):
        #return np.exp(self.theta[s,a])/ np.sum([np.exp(self.theta[s,b]) for b in range(self.num_actions)])
        return self.pi[s,a]

    ## compute P(s | TAU, T)
    ## find the state-visition frequency for the provided trajectories
    def get_state_visitation_frequency_under_TAU(self,env):

        # mu_tau[state, time] is the prob of visiting state s at time t FROM our trajectories         
        self.mu_tau = np.zeros([self.num_states])        
        
        for i in self.TAU_S:
            for j in i:
                self.mu_tau[int(j)] += 1

        return self.mu_tau/self.tau_num
    
    ## compute P(s | pi_theta, T)
    ## find the state-visitation frequency for all states
    def get_state_visitation_frequency(self,env):

        # mu[state, time] is the prob of visiting state s at time t
        mu = np.zeros([self.num_states, self.tau_len]) 

        for tau_t0 in self.TAU_S[0,:]: # look at t=0 for each trajectory
            mu[int(tau_t0),0] += 1 # initialize mu(.,t=0)
            
        mu[:,0] = mu[:,0]/self.tau_num

        for time in range(self.tau_len-1):
            for state in range(self.num_states):
                for action in range(self.num_actions):
                    for state_next in range(self.num_states):
                        #print("(state:",state,",action:",action,",state_p",state_next,")  mu(s):",mu[state,0]," pi(a|s):", self.policy(env,state,action), " T(s'|s,a):", env.T_sas(state,action,state_next))
                        mu[state_next, time+1] += mu[state, time] * self.policy(env,state,action) * env.T_sas(state,action,state_next)
                        
        return np.mean(mu, 1) # squeeze throughout time and return
    
    def update(self, env):

        # STEP:1
        # TODO: solve for optimal policy: do policy iteration on r(s;psi)
        self.value_iteration(env);
        ## pi = get_policy();

        # STEP:2
        mu_tau = self.get_state_visitation_frequency(env)        
        mu = self.get_state_visitation_frequency_under_TAU(env)

        # STEP:3
        grad = - (mu_tau - mu);
        print(grad.shape)        
        
        # STEP:4
        # update psi of r(s;psi)
        self.psi = self.psi + self.alpha*grad;

        # REPEAT
        
        print("updating..")    
