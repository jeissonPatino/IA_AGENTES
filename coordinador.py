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

    
    try:
        respuesta_ruta = requests.get(f'http://localhost:5000/ruta?origen={origen}&destino={destino}')
        respuesta_ruta.raise_for_status() 
        rutas = respuesta_ruta.json()
        print(rutas)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener rutas: {e}")
        return jsonify({'error': 'Error al obtener rutas'}), 500

    
    if rutas:
        try:
            primera_ruta = rutas[0]
            try:
                latitud = primera_ruta['legs'][0]['start_location']['lat']
            except KeyError:
                print("Error: 'legs' key not found in the API response.")
            latitud = primera_ruta['legs'][0]['start_location']['lat']
            print(primera_ruta)
            longitud = primera_ruta['legs'][0]['start_location']['lng']

            respuesta_clima = requests.get(f'http://localhost:5002/clima?latitud={latitud}&longitud={longitud}')
            respuesta_clima.raise_for_status()
            clima = respuesta_clima.json()

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener el clima: {e}")
            return jsonify({'error': 'Error al obtener el clima'}), 500
       
        try:
            respuesta_vehiculo = requests.get(
                f'http://localhost:5001/vehiculo?tipo={tipo_vehiculo}&clima={clima["descripcion"]}'
            )
            respuesta_vehiculo.raise_for_status()
            compatibilidad = respuesta_vehiculo.json()['compatibilidad']

            if compatibilidad:
                mejor_ruta = primera_ruta  
                return jsonify(mejor_ruta)
            else:
                return jsonify({'mensaje': 'El tipo de vehículo no es compatible con la ruta debido al clima.'})

        except requests.exceptions.RequestException as e:
            print(f"Error al verificar la compatibilidad del vehículo: {e}")
            return jsonify({'error': 'Error al verificar la compatibilidad del vehículo'}), 500

    else:
        return jsonify({'mensaje': 'No se encontraron rutas.'})

if __name__ == '__main__':
    app.run(debug=True, port=5003)