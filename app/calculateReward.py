import json


class calculateRewrd:

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
    
    def __init__(self,abilities) -> None:
        self.abilities = abilities # Lista de todas las habilidades
        self.abilitiesPerTactic = [0] * len(self.tactics) # Número de habilidades por táctica
        self.abilities_executed = []

    def check_ability(self,ability, unlocked_reqs):
        if ability["id"] in self.abilities_executed:
            return -1
        
        requirementes = ability['requirements']
        if requirementes: 
            for i in requirementes:
                if i not in(unlocked_reqs):
                    return -1
        return 1

    def check_req_match(self, ability, target_requirements):
        unlocks = ability['unlocks']
        score = 0

        for i in unlocks:
            if i in(target_requirements):
                score += 10
            else:
                score += 1
        return score

    def get_probability(self,last_tactic,next_tactic):
        weight =  (float)(next_tactic - last_tactic) # Posición de la nueva táctica con respecto la última
        # Si la táctica a evaluar es anterior a la última ejecutada la probabilidad será 0
        # En otro caso se aplica la fórmula P = 0.6 * 0.4(posición respecto la última táctica ejecutada)
        if(weight < 0):    
            probability = 0
        else:
            probability = 0.6 * (0.4 **(weight))        
        return probability

    def get_tactic_index(self,tactic):
        
        for index in self.tactics:
            if self.tactics[index] == tactic:
                return index
        return

    def count_abilities(self):

        for elem in self.abilities:
            tactic = elem['tactic']
            for i in self.tactics:
                if self.tactics[i] == tactic:
                    self.abilitiesPerTactic[i] += 1
    
    def calculate(self,ability,unlocked_reqs, last_tactic, target_requirements):
        req_ok = self.check_ability(ability, unlocked_reqs)
        unlocks_score = self.check_req_match(ability,target_requirements)  
        new_tactic = self.get_tactic_index(ability['tactic'])
        # Si el nombre de la táctica no se encuentra en la matriz de Mitre, la probabilidad de ese comando es 0
        if new_tactic is None:
            return 0
        prob_tactic = self.get_probability(last_tactic, new_tactic)
        self.count_abilities()
        self.abilities_executed.append(ability["id"])
        reward = (req_ok * (prob_tactic/self.abilitiesPerTactic[new_tactic])) + unlocks_score
        return reward