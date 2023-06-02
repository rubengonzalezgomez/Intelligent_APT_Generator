
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


    def check_req_match(self, ability, pending_reqs):
        unlocks = ability['unlocks']
        score = 0

        for i in unlocks:
            if i in(pending_reqs):
                score += 10
            else:
                score += 5
        return score

    def get_probability(self,last_tactic,next_tactic):
        weight =  (float)(abs(last_tactic - next_tactic)) # Posición de la nueva táctica con respecto la última
        
        # Cuanto más cerca esté de la última táctica mayor puntuación
        probability = 0.5 * (0.5 **(weight))
        # Devolvemos el valor multiplicado por 10 para darle mayor importancia a la hora de calcular la reward
        return 10*probability   

    def get_tactic_index(self,tactic):
        
        for index in self.tactics:
            if self.tactics[index] == tactic:
                return index
        return
    
    def calculate(self,ability, last_tactic, pending_reqs):

        unlocks_score = self.check_req_match(ability,pending_reqs)  
        new_tactic = self.get_tactic_index(ability['tactic'])
        # Si el nombre de la táctica no se encuentra en la matriz de Mitre, la probabilidad de ese comando es 0
        if new_tactic is None:
            return 0
        prob_tactic = self.get_probability(last_tactic, new_tactic)

        reward = prob_tactic * unlocks_score
        return reward