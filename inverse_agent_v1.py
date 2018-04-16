#!/usr/bin/env python3

import sys
import numpy as np
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
    
    def __init__(self, env):

        self.tau_num = 10; # number of trajectories
        self.tau_len = 15; # length of each trajectory
        
        self.gridSize = env.gridSize
        self.num_states = self.gridSize*self.gridSize # number of states
        self.num_actions = env.action_space.n # number of actions
        self.T_sas = np.zeros((self.num_states, self.num_actions, self.num_states))
        # Construct transition matrix
        '''
        # Preconstruct the transition probability array.
        self.T_sas = np.array(
            [[[self._T_sas(i, j, k)
               for k in range(self.num_states)]
              for j in range(self.num_actions)]
             for i in range(self.num_states)])
        '''

        #self.TAU;# = TAU; #np.random.randint(0,4,size=(self.tau_num, self.tau_len)) # matrix with all trajectories

        self.theta = np.random

    def store_trajectories(self, TAU):
        self.TAU_S = TAU[0];
        self.TAU_A = TAU[1];

        for tau_idx in range(self.tau_num):
            for t in range(self.tau_len):
                print("(",self.TAU_S[tau_idx][t],",",self.TAU_A[tau_idx][t],")->",end='')
            print('\n')
        
    def policy(self,env,s):        
        return env.action_space.sample()
        
    # compute P(s | pi_theta, T) 
    def get_state_visitation_frequency(self, env):

        # mu[state, time] is the prob of visiting state s at time t
        mu = np.zeros([self.num_states, self.tau_len]) 

        for tau_i in self.TAU_S:
            mu[int(tau_i[0]),0] += 1
        mu[:,0] = mu[:,0]/self.tau_len

        #print("TAU_S[t=0]",self.TAU_S[:,0])
        #print("MU:",mu)
            
        for time in range(self.tau_len-1):
            for state in range(self.num_states):
                for state_previous in range(self.num_states):

                    # assuming (for now) that T(s,a,s') is equiprobable if states are nearby
                    T_sas = 1.0; #1.0/self.num_actions if abs(state-state_previous) <1 else 0
                    self.T_sas = 1.0;
                
                    #mu[state, time+1] += mu[state_previous, time] * T_sas * self.policy(env,state)

        p = np.sum(mu, 1)
        #print(mu)
        return p
        
    def update(self,env):
        
        print("Done!")

    def expert_get_state_visitation_frequency(self):
        p = np.zeros(self.num_states)
        for tau_i in self.TAU_S:
            for step in range(self.tau_num):
                p[int(tau_i[0])] += 1
        p = p / self.tau_len
        return p

    def get_transition_probs(self):
        # look at tryMove in capture the flag
        # is trans prob dependent on environment or uniformly distributed

        for i in range(self.num_states):
            for i in range(self.num_states_prime):
                if action = up and we want to go up
                then trans prob == 1
        pass

  for si in range(N_STATES):
    statei = gw.idx2pos(si)
    for a in range(N_ACTIONS):
      probs = gw.get_transition_states_and_probs(statei, a)
      for statej, prob in probs:
        sj = gw.pos2idx(statej)
        # Prob of si to sj given action a
        P_a[si, sj, a] = prob
