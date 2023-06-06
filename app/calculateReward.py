
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
                score += 50

        return score

    def get_tactic_index(self,tactic):
        
        for index in self.tactics:
            if self.tactics[index] == tactic:
                return index
        return
    
    def calculate(self,ability,pending_reqs):
        
        new_tactic = self.get_tactic_index(ability['tactic'])
        
        # Si el nombre de la táctica no se encuentra en la matriz de Mitre, la probabilidad de ese comando es 0
        if new_tactic is None:
            return 0
        
        reward = self.check_req_match(ability,pending_reqs)
        return reward