# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · osrm.py

    Este fichero contiene las funciones necesarias para el control del servidor OSRM (OpenStreetMap),
    tanto para el arranque como para la detención, así como para realizar consultas.
    
"""

# Importación de librerías estándar
from decimal import Decimal, ROUND_HALF_UP
import subprocess
import time
import os

# Importación de dependencias externas
import requests



'''
    Inicia el servidor OSRM (OpenStreetMap) para calcular rutas entre tiendas.

    Argumentos:
        - modo (str): Modo de desplazamiento. Indica el servidor que se debe iniciar.
    
    Proceso:
        1. Cambia al directorio "Recursos" (si no está ya en él) donde están los archivos OSRM.
        2. Lanza un terminal CMD que ejecuta el script "iniciarServidor.bat" para iniciar el servidor del modo indicado.
        3. Si los archivos OSRM no están generados, los crea y espera su finalización.
        4. Verifica que el servidor está activo antes de continuar.
'''
def iniciarServidor(modo):

    # Definimos la dirección del servidor OSRM en función del modo de desplazamiento
    if modo == "foot":
        puerto = 5000
    elif modo == "bike":
        puerto = 5001
        
    url=f"http://localhost:{puerto}"
        
    # Nos movemos al directorio Recursos para trabajar con los scripts
    recursos_path = os.path.join(os.getcwd(), "Recursos")
    if not os.getcwd().endswith("Recursos"):
        os.chdir(recursos_path)
        
    # Para abrir un terminal CMD y ver la ejecución del script
    subprocess.Popen(fr'start cmd /c "Scripts\iniciarServidor.bat {modo}"', shell=True)
      #  /k - Abre el terminal y se queda abierto al finalizar la ejecución
      #  /c - Abre el terminal y lo cierra al finalizar la ejecución
    
    # Comprobamos si los archivos OSRM ya están generados
    if not os.path.exists(f"OSRM/data/{modo}/sevilla.osrm.names") or not os.path.exists(f"OSRM/data/{modo}/sevilla.osrm.hsgr"):
        print(f"\n\t   🔧 Generando Archivos OSRM (Modo \"{modo}\")...")
        time.sleep(40)  # Esperamos 40 segundos mientras se generan los archivos OSRM
    
    # Iniciamos el servidor OSRM y esperamos hasta que esté activo
    print(f"\n\t   🚀 Iniciando Servidor OSRM (Modo \"{modo}\")...")
        
    while True:
        try:
            requests.get(url)
            print(f"\n\t   🎯 Servidor OSRM (Modo \"{modo}\") listo para usar")
            break
        except requests.ConnectionError:
            print("\t   ⏳ Esperando que OSRM se inicie...")
            time.sleep(3)  # Esperamos 3 segundos antes de volver a intentarlo




'''
    Detiene el servidor OSRM ejecutando un script de cierre.

    Proceso:
        1. Ejecuta el script "detenerServidor.bat" para detener el servidor OSRM.
        2. Muestra un mensaje confirmando la detención.
'''
def detenerServidor():
    
    print("\n\t   🛑 Deteniendo Servidor OSRM...")
    subprocess.run([r"Scripts\detenerServidor.bat"], shell=True)
    print("\n\t   ✅ Servidor OSRM detenido.")




'''
    Comprueba si el servidor OSRM está activo. Si no lo está, lo reinicia.

    Argumentos:
        - modo (str): Modo de desplazamiento. Indica el servidor que se debe comprobar.

    Proceso:
        1. Intenta hacer una petición al servidor.
        2. Si la conexión falla, inicia nuevamente el servidor.
'''
def servidorActivo(modo):

    # Definimos la dirección del servidor OSRM en función del modo de desplazamiento
    if modo == "foot":
        puerto = 5000
    elif modo == "bike":
        puerto = 5001
        
    url=f"http://localhost:{puerto}"
    
    try:
        requests.get(url)
        print(f"\n\t   ✅ Servidor OSRM (Modo \"{modo}\") activo")
    except requests.ConnectionError:
        print(f"\n\t   🛑 Servidor OSRM (Modo \"{modo}\") inactivo. Reiniciando...")
        iniciarServidor(modo)




'''
    Consulta al servidor OSRM para obtener la distancia, el tiempo estimado y la ruta entre dos tiendas.

    Argumentos:
        - modo (str):   Modo de desplazamiento. Indica el servidor al que se le deben realizar las consultas.
        - lat1 (float): Latitud de la tienda de origen.
        - lon1 (float): Longitud de la tienda de origen.
        - lat2 (float): Latitud de la tienda de destino.
        - lon2 (float): Longitud de la tienda de destino.

    Devuelve:
        - tuple: (distancia, tiempo, ruta), donde:
            - distancia (Decimal):      Distancia en kilómetros entre las dos tiendas.
            - tiempo (Decimal):         Tiempo estimado de recorrido entre las dos tiendas.
            - ruta (list[list[float]]): Lista de coordenadas de la ruta entre las dos tiendas.
    Si hay un error, devuelve un diccionario con la clave "error".
'''
def obtenerRuta(modo, lat1, lon1, lat2, lon2):
    
    # Nos aseguramos que el servidor está activo antes de realizar la consulta
    #servidorActivo(modo)

    # Construimos la URL con las coordenadas recibidas y el modo de desplazamiento
    if modo == "foot":
        puerto = 5000
        urlModo = "walking"
    elif modo == "bike":
        puerto = 5001
        urlModo = "cycling"

    url = f"http://localhost:{puerto}/route/v1/{urlModo}/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"

    # Realizamos la petición al servidor OSRM
    response = requests.get(url)

    # Verificamos si la respuesta es válida
    if response.status_code == 200:
        data = response.json()
        
        if data["code"] == "Ok":  # Si es válida
            distancia = data["routes"][0]["distance"]/1000  # Distancia en kilómetros
            tiempo = data["routes"][0]["duration"]/3600     # Tiempo en horas
            
            # Redondeamos la distancia en kilómetros a dos decimales
            distancia = Decimal(str(distancia)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            # Redondeamos el tiempo en horas a dos decimales
            tiempo = Decimal(str(tiempo)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                        
            # Obtenemos la ruta entre las tiendas
            ruta = data["routes"][0]["geometry"]["coordinates"]

            return distancia, tiempo, ruta
        
        else:  # Si no es válida
            return {"error": "Respuesta inválida de OSRM"}
        
    else:  # En caso de error en la solicitud
        return {"error": f"Error en la solicitud: {response.status_code}"}