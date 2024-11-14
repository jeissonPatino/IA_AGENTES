# Sistema Multiagente para Encontrar la Mejor Ruta

Este proyecto implementa un sistema multiagente para encontrar la mejor ruta considerando el clima y el tipo de vehículo.

## Descripción

El sistema está compuesto por cuatro agentes:

*   Agente coordinador: Recibe la solicitud del usuario, consulta a los otros agentes y devuelve la mejor ruta.
*   Agente de rutas: Obtiene información sobre las rutas utilizando la API de Google Maps.
*   Agente de clima: Obtiene información meteorológica utilizando la API de OpenWeatherMap.
*   Agente de vehículos: Determina la compatibilidad entre el tipo de vehículo y la ruta, considerando el clima.

## Requisitos

*   Python 3.13.0
*   Las siguientes bibliotecas de Python:
    *   Flask
    *   flask_cors
    *   requests
    *   googlemaps

## Instalación

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/tu_usuario/tu_repositorio.git](https://github.com/tu_usuario/tu_repositorio.git)
    ```
2.  Instala las bibliotecas:
    ```bash
    pip install -r requirements.txt
    ```
3.  Obtén una clave de API de Google Maps y una clave de API de OpenWeatherMap.
4.  Configura las claves de API en los archivos `agente_rutas.py` y `agente_clima.py`.

## Ejecución

1.  Ejecuta cada agente en una terminal separada:
    ```bash
    python agente_coordinador.py
    python agente_rutas.py
    python agente_clima.py
    python agente_vehiculos.py
    ```
2.  Abre el archivo `index.html` en tu navegador web.

## Uso

1.  Introduce el origen, el destino y el tipo de vehículo en el formulario.
2.  Haz clic en el botón "Buscar".
3.  El sistema mostrará la mejor ruta, considerando el clima y la compatibilidad con el vehículo.

## Mejoras

*   Se ha implementado un algoritmo de selección de mejor ruta que considera el tiempo de viaje, la distancia, el clima y la dificultad de la ruta.
*   Se ha añadido la capacidad de obtener información del tráfico en tiempo real.
*   Se ha mejorado el manejo de errores en las respuestas de las APIs.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un "issue" o envía un "pull request" si tienes alguna sugerencia o mejora.

## Autor

Jeisson Andrés Patiño Ramirez
