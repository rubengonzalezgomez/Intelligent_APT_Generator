import tensorflow as tf
import numpy as np
import random
import matplotlib.pyplot as plt
import calculateReward
import NeuronalNetowork

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

    target = "be4801446e4452c2a3e53dbe57c7a365"

    def __init__(self, actions):
        self.actions = actions
        self.state = None
        self.calculator = calculateReward.calculateRewrd(self.actions)

    def set_initial_state(self):
        for elem in self.actions:
            if elem["id"] == self.target:
                initial_state = (elem["requirements"], 13)
        return initial_state

    def reset(self):
        self.state = self.set_initial_state()
        return self.state

    def calculate_next_state(self, action, current_state):
        pending_reqs = list(current_state[0])

        if len(action["unlocks"]) > 0:
            pending_reqs = self.remove_reqs(pending_reqs, action["unlocks"])

        new_reqs = action["requirements"]
        pending_reqs = pending_reqs + new_reqs
        new_tactic = action["tactic"]
        new_tactic = self.get_tactic_index(new_tactic)
        new_state = (pending_reqs, new_tactic)
        return new_state

    def remove_reqs(self, pending, unlocks):
        pending = [x for x in pending if x not in unlocks]
        return pending

    def get_tactic_index(self, tactic):
        for index in self.tactics:
            if self.tactics[index] == tactic:
                return index
        return

    def check_if_done(self, next_state):
        pending_reqs = list(next_state[0])
        if len(pending_reqs) == 0:
            return True
        else:
            return False

    def step(self, action, current_state):
        reward = self.calculator.calculate(action, current_state[1], current_state[0])
        next_state = self.calculate_next_state(action, current_state)
        done = self.check_if_done(next_state)
        return next_state, reward, done


class ReplayBuffer:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = []

    def add(self, experience):
        self.buffer.append(experience)
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(dones)


class Trainer:
    def __init__(self, num_episodes, max_steps, actions, replay_buffer_max_length):
        self.actions = actions
        self.num_actions = len(actions)
        self.num_episodes = num_episodes
        self.max_steps = max_steps
        self.replay_buffer_max_length = replay_buffer_max_length
    
    def get_action_position(self,id):
        position = None
        for i, objeto in enumerate(self.actions):
            if objeto["id"] == id:
                position = i
                break  # Terminar el bucle una vez que se haya encontrado la acción

        return position
    
    def compute_avg_return(self, environment, agent, num_episodes):
        total_return = 0.0

        for _ in range(num_episodes):
            state = environment.reset()
            episode_return = 0.0

            for _ in range(self.max_steps):
                action = agent.act(state)
                next_state, reward, done = environment.step(action, state)
                episode_return += reward
                state = next_state

                if done:
                    break

            total_return += episode_return

        avg_return = total_return / num_episodes
        return avg_return

    def train(self, evaluate_every, evaluate_episodes):
        env = CustomEnvironment(self.actions)
        agent = NeuronalNetowork.DQNAgent(self.actions, self.num_actions)
        replay_buffer = ReplayBuffer(self.replay_buffer_max_length)

        best_action_sequence = [env.target]
        max_reward = 0
        accumulate_reward = 0

        # Listas para la representación gráfica
        avg_returns = []
        episodes = []

        for episode in range(self.num_episodes):
            state = env.reset()
            action_sequence = [env.target]
            total_reward = 0

            for t in range(self.max_steps):
                repeat = True
                while repeat:
                    action = agent.act(state)
                    if action["id"] not in action_sequence:
                        repeat = False

                action_sequence.append(action["id"])
                next_state, reward, done = env.step(action, state)

                total_reward += reward # Recompensa total de las acciones tomadas

                action_position = self.get_action_position(action["id"])
                replay_buffer.add((state, action_position, reward, next_state, done))

                if len(replay_buffer.buffer) >= agent.batch_size:
                    batch = replay_buffer.sample(agent.batch_size)
                    agent.train(batch)

                state = next_state

                if done:
                    break
            
            accumulate_reward += total_reward # Recompensa acumulada de varias vueltas para calcular la media

            # Calculamos la media de las recompensas devueltas cada cierto tiempo para evaluar la calidad del modelo
            if (episode + 1) % evaluate_every == 0:
                    avg_return = accumulate_reward / evaluate_episodes
                    avg_returns.append(avg_return)
                    episodes.append(episode + 1)    
                    print(f"Average return after {episode+1} episodes: {avg_return}")
                    accumulate_reward = 0
                    
            if total_reward > max_reward:
                max_reward = total_reward
                best_action_sequence = action_sequence

        # Representar gráficamente los resultados
        plt.plot(episodes, avg_returns)
        plt.xlabel('Episodes')
        plt.ylabel('Average Return')
        plt.title('Average Return over Episodes')
        plt.show()


        print("Best action sequence:", best_action_sequence[::-1])
        print("Reward: ", max_reward)

        return best_action_sequence[::-1]