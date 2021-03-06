# -*- coding: utf-8 -*-
# Proximal Policy Optimization algorithm of acrobot example
# env: http://gym.openai.com/envs/Acrobot-v1/

import sys, os
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Algorithms.ppo_discrete_torch import PPO, Memory
import gym
import torch
import numpy as np


############## Hyperparameters ##############
env_name = "Acrobot-v1"
env = gym.make(env_name)
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n
n_latent_var = 64           # number of variables in hidden layer
update_timestep = 512       # update policy every n timesteps
lr = 3e-4
betas = (0.9, 0.999)
gamma = 0.99                # discount factor
K_epochs = 10                # update policy for K epochs
eps_clip = 0.2              # clip parameter for PPO
random_seed = None
#############################################

if random_seed:
    torch.manual_seed(random_seed)
    env.seed(random_seed)

memory = Memory()
ppo = PPO(state_dim, action_dim, n_latent_var, lr, betas, gamma, K_epochs, eps_clip)
ppo.policy_old.load_state_dict(torch.load('Weights\\Acrobot\\acrobot.pth', map_location='cpu'))

# logging variables
i_episode = 0
total_timestep = 0

# training loop
while True:
    i_episode += 1
    time_step = 0
    episode_reward = 0

    state = env.reset()

    while True:
        time_step += 1
        total_timestep += 1

        env.render()

        # Running policy_old:
        action = ppo.policy_old.act(state, memory)
        state, reward, done, _ = env.step(action)

        # Saving reward and is_terminal:
        memory.rewards.append(reward)
        memory.is_terminals.append(done)

        # update if its time
        if total_timestep % update_timestep == 0:
            ppo.update(memory)
            memory.clear_memory()
            total_timestep = 0

        episode_reward += reward

        if done:
            break

    print('i_episode: {0} \t time_step: {1} \t max_episode_steps: {2} \t episode_reward: {3}'.format(i_episode, time_step, env.spec.max_episode_steps, episode_reward))

    # saving
    # if i_episode % 500 == 0:
    #     torch.save(ppo.policy.state_dict(), 'Weights\\Acrobot\\acrobot.pth')