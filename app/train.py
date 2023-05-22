import calculateReward

class trainer:

    def __init__(self,agent) -> None:
        self.agent = agent
        self.actions = self.agent.actions


    # Definir la función de recompensa
    def calculate_reward(self,action):
        calculator = calculateReward(self.actions)
        return calculator.update_qualities(action)

    def start_train(self):
        # Bucle principal de entrenamiento
        for episode in range(num_episodes):
            state = env.reset()  # Reiniciar el entorno para un nuevo episodio
            state = np.reshape(state, [1, self.agent.state_size])  # Ajustar la forma del estado para el modelo

            for t in range(max_steps):
                action_index = self.agent.act(state)  # Elegir un índice de acción
                action = self.agent.actions[action_index]  # Obtener la acción correspondiente al índice
                reward = calculate_reward(action)  # Calcular la recompensa para la acción

                next_state, done = env.step(action)  # Tomar la acción en el entorno
                next_state = np.reshape(next_state, [1, self.agent.state_size])  # Ajustar la forma del próximo estado

                self.agent.train(state, action_index, reward, next_state, done)  # Entrenar al self.agente

                state = next_state  # Actualizar el estado actual

                if done:
                    break