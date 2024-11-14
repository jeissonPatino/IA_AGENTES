from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/vehiculo', methods=['GET'])
def obtener_info_vehiculo():
    tipo_vehiculo = request.args.get('tipo')
    clima = request.args.get('clima')  # Recibe la descripción del clima

    if not tipo_vehiculo or not clima:
        return jsonify({'error': 'Tipo de vehículo y clima son requeridos'}), 400

    # Define la lógica para determinar la compatibilidad
    compatibilidad = True  # Por defecto, asumimos que es compatible
    if tipo_vehiculo == "bicicleta" and "lluvia" in clima:
        compatibilidad = False
    # ... (añade más reglas según tus necesidades)

    return jsonify({'compatibilidad': compatibilidad})

if __name__ == '__main__':
    app.run(debug=True, port=5001)