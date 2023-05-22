import random
import numpy as np
import tensorflow as tf
import calculateReward

# Definir la clase del modelo de Q-Learning profundo
class DQNModel(tf.keras.Model):
    def __init__(self, num_actions):
        super(DQNModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(24, activation='relu')
        self.dense2 = tf.keras.layers.Dense(24, activation='relu')
        self.dense3 = tf.keras.layers.Dense(num_actions)

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return self.dense3(x)

# Definir la clase del agente DQN
class DQNAgent:
    def __init__(self, abilities):
        self.actions = abilities
        self.num_actions = len(abilities)
        self.state_size = 8  # Tamaño del estado
        self.epsilon = 1.0  # Factor de exploración inicial
        self.epsilon_decay = 0.99  # Factor de decaimiento de la exploración
        self.epsilon_min = 0.01  # Límite mínimo de exploración
        self.gamma = 0.99  # Factor de descuento
        self.learning_rate = 0.001  # Tasa de aprendizaje

        # Construir el modelo principal y el modelo objetivo
        self.model = DQNModel(self.num_actions)
        self.target_model = DQNModel(self.num_actions)
        self.target_model.set_weights(self.model.get_weights())

        # Compilar el modelo
        self.model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))

    def act(self, state):
        # Tomar una acción basada en una política epsilon-greedy
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.num_actions)
        else:
            q_values = self.model.predict(state)
            return np.argmax(q_values[0])

    def train(self, state, action, reward, next_state, done):
        # Actualizar el modelo mediante el algoritmo de Q-Learning
        q_values = self.model.predict(state)
        q_values_next = self.target_model.predict(next_state)
        q_target = reward + self.gamma * np.amax(q_values_next[0])
        q_values[0][action] = q_target

        # Entrenar el modelo en un solo paso
        self.model.fit(state, q_values, verbose=0)

        # Actualizar la exploración epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Actualizar el modelo objetivo
        if done:
            self.target_model.set_weights(self.model.get_weights())