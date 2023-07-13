import os
import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['NBA']  # Reemplaza con el nombre de tu base de datos
collection = db['partidos']  # Reemplaza con el nombre de tu colección


temporadas = ["season20002001","season20012002","season20022003","season20032004",
              "season20042005","season20052006","season20062007","season20072008",
              "season20082009","season20092010","season20102011","season20112012",
              "season20122013","season20132014","season20142015","season20152016",
              "season20162017","season20172018","season20182019","season20192020",
              "season20202021","season20212022","season20222023"]

for temporada in temporadas:
        
    collectionTemporada = db[temporada] 

    # Ruta de la carpeta que contiene los archivos JSON
    carpeta_json = '/Users/formotion/tfg/python/DATA/JSON/'+temporada
    
    # Recorrer los archivos JSON en la carpeta
    for archivo in os.listdir(carpeta_json):
        if archivo.endswith('.json'):
            ruta_archivo = os.path.join(carpeta_json, archivo)
            print("Inseratndo:    "+ruta_archivo)
            with open(ruta_archivo) as archivo_json:
                contenido_json = json.load(archivo_json)
                
                collection.insert_one(contenido_json)
                collectionTemporada.insert_one(contenido_json)

# Cerrar la conexión a MongoDB
client.close()
