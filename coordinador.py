import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

@app.route('/mejor_ruta', methods=['POST'])
def obtener_mejor_ruta():
    data = request.get_json()
    origen = data.get('origen')
    destino = data.get('destino')
    tipo_vehiculo = data.get('tipo_vehiculo')

    # 1. Obtener rutas de Agente de rutas
    try:
        respuesta_ruta = requests.get(
            f'http://localhost:5000/ruta?origen={origen}&destino={destino}&tipo_vehiculo={tipo_vehiculo}'
        )
        respuesta_ruta.raise_for_status()
        rutas = respuesta_ruta.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener rutas: {e}")
        return jsonify({'error': 'Error al obtener rutas'}), 500

    # 2. Obtener clima de Agente de clima (usando la primera ruta como ejemplo)
    if rutas:
        try:
            primera_ruta = rutas[0]

            # Obtener la latitud y longitud de la respuesta del agente de rutas
            latitud = primera_ruta['latitud_inicio']
            longitud = primera_ruta['longitud_inicio']

            respuesta_clima = requests.get(
                f'http://localhost:5002/clima?latitud={latitud}&longitud={longitud}'
            )
            respuesta_clima.raise_for_status()
            clima = respuesta_clima.json()

            # 3. Verificar compatibilidad con Agente de vehículos
            # Lógica para determinar la dificultad según el modo y el tipo de vehículo
            modo_transporte = "driving"  # O el modo que corresponda según el tipo de vehículo
            if modo_transporte == "bicycling":
                dificultad = "alta"
            elif modo_transporte == "walking" and tipo_vehiculo == "bicicleta":
                dificultad = "media"
            else:
                dificultad = "baja"

            respuesta_vehiculo = requests.get(
                f'http://localhost:5001/vehiculo?tipo={tipo_vehiculo}&clima={clima["descripcion"]}&dificultad={dificultad}'
            )
            respuesta_vehiculo.raise_for_status()
            compatibilidad = respuesta_vehiculo.json()['compatibilidad']

            if compatibilidad:
                mejor_ruta = seleccionar_mejor_ruta(rutas, clima,
                                                    tipo_vehiculo, dificultad)

                # Agregar origen y destino a la respuesta
                mejor_ruta['origen'] = origen
                mejor_ruta['destino'] = destino

                return jsonify(mejor_ruta)
            else:
                return jsonify({
                    'mensaje':
                    'El tipo de vehículo no es compatible con la ruta debido al clima o la dificultad.'
                })

        except requests.exceptions.RequestException as e:
            print(
                f"Error al obtener el clima o verificar la compatibilidad del vehículo: {e}"
            )
            return jsonify({
                'error':
                'Error al obtener el clima o verificar la compatibilidad del vehículo'
            }), 500
    else:
        return jsonify({'mensaje': 'No se encontraron rutas.'})

def seleccionar_mejor_ruta(rutas, clima, tipo_vehiculo, dificultad):
    """
    Selecciona la mejor ruta usando un algoritmo simple que considera:
    - Tiempo de viaje (menor tiempo -> mejor)
    - Distancia (menor distancia -> mejor)
    - Clima (lluvia -> penalización)
    - Dificultad (dificultad alta -> penalización)
    """

    mejor_puntuacion = float('inf')
    mejor_ruta = None

    for ruta in rutas:
        tiempo = convertir_tiempo_a_minutos(ruta['tiempo'])
        distancia = convertir_distancia_a_km(ruta['distancia'])

        puntuacion = tiempo * 0.7 + distancia * 0.3  # Ponderación tiempo/distancia

        if "lluvia" in clima['descripcion']:
            puntuacion += 30  # Penalización por lluvia

        if dificultad == "alta":
            puntuacion += 50  # Penalización por dificultad alta
        elif dificultad == "media":
            puntuacion += 20  # Penalización por dificultad media

        if puntuacion < mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_ruta = ruta

    return mejor_ruta

def convertir_tiempo_a_minutos(tiempo_str):
    """Convierte una cadena de tiempo (ej. "1 h 30 min") a minutos."""
    try:
        horas, minutos = map(int, tiempo_str.split()[::2])
        return horas * 60 + minutos
    except ValueError:
        return 0  # Manejar errores de formato

def convertir_distancia_a_km(distancia_str):
    """Convierte una cadena de distancia (ej. "100 km") a kilómetros."""
    try:
        return float(distancia_str.split()[0])
    except ValueError:
        return 0  # Manejar errores de formato

if __name__ == '__main__':
    app.run(debug=True, port=5003)