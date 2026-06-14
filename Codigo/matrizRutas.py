# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · matrizRutas.py

    Este fichero contiene las funciones necesarias para crear los archivos ".csv" que almacenan
    los datos de las tiendas consultados al servidor OSRM y verificar que son correctos.
    
"""

# Importación de librerías estándar
from datetime import datetime, timedelta
from decimal import Decimal
import json
import os

# Importación de dependencias externas
import pandas as pd
import numpy as np

# Importación de módulos propios del proyecto
import utilidades
import osrm



'''
    Verifica la existencia de los ficheros que almacenan distancias, tiempos y rutas entre tiendas.
    Si no existen, los crea en el directorio Recursos.
    
    Argumentos:
        - modo (str): Modo de desplazamiento. Indica los ficheros cuya existencia se debe verificar.

    Devuelve:
        - ficheros (bool): True si ambos ficheros ya existían, False si alguno se ha tenido que crear.
'''
def verificarFicheros(modo):
    
    ficheros = True
    # Lista con el nombre de los ficheros que contienen la información
    archivos = [f"DatosRutas/distanciaRutas{modo.capitalize()}.csv", f"DatosRutas/tiempoRutas{modo.capitalize()}.csv", f"DatosRutas/rutas{modo.capitalize()}.csv"]

    print("\n\t   🛠 Comprobando la existencia de los ficheros...\n")

    for archivo in archivos:
        if not os.path.isfile(archivo):
            print(f"\t\t ❌ {archivo} no existe. Generando...")
            ficheros = False
            with open(archivo, 'w'):
                print(f"\t\t 📝 {archivo} generado")
        else:
            print(f"\t\t 📝 {archivo} ya existe")

    return ficheros




'''
    Verifica la validez del contenido de los ficheros con respecto al número actual de tiendas
    y compara aleatoriamente datos reales con los almacenados.

    Argumentos:
        - modo (str):               Modo de desplazamiento. Indica los ficheros cuyo contenido se debe comprobar.
        - latitudes (list[float]):  Lista de latitudes de las tiendas.
        - longitudes (list[float]): Lista de longitudes de las tiendas.

    Devuelve:
        - bool: True si todos los valores coinciden, False si hay discrepancias o el número de tiendas no coincide.
'''
def verificarContenido(modo, latitudes, longitudes):
   
    print("\n\t   🔍 Comprobamos si los ficheros contienen información\n")
    
    try:  # Intentamos leer las matrices almacenadas
        df_distancia = pd.read_csv(f"DatosRutas/distanciaRutas{modo.capitalize()}.csv", index_col=0)
        df_tiempo = pd.read_csv(f"DatosRutas/tiempoRutas{modo.capitalize()}.csv", index_col=0)
        df_ruta = pd.read_csv(f"DatosRutas/rutas{modo.capitalize()}.csv", index_col=0)
        
        print("\t\t ✅ Los ficheros tienen información almacenada")
        
    except pd.errors.EmptyDataError:  # Si los ficheros están vacíos...
        print("\t\t ❌ Los ficheros están vacíos")
        return False
    
    print("\n\t   🔍 Comprobamos el número de tiendas\n")
    
    # Comprobamos si el número de tiendas ha cambiado
    num_tiendas_csv_dist = df_distancia.shape[0]
    num_tiendas_csv_tiem = df_tiempo.shape[0]
    num_tiendas_csv_ruta = df_ruta.shape[0]
    num_tiendas_actual = len(latitudes)
    
    if num_tiendas_csv_dist != num_tiendas_actual or num_tiendas_csv_tiem != num_tiendas_actual or num_tiendas_csv_ruta != num_tiendas_actual:
        print("\t\t ❌ El número de tiendas es incorrecto")
        return False
    else:
        print(f"\t\t ✅ El número de tiendas es correcto ({num_tiendas_actual-1} tiendas)")

    print("\n\t   🔍 Comprobamos el contenido de los ficheros")

    # Número de pruebas que se van a realizar
    num_pruebas = 10
    
    for i in range(num_pruebas):
        t1, t2 = np.random.choice(len(df_distancia), size=2, replace=False)
        
        # Obtenemos los datos reales desde el servidor OSRM
        distancia_real, tiempo_real, ruta_real = osrm.obtenerRuta(modo, latitudes[t1], longitudes[t1], latitudes[t2], longitudes[t2])
    
        # Obtenemos los datos desde los ficheros CSV
        tienda = lambda i: "oficina" if i == 0 else f"tienda {i}"
    
        distancia_csv = df_distancia.loc[tienda(t1), tienda(t2)]
        tiempo_csv = df_tiempo.loc[tienda(t1), tienda(t2)]
        ruta_csv = json.loads(df_ruta.loc[tienda(t1), tienda(t2)])

        # Mostramos los resultados y diferencias
        nombre_tienda = lambda i: "Oficina" if i == 0 else f"Tienda {i}"
        print(f"\n\t\t PRUEBA {i+1}: {nombre_tienda(t1)} <-> {nombre_tienda(t2)}:")
        print(f"\t\t  - DISTANCIA (CSV): {distancia_csv} km \t|  Real: {distancia_real} km")
        print(f"\t\t  - TIEMPO    (CSV): {tiempo_csv} h  \t|  Real: {tiempo_real} h")
        print(f"\t\t  - RUTA [±5] (CSV): {len(ruta_csv)} pts  \t|  Real: {len(ruta_real)} pts")
    
        
        # Validamos si coinciden (con un margen de error pequeño)
        dist_ok = abs(Decimal(distancia_csv) - Decimal(distancia_real)) < 0.05
        time_ok = abs(Decimal(tiempo_csv) - Decimal(tiempo_real)) < 0.05
        ruta_ok = abs(len(ruta_csv) - len(ruta_real)) <= 5
        
        if dist_ok and time_ok and ruta_ok:
            print("\t\t ✅ Datos correctos")
        else:
            print("\t\t ❌ Datos incorrectos")
            return False
    
    return True




'''
    Rellena y guarda los ficheros con los datos de distancia, tiempo y ruta entre cada par de tiendas.
    Optimiza el proceso evitando realizar consultas repetidas (modo "foot") y omitiendo las diagonales.

    Argumentos:
        - modo (str):               Modo de desplazamiento. Indica los ficheros a escribir.
        - latitudes (list[float]):  Lista de latitudes de las tiendas.
        - longitudes (list[float]): Lista de longitudes de las tiendas.

    Guardado:
        - "DatosRutas/distanciaRutas.csv{modo.capitalize()}": Matriz de distancias en kilometros.
        - "DatosRutas/tiempoRutas.csv{modo.capitalize()}":    Matriz de tiempos en horas.
        - "DatosRutas/rutas{modo.capitalize()}.csv":          Matriz de rutas.
'''    
def escribirFicheros(modo, latitudes, longitudes): 

    N = len(latitudes)
    tiendas = ["oficina" if i == 0 else f"tienda {i}" for i in range(N)]
    nombre = lambda x: "Oficina" if x == 0 else f"Tienda {x}"
    
    # Inicializamos las matrices
    matriz_distancia = np.full((N, N), np.nan)
    matriz_tiempo = np.full((N, N), np.nan)
    matriz_rutas = [[None for _ in range(N)] for _ in range(N)]  # Aquí guardaremos las rutas completas
    
    # Instante inicial de la escritura
    start = datetime.now()
    
    # Rellenamos las matrices con la información obtenida tras consultar al servidor OSRM
    for i in range(N):
        print("")
        for j in range(N):
            
            # Comprobamos el índice de las dos tiendas
            if i == j:  # Si coincide...
            
                # No hay que realizar ninguna consulta (tienda origen = tienda destino)
                matriz_distancia[i][j] = 0
                matriz_tiempo[i][j] = 0
                matriz_rutas[i][j] = []
                print(f"\t\t [{i}/{N-1}] {nombre(i)} <-> {nombre(j)}: 0")
            
            
            elif i > j and modo == "foot":  # Si el índice de la tienda origen es mayor que el de la tienda destino y estamos en el modo "foot"...
            
                # Reutilizamos el valor de las consultas realizadas anteriormente, ya que la ida y la vuelta será igual
                matriz_distancia[i][j] = matriz_distancia[j][i]
                matriz_tiempo[i][j] = matriz_tiempo[j][i]
                matriz_rutas[i][j] = matriz_rutas[j][i]
                
                
            else:  # Si no coincide...
                
                # Realizamos la consulta
                print(f"\t\t [{i}/{N-1}] Consultando {nombre(i)} <-> {nombre(j)}...")
                distancia, tiempo, ruta = osrm.obtenerRuta(modo, latitudes[i], longitudes[i], latitudes[j], longitudes[j])
                
                matriz_distancia[i][j] = distancia
                matriz_tiempo[i][j] = tiempo
                matriz_rutas[i][j] = json.dumps(ruta)  # Convertimos la lista a string


    # Creamos los DataFrames (estructura de datos bidimensional)
    df_distancia = pd.DataFrame(matriz_distancia, index=tiendas, columns=tiendas)
    df_tiempo = pd.DataFrame(matriz_tiempo, index=tiendas, columns=tiendas)
    df_rutas = pd.DataFrame(matriz_rutas, index=tiendas, columns=tiendas)
    
    # Guardamos la información en los ficheros
    df_distancia.to_csv(f"DatosRutas/distanciaRutas{modo.capitalize()}.csv")
    df_tiempo.to_csv(f"DatosRutas/tiempoRutas{modo.capitalize()}.csv")
    df_rutas.to_csv(f"DatosRutas/rutas{modo.capitalize()}.csv")
    
    # Instante final de la escritura
    end = datetime.now()
    
    print(f"\n\t   ✅ Contenido de los ficheros del modo \"{modo}\" generado correctamente")

    print(f"\t\t ⏱ Tiempo total de las consultas: {timedelta(seconds=round((end - start).total_seconds()))}")




'''
    Lee los datos numéricos desde un fichero CSV y devuelve la matriz sin etiquetas (sin primera fila/columna).

    Argumentos:
        - fichero (str): Ruta del archivo CSV a leer.

    Devuelve:
        - matriz (ndarray): Matriz NumPy con los valores numéricos.
        - df (DataFrame):   DataFrame con los valores.
        - None:             Si ocurre algún error en la lectura.
'''
def leerDatos(fichero):
    try:
        if fichero.startswith("DatosRutas/rutas"):
            # Leemos con índice múltiple: origen, destino
            df = pd.read_csv(fichero, index_col=0)
            return df
        else:
            df = pd.read_csv(fichero, index_col=0)
            matriz = df.to_numpy()
            return matriz
        
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {fichero}")
        return None
    except Exception as e:
        print(f"⚠️ Error al leer el archivo: {e}")
        return None

  


'''
    Función principal para preparar las matrices de distancias y tiempos.

    Acciones:
        - Inicia el servidor OSRM.
        - Obtiene la información geográfica de las tiendas.
        - Verifica si existen los ficheros necesarios.
            - Si no existen, los genera.
            - Si existen, verifica su validez.
                - Si no son válidos, los regenera.
        - Finalmente, detiene el servidor OSRM.
    
    Argumentos:
        - modo (str): Modo de desplazamiento. Indica los ficheros a escribir.
'''
def matrices(modo):
    
    # Instante inicial de la ejecución
    start = datetime.now()
    
    # Obtenemos la información de las tiendas
    nombres, direcciones, tipos, latitudes, longitudes = utilidades.obtenerInfo()
        
    print(f"\n\t 🗺️ MODO DE DESPLAZAMIENTO \"{modo.upper()}\"")

    # Iniciamos el servidor OSRM
    osrm.iniciarServidor(modo)
    
    try:
                    
        # Verificamos la existencia de los ficheros en los que vamos a almacenar los datos
        if not verificarFicheros(modo):
            # Si no existían, los rellenamos con los datos
            print("\n\t   📊 Generando el contenido de los ficheros...")
            escribirFicheros(modo, latitudes, longitudes)
        else:        
            # Si los ficheros ya existían, verificamos su contenido
            if not verificarContenido(modo, latitudes, longitudes):
                print("\n\t   ⚠️ El contenido de los ficheros es incorrecto")
                print("\n\t   🔄 Regenerando el contenido de los ficheros...")
                # Si no es correcto, los rellenamos de nuevo
                escribirFicheros(modo, latitudes, longitudes)
            else:
                print(f"\n\t   ✅ El contenido de los ficheros del modo \"{modo}\" es correcto")
    
    finally:
        # Detenemos el servidor al cerrar el programa
        osrm.detenerServidor()
    
    # Instante final de la ejecución
    end = datetime.now()
    
    # Mostramos el tiempo total de ejecución
    print(f"\n\t ⏱ Tiempo total de ejecución: {timedelta(seconds=round((end - start).total_seconds()))}\n")