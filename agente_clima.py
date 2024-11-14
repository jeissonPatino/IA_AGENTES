import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/clima', methods=['GET'])
def obtener_clima():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')

    if not latitud or not longitud:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    API_KEY = "046691bc72e28c0774b63e4eb29630dc"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json() 


        clima = {
            'temperatura': data['main']['temp'],
            'descripcion': data['weather'][0]['description'],
        }

        return jsonify(clima)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return jsonify({'error': 'Error fetching weather data'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)