from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/vehiculo', methods=['GET'])
def obtener_info_vehiculo():
    tipo_vehiculo = request.args.get('tipo')
    clima = request.args.get('clima')
    
    dificultad_ruta = request.args.get('dificultad')

    if not tipo_vehiculo or not clima or not dificultad_ruta:
        return jsonify({'error': 'Tipo de vehículo, clima y dificultad de ruta son requeridos'}), 400

    
    compatibilidad = True
    if tipo_vehiculo == "bicycling" and ("lluvia" in clima or dificultad_ruta == "alta"):
        compatibilidad = False
    
    if tipo_vehiculo == "walking" and ("lluvia" in clima or dificultad_ruta == "alta"):
        compatibilidad = False
    
    return jsonify({'compatibilidad': compatibilidad})

if __name__ == '__main__':
    app.run(debug=True, port=5001)