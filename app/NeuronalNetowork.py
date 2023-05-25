import tensorflow as tf
import numpy as np
import random
import json
from sklearn.preprocessing import OneHotEncoder

# Definir la red neuronal para el modelo DQN
class DQNModel(tf.keras.Model):
    def __init__(self, num_actions):
        super(DQNModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(24, activation='relu')
        self.dense2 = tf.keras.layers.Dense(24, activation='relu')
        self.dense3 = tf.keras.layers.Dense(num_actions, activation='linear')
        self.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')


    def call(self, inputs):
        x = self.dense1(x)
        x = self.dense2(x)
        return self.dense3(x)

# Definir el agente DQN
class DQNAgent:
    def __init__(self, actions):
        self.actions = actions
        self.num_actions = len(actions)
        self.state_dict = {}
        self.counter = 0
        self.state_size = 2  # Los estados son tuplas compuestas por una lista de requisitos desbloqueados y la última táctica ejecutada
        self.epsilon = 1.0
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
        self.model = DQNModel(self.num_actions)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)


    def get_state_id(self, state):
        requirements = tuple(state[0])  # Convertir la lista de requisitos en una tupla
        value = state[1]  # Valor numérico
        state_tuple = (requirements, value)
        
        if state_tuple in self.state_dict:
            return self.state_dict[state_tuple]
        else:
            state_id = self.counter
            self.state_dict[state_tuple] = state_id
            self.counter += 1
            return state_id

    def act(self, state):
        state_numeric = self.get_state_id(state)
        state_numeric = np.array(state_numeric)
        state_numeric = np.expand_dims(state_numeric, axis=0)
        state_tensor = tf.convert_to_tensor(state_numeric, dtype=tf.float32)
        
        if np.random.rand() <= self.epsilon:
            return random.choice(self.actions)
        else:
            q_values = self.model.predict(state_tensor)
            action_index = np.argmax(q_values[0])
            return self.actions[action_index]

    def train(self, state, action, reward, next_state, done):
        print(state,next_state,reward)
        state_numeric = self.get_state_id(state)
        next_state_numeric = self.get_state_id(next_state)

        state_numeric = np.array(state_numeric)
        next_state_numeric = np.array(next_state_numeric)

        state_numeric = np.expand_dims(state_numeric, axis=0)
        next_state_numeric = np.expand_dims(next_state_numeric, axis=0)

        state_tensor = tf.convert_to_tensor(state_numeric, dtype=tf.float32)
        next_state_tensor = tf.convert_to_tensor(next_state_numeric, dtype=tf.float32)

        state_tensor = tf.reshape(state_tensor, (1, -1))
        next_state_tensor = tf.reshape(next_state_tensor, (1, -1))

        target = reward
        if not done:
            target = reward + 0.99 * np.amax(self.model.predict(next_state_tensor)[0])
        target_f = self.model.predict(state_tensor)
        target_f[0][self.actions.index(action)] = target
        self.model.fit(state_tensor, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay