import api_comunicator as api
import parser_ability
import argparse

import trainer

# Creamos el objeto ArgumentParser
parser = argparse.ArgumentParser(description='Creación de una APT inteligente para Mitre Caldera')

# Agregamos los argumentos que queremos recibir
parser.add_argument('-c', '--cookie', type=str, required=True, help='Valor de la cookie API_SESSION')
parser.add_argument('-p', '--platform', type=int, choices=range(0, 3), required=True, help='Plataforma sobre la que se va a dValor de la cookie API_SESSIONesarrollar la APT. 0:Linux; 1:Windows; 2:Darwin')
parser.add_argument('-ne', '--num_epochs', type=int, default=1000, help='Número de epochs durante las que se queire entrenar al modelo. Recomendable que el valor este entre 500 y 2000, dependiendo de la complejidad del problema')
parser.add_argument('-e', '--evaluate', type=int, default=50, help='Cada cuántas epochs se debe evaluar el modelo')
parser.add_argument('-t', '--target', type=int, choices=range(0, 3),required = True, help='Perfil del atacante. 0:Crypto mining; 1:Disrupt Wi-Fi; 2:Exfiltrate and encrypt files')

# Parseamos los argumentos
args = parser.parse_args()

# Parseamos las habilidades de la plataforma seleccionada
def platform_translator(platform):

    dictionary_platform = {
        0: 'linux',
        1: 'windows',
        2: 'darwin'
    }

    # Creamos JSON con las habilidades de la plataforma seleccionada
    platform = dictionary_platform.get(platform)
    print("Seleccionadas habilidades de " + platform + "\n")
    return platform


# INICIO EJECUCIÓN
print("\n\nBIENVENIDO A INTELLIGENT APT\n\n")

# Cargamos todas las habilidades de Caldera
api = api.comunicator()
if(api.get_abilities(args.cookie)):
    print("Habilidades de Mitre Caldera cargadas\n")

    # Parseamos las habilidades obtenidas dependiendo de la plataforma seleccionada
    platform = platform_translator(args.platform)
    parser = parser_ability.parser()
    abilities = parser.filter_platform(platform)

    # Dependiendo del perfil del ataque se necesitará un conjunto de hiperparámetros
    target = args.target
    if target == 0:
        steps = 4
    elif target == 1:
        steps = 7
    elif target == 2:
        steps = 10

    # Instanciamos el objeto que crea y entrena a la red neuronal
    trainer = trainer.Trainer(args.num_epochs,steps,abilities,500000,target) 
    action_sequence,attack = trainer.train(args.evaluate)
    # Creamos la operación en CALDERA
    api.create_operation(args.cookie,action_sequence,attack)
    print("APT INICIADA")
