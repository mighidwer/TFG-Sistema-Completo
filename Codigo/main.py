# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · main.py

    Este fichero constituye el punto de entrada principal de la aplicación.
    Permite al usuario acceder a las distintas funcionalidades desarrolladas
    en el proyecto:
        
        1. Aplicación de búsqueda y visualización de rutas entre tiendas.
        2. Simulación simple de los modelos de distribución.
        3. Simulación MPC (Model Predictive Control) de los modelos de distribución.
    
    Además, coordina el flujo general del programa, gestionando la preparación
    de los datos, la selección del modelo de optimización y el procesamiento
    de los resultados obtenidos.
    
"""

# Importación de librerías estándar
import numpy as np

# Importación de módulos propios del proyecto
from Modelos import optimizarRutas, modeloSecuencial, modeloAleatorio, modeloGreedy
import horizonteDeslizante
import configuracion
import presentacion
import buscarRutas
import matrizRutas
import resultados



'''
    Función principal del sistema.
    
    Muestra un menú que permite al usuario seleccionar:
        1. Acceder a la aplicación 'BUSCAR RUTAS'.
        2. Ejecutar simulaciones simples utilizando distintos modelos de distribución.
        3. Ejecutar simulaciones MPC utilizando distintos modelos de distribución.
        4. Salir de la aplicación.
        
    En el modo de simulación, coordina la ejecución completa del programa, incluyendo:
        - La carga de la configuración del problema.
        - La generación de las matrices de rutas.
        - La selección y ejecución del modelo de optimización.
        - El procesamiento y análisis de los resultados obtenidos.

    Además, permite fijar una semilla aleatoria para poder realizar comparaciones
    entre los modelos partiendo desde el mismo punto de generación aleatoria.
'''
def main():
    
    # Menú de selección de opción
    while True:

        opcion = presentacion.menuMain()
        
        
        if opcion == "1":  # APLICACIÓN 'BUSCAR RUTAS'

            presentacion.mostrarProceso("🗺️ Iniciando aplicación de búsqueda de rutas entre tiendas...")
            buscarRutas.ejecutarApp()
            
            break
    
        
        elif opcion in ["2", "3"]:  # SIMULACIÓN SIMPLE / MPC
            
            # Comprobamos el modo de simulación elegido
            mpc = (opcion == "3")
            
            # Definimos la semilla de generación de números pseudoaleatorios
            np.random.seed(7)  # Para obtener siempre los mismos valores en los parámetros aleatorios y poder hacer comparaciones
            
            # Leemos la configuración de los parámetros del modelo
            config = configuracion.obtenerConfig()
            
            # Definimos los modelos disponibles
            modelos = {
                "1": ("Modelo de Optimización", optimizarRutas),
                "2": ("Modelo Aleatorio", modeloAleatorio),
                "3": ("Modelo Secuencial", modeloSecuencial),
                "4": ("Modelo Greedy", modeloGreedy)
            }
            
            # Menú de selección de modelo
            while True:
                
                opcionModelo = presentacion.menuModelos(mpc)
                
                if opcionModelo in modelos:
                    
                    nombreModelo, modelo = modelos[opcionModelo]
                    
                    # Llamamos al proceso de preparación de las matrices de datos
                    presentacion.mostrarProceso("🧮 Iniciando proceso de generación de matrices de rutas...")
                    matrizRutas.matrices(config["transporte"]["modo"])
            
                    
                    # Ejecución del modelo
                    if mpc:
        
                        # Ejecutamos MPC
                        presentacion.mostrarProceso(f"⚙️ Iniciando simulación MPC del modelo: {nombreModelo}...")
                        datos = horizonteDeslizante.ejecutar(config, modelo)
            
                    else:
                        
                        # Resolvemos el modelo elegido y leemos los resultados
                        presentacion.mostrarProceso(f"⚙️ Iniciando simulación del modelo: {nombreModelo}...")
                        datos = modelo.ejecutar(config)
                    
                    # Procesamos los resultados obtenidos para obtener los valores reales
                    presentacion.mostrarProceso("📈 Iniciando análisis de resultados de la simulación...")
                    resultados.procesarResultados(config, datos)
            
                    break
                     
            
                elif opcionModelo == "5":
                    break
                
                else:
                    presentacion.mensajeMenu("OPCION_NO_VALIDA", 2)
            
            
            # Si se ejecutó una simulación, salimos del programa
            if opcionModelo in modelos:
                break
    
           
        elif opcion == "4":  # SALIR
            presentacion.mensajeMenu("CERRANDO")
            break
    
        else:
            presentacion.mensajeMenu("OPCION_NO_VALIDA")




if __name__ == "__main__":
    main()