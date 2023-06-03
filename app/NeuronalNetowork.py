import tensorflow as tf
import numpy as np
import random

# Definir la red neuronal para el modelo DQN
class DQNModel(tf.keras.Model):
    def __init__(self, num_actions):
        super(DQNModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(24, activation='relu')
        self.dropout1 = tf.keras.layers.Dropout(0.2)  # Agregar capa de Dropout
        self.dense2 = tf.keras.layers.Dense(24, activation='relu')
        self.dropout2 = tf.keras.layers.Dropout(0.2)  # Agregar capa de Dropout con tasa de dropout 0.2
        self.dense3 = tf.keras.layers.Dense(num_actions, activation='linear')
        self.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='mse')

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return self.dense3(x)

# Definir el agente DQN
class DQNAgent:
    def __init__(self, actions, num_actions):
        self.actions = actions
        self.num_actions = num_actions
        self.state_dict = {}
        self.counter = 0
        self.state_size = 2
        self.epsilon = 3
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
        self.batch_size = 64
        self.model = DQNModel(self.num_actions)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

    def get_state_id(self, state):
        requirements = tuple(state[0])
        value = state[1]
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
        if np.random.rand() <= self.epsilon:
            action = random.choice(self.actions)
        else:
            state_tensor = tf.convert_to_tensor([state_numeric], dtype=tf.float32)
            state_tensor = tf.expand_dims(state_tensor, axis=0)  # Agregar una dimensión adicional
            q_values = self.model(state_tensor)
            action_index = tf.argmax(q_values[0]).numpy()
            action = self.actions[action_index]
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        return action

    def train(self, batch):
        states, actions, rewards, next_states, dones = batch
        states_numeric = [self.get_state_id(state) for state in states]
        next_states_numeric = [self.get_state_id(state) for state in next_states]

        states_tensor = tf.convert_to_tensor(states_numeric, dtype=tf.float32)
        states_tensor = tf.expand_dims(states_tensor, axis=1)  # Agregar una dimensión adicional

        next_states_tensor = tf.convert_to_tensor(next_states_numeric, dtype=tf.float32)
        next_states_tensor = tf.expand_dims(next_states_tensor, axis=1)  # Agregar una dimensión adicional
        
        with tf.GradientTape() as tape:
            q_values = self.model(states_tensor)
            target_q_values = self.model(next_states_tensor)
            target_q_values = rewards + (1 - dones) * tf.reduce_max(target_q_values, axis=1)
            mask = tf.one_hot(actions, self.num_actions)
            q_values_masked = tf.reduce_sum(tf.multiply(q_values, mask), axis=1)
            loss = tf.reduce_mean(tf.square(target_q_values - q_values_masked))

        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
