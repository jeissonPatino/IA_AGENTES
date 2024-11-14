from flask import Flask, request, jsonify
import googlemaps

app = Flask(__name__)


API_KEY = "AIzaSyBufP9GhletrAG9Pwv8i69qh88hikYS5EM"  
gmaps = googlemaps.Client(key=API_KEY)

@app.route('/ruta', methods=['GET'])
def obtener_ruta():
    origen = request.args.get('origen')
    destino = request.args.get('destino')

    if not origen or not destino:
        return jsonify({'error': 'Origen y destino son requeridos'}), 400

   
    directions_result = gmaps.directions(origen,
                                         destino,
                                         mode="driving",
                                         language="es",
                                         units="metric")

    # Procesa la respuesta de la API 
    rutas = []
    for route in directions_result:
        pasos = []
        for leg in route['legs']:
            for step in leg['steps']:
                pasos.append(step['html_instructions'])
        rutas.append({
            'distancia': leg['distance']['text'],
            'tiempo': leg['duration']['text'],
            'pasos': pasos
        })

    return jsonify(rutas)

if __name__ == '__main__':
    app.run(debug=True, port=5000)