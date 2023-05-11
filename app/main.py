import sys

import api_requests
import parse_ability
import argparse

# Creamos el objeto ArgumentParser
parser = argparse.ArgumentParser(description='Creación de una APT inteligente para Mitre Caldera')

# Agregamos los argumentos que queremos recibir
parser.add_argument('-c', '--cookie', type=str, required=True, help='Valor de la cookie API_SESSION')
parser.add_argument('-p', '--platform', type=int, required=True, help='Plataforma sobre la que se va a desarrollar la APT. 0:Linux; 1:Windows; 2:Darwin')

# Parseamos los argumentos
args = parser.parse_args()

# Parseamos las habilidades de la plataforma seleccionada
def ability_parser(platform):

    if platform not in [0,1,2]:
        print("Error: Plataforma seleccionada no válida. Introduzca un valor válido. 0:Linux; 1:Windows; 2:Darwin ")
        exit()

    dictionary_platform = {
        0: 'linux',
        1: 'windows',
        2: 'darwin'
    }

    # Creamos JSON con las habilidades de la plataforma seleccionada
    platform = dictionary_platform.get(platform)
    print("Seleccionadas habilidades de " + platform + "\n")
    parse_ability.filter_platform(platform)



# INICIO EJECUCIÓN
print("\n\nBIENVENIDO A INTELLIGENT APT\n\n")

# Cargamos todas las habilidades de Caldera
api_requests.get_abilities(args.cookie)
print("Habilidades de Mitre Caldera cargadas\n")

# Parseamos las habilidades obtenidas dependiendo de la plataforma seleccionada
ability_parser(args.platform)

