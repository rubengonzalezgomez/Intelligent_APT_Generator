import sys
import requests
import json

class comunicator:
    
    # Consulta a la API de Caldera con el path especificado
    def send_request(self,cookie, path):

        # Crear una sesión
        session = requests.session()

        # Definir cabeceras
        headers = {
            'Host': 'localhost:8888',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://localhost:8888',
            'Accept': 'application/json',
            'Cookie' : "API_SESSION="+cookie
            }
        
        # Definimos y llamamos a la URL de la API
        api_url = 'http://localhost:8888/api/v2/' + path

        response = session.get(api_url, headers=headers)

        # Comprobamos el estado de la respuesta y la devolvemos en caso de ser correcta
        status = response.status_code
        if status != 200:
            print("ERROR. PETICIÓN NO VALIDA.")
            return

        # Devolvemos el objeto respuesta
        return response


    # Obtenemos todas las habilidades almacenadas en Mitre Caldera
    def get_abilities(self,cookie):

        # Ejecutar petición y transformar a JSON
        response = self.send_request(cookie,'abilities')

        if response is not None:
            response = response.json()

            # Guardamos la salida en un fichero JSON
            with open('../data/abilities.json', 'w') as archivo:
                json.dump(response,archivo)


    

