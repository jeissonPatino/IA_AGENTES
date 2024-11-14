import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error 
# no lo logre integrar para mejorar los tiempos 
datos = pd.read_csv('ruta_al_archivo.csv')

X = datos[['distancia', 'tipo_vehiculo', 'trafico', 'clima']]
y = datos['tiempo_viaje']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)



modelo = LinearRegression()
modelo.fit(X_train, y_train)


predicciones = modelo.predict(X_test)


mse = mean_squared_error(y_test, predicciones)

import pickle
nombre_archivo = 'modelo_entrenado.pkl'
with open(nombre_archivo, 'wb') as archivo:
    pickle.dump(modelo, archivo)

print(f'Error cuadrático medio: {mse}')