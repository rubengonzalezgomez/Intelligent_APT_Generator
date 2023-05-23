import NeuronalNetowork as NN
import calculateReward

# Definir el entorno personalizado
class CustomEnvironment:
    # Definimos el estado inicial como una tupla con 0 requisitos desbloqueados y la táctica inicial
    initial_state = ([],"reconnaissance") 
    target = "ba0deadb-97ac-4a4c-aa81-21912fc90980"
    target_requirements = []

    def __init__(self, actions):
        self.actions = actions
        self.state = None
        self.calculator = calculateReward.calculateRewrd(self.actions)
        self.set_target()

    def set_target(self):
        for elem in self.actions:
            if elem["id"] == self.target:
                self.target_requirements = elem["requirements"]

    def reset(self):
        # Reiniciar el entorno y establecer el estado inicial
        self.state = self.initial_state
        return self.state

    def calculate_next_state(self,action):
        unlocked_reqs = list(self.state[0])
        new_reqs = action["unlocks"]
        unlocked_reqs = unlocked_reqs + new_reqs
        new_tactic = action["tactic"]
        new_state = (unlocked_reqs,new_tactic)
        return new_state
    
    def check_if_done(self, next_state):
        unlocked_reqs = list(next_state[0])
        for unlock in unlocked_reqs:
            if unlock not in unlocked_reqs:
                return False
        return True

    def step(self, action):
        # Tomar la acción en el entorno y obtener el siguiente estado, la recompensa y la señal de finalización
        next_state = self.calculate_next_state(action)
        unlocked_reqs = list(self.state[0])
        reward = self.calculator.calculate(action,unlocked_reqs, self.state[1],self.target_requirements)
        done = self.check_if_done(next_state)
        self.state = next_state
        return next_state, reward, done


class trainer:
    # Definir los parámetros
    def __init__(self, num_episodes, max_steps, actions):
        self.actions = actions
        self.state = None
        self.num_episodes = num_episodes
        self.max_steps = max_steps

    def train(self):
        # Crear el entorno y el agente
        env = CustomEnvironment(self.actions)
        agent = NN.DQNAgent(self.actions)

        # Bucle principal de entrenamiento
        for episode in range(self.num_episodes):
            state = env.reset()  # Reiniciar el entorno para un nuevo episodio

            action_sequence = []  # Lista para almacenar las acciones tomadas en el episodio

            for t in range(self.max_steps):
                action = agent.act(state)  # Elegir una acción
                action_sequence.append(action)  # Agregar la acción a la secuencia

                next_state, reward, done = env.step(action)  # Tomar la acción en el entorno

                agent.train(state, action, reward, next_state, done)  # Entrenar al agente

                state = next_state  # Actualizar el estado actual

                if done:
                    break

            print(f"Episodio {episode+1}: Acciones tomadas {action_sequence}")

        # Obtener la secuencia de acciones del mejor episodio
        best_action_sequence = action_sequence

        print("Mejor secuencia de acciones:", best_action_sequence)