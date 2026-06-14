# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · postprocesado.py

    Este fichero implementa la fase de postprocesado de los modelos de optimización,
    transformando la salida del solver en una estructura de datos homogénea y
    estandarizada, independientemente del modelo matemático utilizado.
    
"""

# Importación de módulos propios del proyecto
from Modelos import herramientasModelo



'''
    Construye la salida estándar de cualquier modelo de optimización.

    Argumentos:
        - model (gurobipy.Model):                           Modelo Gurobi resuelto.
        - tiempoSimulacionTotal (datetime.timedelta):       Tiempo total de simulación del modelo.
        - numComerciantes (int):                            Número de comerciantes con el que se ha resuelto el modelo.
        - demandaTienda (list[list[list[list[int]]]]):      Demanda media diaria de las tiendas.
        - variables (dict[str, dict[tuple, gurobipy.Var]]): Diccionario con las variables de decisión del modelo.

    Devuelve:
        - dict[str, dict]: Diccionario con la estructura estándar.
'''
def construirSalida(model, tiempoSimulacionTotal, numComerciantes, demandaTienda, variables):

######################################## VARIABLES DE DECISIÓN ########################################
    
    ##### TIENDAS VISITADAS #####

    V = {k: herramientasModelo.valor(var) for k, var in variables["V"].items()}

    ##### CAMINOS ENTRE TIENDAS #####

    X = {k: herramientasModelo.valor(var) for k, var in variables["X"].items()}

    ##### STOCK DE LAS TIENDAS #####

    S = {k: herramientasModelo.valor(var) for k, var in variables["S"].items()}

    ##### UNIDADES ENTREGADAS #####

    U = {k: herramientasModelo.valor(var) for k, var in variables["U"].items()}

    ##### DÍAS LABORALES #####

    L = {k: herramientasModelo.valor(var) for k, var in variables["L"].items()}


############################################### RETURN ################################################
    
    return {
    
        ##### DATOS DE LA SIMULACIÓN #####
    
        "datosSimulacion": {
            "numComerciantes": numComerciantes,
            "demandaTienda": demandaTienda,
            "tiempoSimulacionTotal": tiempoSimulacionTotal
        },
        
        ##### DATOS DEL MODELO #####
        
        "datosModelo": {
            "numVariables": model.NumVars,
            "numRestricciones": model.NumConstrs
        },
            
        ##### VARIABLES DE DECISIÓN #####
    
        "variablesDecision": {
    
            "V": V,
            "X": X,
            "S": S,
            "U": U,
            "L": L
        }
    }