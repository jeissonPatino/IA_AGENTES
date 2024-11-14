import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/mejor_ruta', methods=['POST'])
def obtener_mejor_ruta():
    data = request.get_json()
    origen = data.get('origen')
    destino = data.get('destino')
    tipo_vehiculo = data.get('tipo_vehiculo')

    
    respuesta_ruta = requests.get(f'http://localhost:5000/ruta?origen={origen}&destino={destino}')
    rutas = respuesta_ruta.json()

    
    if rutas:
        primera_ruta = rutas[0]  
        latitud = ...  
        longitud = ...
        respuesta_clima = requests.get(f'http://localhost:5002/clima?latitud={latitud}&longitud={longitud}')
        clima = respuesta_clima.json()

        
        respuesta_vehiculo = requests.get(f'http://localhost:5001/vehiculo?tipo={tipo_vehiculo}&clima={clima["descripcion"]}')
        compatibilidad = respuesta_vehiculo.json()['compatibilidad']

        if compatibilidad:
          
            mejor_ruta = primera_ruta 
            return jsonify(mejor_ruta)
        else:
            return jsonify({'mensaje': 'El tipo de vehículo no es compatible con la ruta debido al clima.'})
    else:
        return jsonify({'mensaje': 'No se encontraron rutas.'})

if __name__ == '__main__':
    app.run(debug=True, port=5003)