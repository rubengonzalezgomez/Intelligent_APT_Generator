import NeuronalNetowork as NN
import calculateReward

# Definir el entorno personalizado
class CustomEnvironment:

    tactics = {
        0: "reconnaissance",
        1: "initial-access",
        2: "execution",
        3: "multiple",
        4: "persistence",
        5: "privilege-escalation",
        6: "defense-evasion",
        7: "credential-access",
        8: "discovery",
        9: "lateral-movement",
        10: "collection",
        11: "command-and-control",
        12: "exfiltration",
        13: "impact"
    }

    # Definimos el estado inicial como una tupla con 0 requisitos desbloqueados y la táctica inicial
    initial_state = ([],0) 
    target = "ea713bc4-63f0-491c-9a6f-0b01d560b87e"
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

    def calculate_next_state(self,action,current_state):
        unlocked_reqs = list(current_state[0])
        new_reqs = action["unlocks"]
        unlocked_reqs = unlocked_reqs + new_reqs
        new_tactic = action["tactic"]
        new_tactic = self.get_tactic_index(new_tactic)
        new_state = (unlocked_reqs,new_tactic)
        return new_state
    
    def get_tactic_index(self,tactic):
        for index in self.tactics:
            if self.tactics[index] == tactic:
                return index
        return
    
    def check_if_done(self, next_state):
        unlocked_reqs = list(next_state[0]) # Requisitos desbloqueados
        if(len(unlocked_reqs)== 0):
            return False
        for unlock in unlocked_reqs:
            if unlock not in self.target_requirements:
                return False
        return True

    def step(self, action, current_state):
        # Tomar la acción en el entorno y obtener el siguiente estado, la recompensa y la señal de finalización
        next_state = self.calculate_next_state(action,current_state)
        unlocked_reqs = list(next_state[0])
        reward = self.calculator.calculate(action,unlocked_reqs, current_state[1],self.target_requirements)
        done = self.check_if_done(next_state)
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

        best_action_sequence = [] # Lista para almacenar la mejor secencia de acciones
        max_reward = 0 # Mayor recompensa de secuencia de acciones

        # Bucle principal de entrenamiento
        for episode in range(self.num_episodes):
            self.state = env.reset()  # Reiniciar el entorno para un nuevo episodio

            action_sequence = []  # Lista para almacenar las acciones tomadas en el episodio
            accumulate_reward = 0 # Recompensa acumulada

            for t in range(self.max_steps):
                # Evitar que se repitan acciones
                repeat = True
                while repeat:
                    action = agent.act(self.state)  # Elegir una acción
                    if action["id"] not in action_sequence:
                        repeat = False
                action_sequence.append(action["id"])  # Agregar la acción a la secuencia
                next_state, reward, done = env.step(action,self.state)  # Tomar la acción en el entorno
            
                accumulate_reward += reward

                agent.train(self.state, action, reward, next_state, done)  # Entrenar al agente

                self.state = (next_state[0], next_state[1])  # Actualizar el estado actual
                if done:
                    print("DONE")
                    break
            
            print(f"Episodio {episode+1}: Acciones tomadas {action_sequence}")
            print("Recompensa total: ", accumulate_reward)

            # Actualización mejor secuencia de acciones
            if accumulate_reward > max_reward:
                max_reward = accumulate_reward
                best_action_sequence = action_sequence

        print("Mejor secuencia de acciones:", best_action_sequence)
        print("Recompensa: ", max_reward)

        # Añadimos el comando objetivo
        best_action_sequence.append(env.target)
        return best_action_sequence