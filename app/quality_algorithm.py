import json

quality_scores = []
requirements_unlocked = []

def init_algorithm(abilities,target):

    target_command,target_requirements = _set_target(abilities, target)

    _update_qualities(abilities,target_requirements)


def _set_target(abilities,target):

    target_command_dictionary_ = {
        0: 'json index command 1',
        1: 'json index command 2',
        2: 'json index command 3'
        # etc... revisar y definir
    }    

    target = target_command_dictionary_.get(target)
    target_requirements = abilities[target]

    return target, target_requirements


def _update_qualities(abilities,target_requirements):
    
    for i, ability in enumerate(abilities):
        req_ok = _check_req_ok(ability, requirements_unlocked)
        

def _check_req_ok(ability, requirements_unlocked):
    requirementes = ability['requiriments']
    if len(requirementes) == 0: 
        return 1
    else:
        for i in requirementes:
            if i not in(requirements_unlocked):
                return 0
    return 1