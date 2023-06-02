import datetime
import requests
import json
import uuid

class comunicator:
    
    # Consulta a la API de Caldera con el path especificado
    def send_request(self,cookie, path, protocol,data):

        # Crear una sesión
        session = requests.session()
        
        # Definimos y llamamos a la URL de la API
        api_url = 'http://localhost:8888/api/v2/' + path

        if protocol == 0:
            # Definir cabeceras
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'Cookie' : "API_SESSION="+cookie
                }
            response = session.get(api_url, headers=headers)
        elif protocol == 1:
            # Definir cabeceras
            headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie' : "API_SESSION="+cookie
            }
            json_data = json.dumps(data)  # Codificar los datos como JSON
            response = session.post(api_url, headers=headers,data=json_data)

        # Comprobamos el estado de la respuesta y la devolvemos en caso de ser correcta
        status = response.status_code
        if status != 200:
            print(response.status_code)
            print(response.reason)
            print(response._content)
            print("ERROR. PETICIÓN NO VALIDA.")
            return None

        # Devolvemos el objeto respuesta
        return response


    # Obtenemos todas las habilidades almacenadas en Mitre Caldera
    def get_abilities(self,cookie):

        # Ejecutar petición y transformar a JSON
        response = self.send_request(cookie,'abilities',0,None)
        if response is None:
            return False
        else:
            response = response.json()
            # Guardamos la salida en un fichero JSON
            with open('../data/abilities.json', 'w') as archivo:
                json.dump(response,archivo)
            return True
    

    def create_adversary(self,cookie,action_sequence):
        # Generamos un id aleatorio para el adversario
        adversary_id = str(uuid.uuid4())

        data = {
            "description": "Adversay created by a neuronal network",
            "atomic_ordering": action_sequence,
            "adversary_id": adversary_id,
            "name": "Intelligent APT",
            "plugin": "stockpile",
            "objective": "495a9828-cab1-44dd-a0ca-66e58177d8cc",
            "tags": []
        }

        self.send_request(cookie,'adversaries',1,data)
        return adversary_id

    def create_operation(self,cookie,action_sequence):
        adversary = self.create_adversary(cookie,action_sequence)
        operation_id = str(uuid.uuid4())
        
        data = {
                "source": {
                    "id": "ed32b9c3-9593-4c33-b0db-e2007315096b",
                },
                "name": "Intelligent APT Operation",
                "id": operation_id,
                "obfuscator":"plain-text",
                "visibility":"51",
                "planner": {
                    "id": "aaa7c857-37a0-4c4a-85f7-4e9f7f30e31a",
                },
                "adversary": {
                    "adversary_id": adversary
                }
            }
        
        self.send_request(cookie,"operations",1,data)