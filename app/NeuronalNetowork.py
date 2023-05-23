import tensorflow as tf
import numpy as np
import random
import json

# Definir la red neuronal para el modelo DQN
class DQNModel(tf.keras.Model):
    def __init__(self, num_actions):
        super(DQNModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(24, activation='relu')
        self.dense2 = tf.keras.layers.Dense(24, activation='relu')
        self.dense3 = tf.keras.layers.Dense(num_actions, activation='linear')

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return self.dense3(x)

# Definir el agente DQN
class DQNAgent:
    def __init__(self, actions):
        self.actions = actions
        self.num_actions = len(actions)
        self.state_size =  2 # Los estados son tuplas compuestas por una lista de requisitos desbloqueados y la última táctica ejecutada
        self.epsilon = 1.0
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
        self.model = DQNModel(self.num_actions)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

    def act(self, state):
        state = np.array(state).reshape(1, self.state_size)
        if np.random.rand() <= self.epsilon:
            return random.choice(self.actions)
        else:
            q_values = self.model.predict(state)
            action_index = np.argmax(q_values[0])
            return self.actions[action_index]

    def train(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + 0.99 * np.amax(self.model.predict(next_state)[0])
        target_f = self.model.predict(state)
        target_f[0][self.actions.index(action)] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

