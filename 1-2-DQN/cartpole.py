# -*- coding: utf-8 -*-
# Deep Q Network algorithm of cartpole example
# env: http://gym.openai.com/envs/CartPole-v1/

import gym
import random
import numpy as np
import tensorflow as tf
from collections import deque


class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.lr = 0.003
        # discount rate
        self.gamma = 0.95
        # exploration rate
        self.epsilon = 1.0  
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32
        self.buffer = deque(maxlen=1000)
        self.optimizer = tf.keras.optimizers.Adam(self.lr)
        self.model = self.build_model()

    def build_model(self):
        return tf.keras.Sequential([
            tf.keras.layers.Dense(24, activation="relu", input_shape=(None, self.state_size)),
            tf.keras.layers.Dense(24, activation="relu"),
            tf.keras.layers.Dense(self.action_size, activation='linear'),
        ])

    def choose_action(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon, self.epsilon_min)

        if np.random.random() < self.epsilon:
            action = random.randrange(self.action_size)
        else:
            action = np.argmax(self.model.predict(np.expand_dims(state, axis=0)))
        return action

    def memorize(self, state, action, reward, done, next_state):
        self.buffer.append((state, action, reward, done, next_state))
        return len(self.buffer) >= self.batch_size

    def train(self):
        sample_batch = random.sample(self.buffer, self.batch_size)
        for state, action, reward, done, next_state in sample_batch:
            with tf.GradientTape() as tape:
                target = reward if done else reward + self.gamma * self.model(np.expand_dims(next_state, axis=0)).numpy().max()
                y_true = self.model(np.expand_dims(state, axis=0)).numpy()
                y_true[0][action] = target
                loss = tf.keras.losses.mse(y_true,  self.model(np.expand_dims(state, axis=0)))
            gradient = tape.gradient(loss, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(gradient, self.model.trainable_variables))


i_episode = 0
env = gym.make("CartPole-v1")
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
agent = DQN(state_size, action_size)

while True:

    i_episode += 1
    step_time = 0

    state = env.reset()

    while True:
        step_time += 1
        env.render()

        action = agent.choose_action(state)

        next_state, reward, done, _ = env.step(action)

        if agent.memorize(state, action, reward, done, next_state):
            agent.train()

        state = next_state

        if done:
            break

    print("i_episode：{} \t step_time：{}".format(i_episode, step_time))
