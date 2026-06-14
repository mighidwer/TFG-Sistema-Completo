# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · solver.py
 
    Este fichero contiene todo lo relacionado con el solver, incluyendo la configuración,
    el proceso de simulación, la gestión de las interrupciones, el tratamiento de las
    incidencias y el control del estado final.
    
"""

# Importación de librerías estándar
import signal
import os

# Importación de dependencias externas
import gurobipy

# Importación de módulos propios del proyecto
from Modelos import herramientasModelo



'''
    Ejecuta el proceso de simulación del solver de Gurobi sobre un modelo de optimización.

    Se encarga de gestionar la ejecución del solver de Gurobi, incluyendo la configuración de parámetros
    de optimización, la gestión de interrupciones externas, y la aplicación de rutinas de control de la
    optimización (como la parada anticipada en función del GAP relativo).

    Además, controla el estado final de la resolución del modelo (óptimo, factible, sin solución o
    infactible), así como el tratamiento de incidencias en caso de que el modelo no sea resoluble.

    Argumentos:
        - model (gurobipy.Model): Modelo de Gurobi a optimizar.
        - configSolver (dict):    Diccionario con los parámetros del solver.
        - numComerciantes (int):  Número de comerciantes usados en la simulación.

    Devuelve:
        - model (gurobipy.Model): Modelo de Gurobi tras la optimización, con su estado final.
'''
def ejecutar(model, configSolver, numComerciantes):

######################################## PARÁMETROS DEL SOLVER ########################################

##### TIEMPO DE SIMULACIÓN #####

    tiempoSimulacion = configSolver["tiempoSimulacion"]

##### TIEMPO DE ESPERA PARA ACTIVAR EL CONTROL DEL GAP #####

    tiempoGap = configSolver["tiempoGap"]

##### MARGEN DE OPTIMALIDAD (GAP) #####

    gapMaximo = configSolver["gapMaximo"]
    
##### CÁLCULO IIS (Irreducible Infeasible Set) #####

    calculoIIS = configSolver["calculoIIS"]


####################################### INTERRUPCIÓN DEL SOLVER #######################################

    # Cambiamos el manejador de señales para poder detener el solver si hay alguna interrupción
    signal.signal(signal.SIGINT, crearHandlerDetencion(model))


######################################### MODO DE SIMULACIÓN ##########################################

    # Ajustamos los parámetros del modelo
    if tiempoSimulacion != 0:  # Si se ha definido un tiempo máximo de simulación...
        model.setParam('TimeLimit', tiempoSimulacion)  # Configuramos el parámetro
    #model.setParam('OutputFlag', 0)  # Desactivamos la salida por pantalla del solver
    
    try:
        # Resolvemos el modelo
        if tiempoGap == 0 or (tiempoGap > tiempoSimulacion and tiempoSimulacion != 0):  # Si no se ha definido un tiempo de gap o es mayor que el tiempo máximo de simulación
            # Simulamos hasta encontrar el óptimo, o hasta el límite de tiempo (si se ha configurado)    
            model.optimize()
            
        else:  # Si se ha definido el tiempo de gap...
            # Ajustamos las variables que se van a usar en la función callback
            model._tiempoGap = tiempoGap  # Tiempo de espera para activar el control del GAP
            model._gapMaximo = gapMaximo  # Margen de optimalidad
            model._mensajeGap = False     # Flag de mensaje mostrado
            
            # Simulamos con "Rutina de Control de Optimización"
            model.optimize(callbackParadaAnticipada)

    finally:
        # Volvemos a activar el manejador de señales por defecto
        signal.signal(signal.SIGINT, signal.default_int_handler)


########################################## ESTADO DEL SOLVER ##########################################

    if model.status == gurobipy.GRB.OPTIMAL:  # Encontramos la solución óptima para el número de comerciantes 
        herramientasModelo.estadoSolver("OPTIMO", numComerciantes)
    
    elif model.status in [gurobipy.GRB.TIME_LIMIT, gurobipy.GRB.INTERRUPTED] and model.SolCount > 0:  # Encontramos una solución válida tras el tiempo máximo de simulación
        herramientasModelo.estadoSolver("FACTIBLE", numComerciantes)
    
    else:  # Si no la encontramos...
                    
        if model.status == gurobipy.GRB.INFEASIBLE:  # Si no existe ninguna solución factible...  
            herramientasModelo.estadoSolver("INFACTIBLE", numComerciantes)
            
            if calculoIIS:  # Si se ha habilitado el cálculo de IIS...
                herramientasModelo.calculandoIIS()
                # Creamos el directorio "Incidencias", si no existe ya
                os.makedirs("Incidencias", exist_ok=True)
                
                # Calculamos IIS y generamos un fichero con las restricciones problemáticas
                model.computeIIS()
                model.write(f"Incidencias/{numComerciantes}comerciantes.ilp")
        
        else:  # Si no se encontró una solución porque se agotó el tiempo de simulación...
            herramientasModelo.estadoSolver("SIN_SOLUCION", numComerciantes)


    return model  # Devolvemos el modelo con su estado final




'''
    Crea un manejador de señal para permitir la interrupción controlada del solver de Gurobi.

    Argumentos:
        - model (gurobipy.Model): Modelo de Gurobi en ejecución.

    Devuelve:
        - function: Función interna que actúa como handler de interrupción.
'''
def crearHandlerDetencion(model):
    
    '''
        Manejador de la señal de interrupción durante la resolución del modelo de optimización.
        Al detectar una interrupción externa, se fuerza la finalización controlada del solver de Gurobi.
    
        Argumentos:
            - sig (int):   Señal del sistema que provoca la interrupción (SIGINT).
            - frame (obj): Contexto de ejecución en el momento de la señal.
    '''
    def detenerSolver(sig, frame):
        print("\n **** Interrupción detectada. Deteniendo Gurobi... ****\n")
        try:
            model.terminate()
        except:
            pass

    return detenerSolver




'''
    Callback de Gurobi (Rutina de Control de la Optimización) que controla la finalización
    anticipada de la optimización en función del tiempo y del GAP.

    Durante los primeros segundos de simulación, el modelo se optimiza sin restricciones adicionales.
    A partir de un tiempo definido (tiempoGap), si el GAP relativo entre la mejor solución encontrada
    y la cota dual es menor o igual a un umbral (gapMaximo), la optimización se detiene y se conserva
    la mejor solución que se haya encontrado.

    Argumentos:
        - model (gurobipy.Model): Modelo de Gurobi en optimización.
        - where (int):            Punto de ejecución del callback.
'''
def callbackParadaAnticipada(model, where):
    
    if where == gurobipy.GRB.Callback.MIP:  # Si hay información de progreso disponible del MIP (Programación Entera Mixta)
        runtime = model.cbGet(gurobipy.GRB.Callback.RUNTIME)  # Tiempo transcurrido desde que comenzó la optimización

        # Antes del tiempo de activación del control del gap no lo evaluamos, buscamos el óptimo
        if runtime < model._tiempoGap:
            return
        
        # Mostramos el mensaje de la búsqueda del gap (sólo una vez)
        if not model._mensajeGap:
            print(f"\n **** ({model._tiempoGap}s) Rutina de Control de Optimización - Parada Anticipada si Gap ≤ {int(model._gapMaximo*100)}% ****\n")
            model._mensajeGap = True
       
        # Almacenamos los datos de la mejor solución encontrada en este instante
        best_obj = model.cbGet(gurobipy.GRB.Callback.MIP_OBJBST)
        best_bound = model.cbGet(gurobipy.GRB.Callback.MIP_OBJBND)

        if best_obj < gurobipy.GRB.INFINITY:  # Si es una solución factible...
            # Calculamos el gap relativo de la solución
            gap = abs(best_obj - best_bound) / abs(best_obj)
            
            if gap <= model._gapMaximo:  # Si el gap es menor que "gapMaximo"...
                model.terminate()  # Detenemos el solver y nos quedamos con la solución encontrada