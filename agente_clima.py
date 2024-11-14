from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/clima', methods=['GET'])
def obtener_clima():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')

    if not latitud or not longitud:
        return jsonify({'error': 'Latitud y longitud son requeridas'}), 400

    API_KEY = "1e123f9fe34e7cc3f5200514d89e401f"  
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()


    clima = {
        'temperatura': data['main']['temp'],
        'descripcion': data['weather'][0]['description'],
    }

    return jsonify(clima)

if __name__ == '__main__':
    app.run(debug=True, port=5002)