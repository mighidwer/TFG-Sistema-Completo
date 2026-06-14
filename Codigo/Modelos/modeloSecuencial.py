# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · modeloSecuencial.py

    Este fichero implementa un modelo alternativo basado en una estrategia secuencial de
    visitas, en la que las tiendas se recorren siguiendo un orden fijo predefinido.
    
"""

# Importación de módulos propios del proyecto
from Modelos import modeloBase, herramientasModelo



'''
    Construye el modelo secuencial, basado en una estrategia de visitas en la que las tiendas
    se recorren siguiendo un orden fijo prefijado según su identificador (1 -> 2 -> 3 ...).
    Define las variables de decisión, restricciones y función objetivo del problema. Tras esto,
    ejecuta el solver y devuelve las variables y parámetros de la solución obtenida.

    Argumentos:
        - config (dict[str, Any]):             Diccionario con la configuración completa del problema y los datos necesarios para la simulación.
        - numComerciantesFijo (int, opcional): Indica el número de comerciantes encontrado en la primera iteración de la optimización MPC.
        - diaIteracionMPC (int):               Día de la iteración actual de la simulación MPC.

    Devuelve:
        - resultados (dict[str, Any]): Diccionario con las variables de decisión y los parámetros obtenidos tras la optimización del modelo.
'''
def ejecutar(datos, numComerciantesFijo=None, diaIteracionMPC=0):
    
    # Llamamos al modelo base, indicando la función encargada de generar las rutas predefinidas de este modelo
    return modeloBase.ejecutar(datos, generarVisitasRutasSecuencial, numComerciantesFijo, diaIteracionMPC)




'''
    Genera simultáneamente las variables de visitas V[c,d,i] y las variables de ruta X[c,d,i,j]
    a partir de una asignación secuencial (1 → 2 → 3 → ...) de tiendas a los comerciantes.

    Argumentos:
        - numComerciantes (int):              Número de comerciantes disponibles.
        - numDias (int):                      Número total de días de simulación.
        - numTiendas (int):                   Número total de tiendas (incluyendo oficina como nodo 0).
        - distanciaRutas (list[list[float]]): Matriz de distancias entre ubicaciones.
        - tiempoRutas (list[list[float]]):    Matriz de tiempos entre ubicaciones.
        - distanciaMax (float):               Distancia máxima permitida por jornada.
        - tiempoMax (float):                  Tiempo máximo permitido por jornada.
        - tiempoVisita (float):               Tiempo de permanencia en cada tienda.
        - frecuenciaVisita (int):             Intervalo de días entre visitas.
        - diaIteracionMPC (int):              Día de la iteración actual de la simulación MPC.

    Devuelve:
        - V (dict[tuple[int,int,int], int]):     Variables binarias de visita a tiendas por comerciante, día y tienda.
        - X (dict[tuple[int,int,int,int], int]): Variables binarias de las rutas empleadas.
'''
def generarVisitasRutasSecuencial(numComerciantes, numDias, numTiendas, distanciaRutas, tiempoRutas, distanciaMax, tiempoMax, tiempoVisita, frecuenciaVisita, diaIteracionMPC=0):
    
    secuencias = {}
        
    # Creamos el orden de visitas
    orden = list(range(1, numTiendas))
    
    # Asignamos las tiendas a visitar para los días correspondientes, ya sea simulación simple o MPC
    for d in range(numDias):

        # Día global dentro de la simulación MPC
        diaGlobal = diaIteracionMPC + d

        # Sólo visitamos cuando toca
        if diaGlobal % frecuenciaVisita != 0:
            continue

        secuencias[d] = list(orden)
    
    return herramientasModelo.generarVisitasRutas(numComerciantes, numDias, numTiendas, distanciaRutas, tiempoRutas, distanciaMax, tiempoMax, tiempoVisita, secuencias)