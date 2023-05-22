import json


class calculateRewrd:

    target = 'x' # Identificador de la habilidad objetivo
    tactics = {
        0: "reconnaissance",
        1: "initial-access",
        2: "execution",
        3: "persistence",
        4: "privilege-escalation",
        5: "defense-evasion",
        6: "credential-access",
        7: "discovery",
        8: "lateral-movement",
        9: "collection",
        10: "command-and-control",
        11: "exfiltration",
        12: "impact"
    }
    
    def __init__(self,abilities) -> None:
        self.abilities = abilities # Lista de todas las habilidades
        self.requirements_unlocked = [] # Requisitos desbloqueados
        self.abilitiesPerTactic = [None] * len(self.tactics) # Número de habilidades por táctica
        self.target_requirements = self.abilities[self.target]['requirements'] # Requisitos objetivo


    def check_req_ok(self,ability, requirements_unlocked):
        
        requirementes = ability['requirements']
        if requirementes: 
            for i in requirementes:
                if i not in(requirements_unlocked):
                    return 0
        return 1

    def check_req_match(self,ability, target_requirements):
        requirementes = ability['requirements']
        cont_match = 0
        
        for i in requirementes:
            if i in(target_requirements):
                cont_match += 1

        return cont_match

    def get_probability(next_tactic):

        if apt:
            ability = abilities[apt[-1]]
            # El valor de la última táctica ejecutada
            last_tactic = get_tactic_index(ability['tactic']) 
        else:
            last_tactic = 0
        
        weight =  next_tactic - last_tactic # Posición de la nueva táctica con respecto la última

        # Si la táctica a evaluar es anterior a la última ejecutada la probabilidad será 0
        # En otro caso se aplica la fórmula P = 0.6 * 0.4(posición respecto la última táctica ejecutada)
        if(weight < 0):    
            probability = 0
        else:
            probability = 0.6 * 0.4^(weight)        

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
                if i == tactic:
                    self.abilitiesPerTactic[i] += 1
    
    def calculate(self,target_requirements,ability):
        req_ok = self.check_req_ok(ability, self.requirements_unlocked)
        req_match = self.check_req_match(ability,target_requirements)  
        tactic = self.get_tactic_index(ability['tactic'])
        prob_tactic = self.get_probability(tactic)
        reward = req_ok * (prob_tactic/self.abilitiesPerTactic[tactic] + req_match/len(target_requirements))
        return reward