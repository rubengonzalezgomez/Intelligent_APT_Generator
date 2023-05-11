import json



# Creamos archivo JSON con las habilidades de la plataforma seleccionada
def filter_platform(platform):

    # Leer el archivo JSON y convertirlo a un diccionario Python
    with open('../data/abilities.json', 'r') as f:
        data = json.load(f)

    # Filtrar los objetos que contienen el valor del parámetro platform en el array 'executors'
    filtered_data = [i for i in data if any(j['platform'] == platform for j in i['executors'])]

    # Eliminar los valores en el array executors que no corresponden al valor del parámetro platform
    for element in filtered_data:
        element['executors'] = [i for i in element['executors'] if i['platform'] == 'linux']

    # Devolvemos el objeto JSON parseado
    return(parse_json(filtered_data,platform))


# Nuevo JSON parseado (solo con los atributos que nos interesan)
def parse_json(init_json, platform):

    final_json = []

    # Recorremos el objeto JSON y creamos el nuevo JSON
    for element in init_json:
        executor = element["executors"][0]
        parser = executor['parsers']
        
        requirements = []
        if len(element['requirements']) != 0:
            for i in element['requirements']:
                requirements.append(i["relationship_match"][0]["source"])

        unlocks = []
        if len(parser) != 0:
            for i in parser[0]["parserconfigs"]:
                unlocks.append(i["source"])
        
        new_obj = {
            "id":  element["ability_id"],
            "ability_name": element["name"],
            "description": element["description"],
            "tactic":  element["tactic"],
            "technique":  element["technique_name"],
            "platform": executor["platform"],
            "requirements":  requirements,
            "command":  executor["command"],
            "unlocks":  unlocks,
        }

        final_json.append(new_obj)
    
    # Escribimos en un fichero para que sea más fácil de visualizar y nos ayude en el desarrollo pero NO es necesario
    with open('../data/' + platform + '_abilities_parsed.json','w') as f:
        json.dump(final_json,f)

    return final_json

    
