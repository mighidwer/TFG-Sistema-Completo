# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · herramientasModelo.py

    Este fichero contiene las funciones auxiliares utilizadas por los modelos de optimización.
    
"""

# Importación de librerías estándar
from decimal import Decimal, ROUND_HALF_UP
import shutil
import sys

# Importación de dependencias externas
import numpy as np



############################### GENERACIÓN DE DATOS PARA LA SIMULACIÓN ################################

'''
    Genera un número aleatorio en función del tipo de tienda, 
    utilizando una distribución de Poisson.

    Argumentos:
        - tipo (str): Tipo de tienda. Puede ser: "Muy Pequeña", "Pequeña", "Mediana", "Grande", o "Muy Grande".

    Devuelve:
        - int: Número aleatorio según el tipo de tienda.
'''
def tipoTienda(tipo):
    
    #np.random.seed(27)  # Para obtener siempre los mismos valores en los parámetros aleatorios
    
    lamda = 200  # Valor provisional en caso de error
    
    if tipo == "Muy Pequeña":
        lamda = 100
    elif tipo == "Pequeña":
        lamda = 175
    elif tipo == "Mediana":
        lamda = 250
    elif tipo == "Grande":
        lamda = 325
    elif tipo == "Muy Grande":
        lamda = 400
        
    return np.random.poisson(lam=lamda)




'''
    Genera la capacidad de cada tienda en función de su tipo.

    Argumentos:
        - numTiendas (int):  Número total de tiendas.
        - tipos (list[str]): Lista con el tipo de cada tienda.

    Devuelve:
        - list[int]: Capacidad de cada tienda.
'''
def generarCapacidadTienda(numTiendas, tipos):
    
    capacidadTienda = [0 for i in range(numTiendas)]
    
    for i in range(1, numTiendas):
        capacidadTienda[i] = tipoTienda(tipos[i])

    return capacidadTienda




'''
    Genera el stock inicial de cada tienda para cada escenario.

    Argumentos:
        - numEscenarios (int): Número de escenarios.
        - numTiendas (int):    Número total de tiendas.
        - numBebidas (int):    Número de bebidas.
        - tipos (list[str]):   Lista con el tipo de cada tienda.

    Devuelve:
        - list[list[list[int]]]: Stock inicial por escenario, tienda y bebida.
'''
def generarStockInicial(numEscenarios, numTiendas, numBebidas, tipos):
    
    stockInicial = [[[0 for b in range(numBebidas)] for i in range(numTiendas)] for e in range(numEscenarios)]
    
    for e in range(numEscenarios):
        for i in range(1, numTiendas):
            for b in range(numBebidas):
                stockInicial[e][i][b] = int(tipoTienda(tipos[i])/(numBebidas+1))

    return stockInicial




'''
    Genera la demanda media diaria de cada tienda.

    Argumentos:
        - numEscenarios (int): Número de escenarios.
        - numTiendas (int):    Número total de tiendas.
        - numBebidas (int):    Número de bebidas.
        - numDias (int):       Número de días.
        - tipos (list[str]):   Lista con el tipo de cada tienda.

    Devuelve:
        - list[list[list[list[int]]]]: Demanda por escenario, día, tienda y bebida.
'''
def generarDemandaTienda(numEscenarios, numTiendas, numBebidas, numDias, tipos):

    demandaTienda = [[[[0 for b in range(numBebidas)] for i in range(numTiendas)] for d in range(numDias)] for e in range(numEscenarios)]
    
    for e in range(numEscenarios):
        for i in range(1, numTiendas):
            for b in range(numBebidas):
                demanda = int(tipoTienda(tipos[i])/(numBebidas+7))
                for d in range(numDias):
                    demandaTienda[e][d][i][b] = demanda

    return demandaTienda




'''
    Genera el precio de cada bebida en cada tienda.

    Argumentos:
        - numTiendas (int):         Número total de tiendas.
        - numBebidas (int):         Número de bebidas.
        - tipos (list[str]):        Lista con el tipo de cada tienda.
        - precioBase (list[float]): Precio base de cada bebida.

    Devuelve:
        - list[list[Decimal]]: Precio de cada bebida por tienda.
'''
def generarPrecioBebida(numTiendas, numBebidas, tipos, precioBase):

    precioBebida = [[0 for b in range(numBebidas)] for i in range(numTiendas)]
    
    for i in range(1, numTiendas):
        for b in range(numBebidas):
            coste = str(precioBase[b] * (1 - tipoTienda(tipos[i])/2500))
            # Convertimos el valor para que tenga exactamente dos decimales y poder trabajar con él
            precioBebida[i][b] = Decimal(coste).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return precioBebida




'''
    Ajusta la demanda diaria de las tiendas, durante los primeros días afectados por el retraso
    en la entrega de pedidos, en el caso de que sea mayor que el stock disponible.

    Argumentos:
        - demandaTienda (list[list[list[list[int]]]]): Demanda diaria por escenario, día, tienda y bebida.
        - stockInicial (list[list[list[int]]]):        Stock inicial por escenario, tienda y bebida.
        - pedidosPendientes (list[list[list[int]]]):   Pedidos pendientes de entrega por día, tienda y bebida.
        - retrasoEntrega (int):                        Número de días de retraso en la entrega de pedidos.
        - numEscenarios (int):                         Número de escenarios simulados.
        - numTiendas (int):                            Número total de tiendas.
        - numBebidas (int):                            Número total de tipos de bebida.

    Devuelve:
        - list[list[list[list[int]]]]: Demanda ajustada por escenario, día, tienda y bebida.
'''
def ajustarDemanda(demandaTienda, stockInicial, pedidosPendientes, retrasoEntrega, numEscenarios, numTiendas, numBebidas):

    for e in range(numEscenarios):
        for i in range(1, numTiendas):
            for b in range(numBebidas):
                
                stockDisponible = stockInicial[e][i][b]
    
                # Ajustar la demanda de los días afectados por el retraso en la entrega
                for r in range(retrasoEntrega):
    
                    # Añadimos los pedidos pendientes de ser entregados en el día correspondiente
                    if r > 0:
                        stockDisponible += pedidosPendientes[r][i][b]
    
                    # Limitamos la demanda según el stock disponible
                    demandaTienda[e][r][i][b] = min(demandaTienda[e][r][i][b], stockDisponible)
    
                    # Eliminamos las unidades vendidas
                    stockDisponible -= demandaTienda[e][r][i][b]
    
    return demandaTienda




######################################## FUNCIONES AUXILIARES #########################################

'''
    Comprueba si se trata o no de una variable de decisión de Gurobi del
    problema de optimización y devuelve su valor numérico como entero.

    Argumentos:
        - var: Variable cuyo valor debe obtenerse. Puede ser:
              + Una variable de Gurobi (gurobi.Var)
              + Un número (int | float)

    Devuelve:
        - int: Valor numérico de la variable.
'''
def valor(var):
    
    try:
        return int(var.X)  # Si es una variable de Gurobi
    except AttributeError:
        return int(var)  # Si no lo es




'''
    Convierte un tupledict de Gurobi en un diccionario "normal".
    Si un índice no existe en dictGurobi, se le asigna un valor inicial.
    
    Argumentos:
        - dictGurobi (gurobipy.tupledict):   Diccionario que almacena las variables de Gurobi.
        - indices (iterable[tuple]):         Conjunto completo de índices de la variable de Gurobi.
        - valorInicial (callable, opcional): Valor inicial que se asignará al diccionario que contiene las variables de Gurobi.
    
    Devuelve:
        - diccionario (dict[tuple, Any]): Diccionario "normal" que contiene las variables de Gurobi y, si era necesario, los valores iniciales añadidos.
'''
def convertirDiccionario(dictGurobi, indices=None, valorInicial=None):
    
    if indices is None:  # Si no se han indicado los índices del tupledict...
        return dict(dictGurobi)  # Devolvemos la conversión a diccionario "normal"
    
    # Creamos el diccionario "normal"
    diccionario = {}

    for idx in indices:
        if idx in dictGurobi:  # Si los índices ya tienen un valor asignado...
            diccionario[idx] = dictGurobi[idx]  # Nos quedamos con ese valor
        else:  # Si los índices no tienen un valor asignado...
            if callable(valorInicial):  # Si el valor inicial depende de los índices...
                diccionario[idx] = valorInicial(*idx)  # Asignamos el valor que corresponde a dichos índices
            else:  # Si el valor inicial es una constante...
                diccionario[idx] = valorInicial  # Asignamos dicho valor

    return diccionario  # Devolvemos el diccionario "normal"




################################### FUNCIONES MODELOS ALTERNATIVOS ####################################

'''
    Genera simultáneamente las variables de visitas V[c,d,i] y las variables de ruta X[c,d,i,j]
    a partir de una secuencia de visitas de tiendas previamente construida para cada comerciante.
    
    Argumentos:
        - numComerciantes (int):                      Número de comerciantes disponibles.
        - numDias (int):                              Número total de días de simulación.
        - numTiendas (int):                           Número total de tiendas (incluyendo oficina como nodo 0).
        - distanciaRutas (list[list[float]]):         Matriz de distancias entre ubicaciones.
        - tiempoRutas (list[list[float]]):            Matriz de tiempos entre ubicaciones.
        - distanciaMax (float):                       Distancia máxima permitida por jornada.
        - tiempoMax (float):                          Tiempo máximo permitido por jornada.
        - tiempoVisita (float):                       Tiempo de permanencia en cada tienda.
        - secuencias (dict[int,dict[int,list[int]]]): Diccionario que contiene el orden de visitas de las tiendas.
    
    Devuelve:
        - V (dict[tuple[int,int,int], int]):     Variables binarias de visita a tiendas por comerciante, día y tienda.
        - X (dict[tuple[int,int,int,int], int]): Variables binarias de las rutas empleadas por comerciante y día.
'''
def generarVisitasRutas(numComerciantes, numDias, numTiendas, distanciaRutas, tiempoRutas, distanciaMax, tiempoMax, tiempoVisita, secuencias):
    
    # Inicializamos las visitas y las rutas
    V = {(c,d,i): 0 for c in range(numComerciantes) for d in range(numDias) for i in range(1, numTiendas)}
    X = {(c,d,i,j): 0 for c in range(numComerciantes) for d in range(numDias) for i in range(numTiendas) for j in range(numTiendas) if i != j}
    
    # Solo recorremos los días que tienen secuencias de visitas
    for d, listaTiendas in secuencias.items():

        tiendasPendientes = list(listaTiendas)
        
        # Construimos las rutas de los comerciantes
        for c in range(numComerciantes):

            distanciaAcumulada = 0
            tiempoAcumulado = 0

            tiendaAnterior = 0

            tiendasRuta = []

            # Añadimos tiendas mientras la ruta siga siendo factible
            while len(tiendasPendientes) > 0:

                # Seleccionamos la siguiente tienda a visitar
                tiendaActual = tiendasPendientes[0]
                                
                # Comprobamos que la ruta sigue siendo válida
                distanciaExtra = (distanciaRutas[tiendaAnterior][tiendaActual] + distanciaRutas[tiendaActual][0])
                tiempoExtra = (tiempoRutas[tiendaAnterior][tiendaActual] + tiempoRutas[tiendaActual][0] + tiempoVisita)

                # Si no cabe una tienda más, terminamos la ruta
                if distanciaAcumulada + distanciaExtra > distanciaMax or tiempoAcumulado + tiempoExtra > tiempoMax:
                    break

                # Asignamos la visita a la tienda
                V[c,d,tiendaActual] = 1
                tiendasRuta.append(tiendaActual)

                distanciaAcumulada += distanciaRutas[tiendaAnterior][tiendaActual]
                tiempoAcumulado += tiempoRutas[tiendaAnterior][tiendaActual] + tiempoVisita

                tiendaAnterior = tiendaActual

                # Eliminamos la tienda ya asignada
                tiendasPendientes.pop(0)
                
            # Construimos las rutas en función de las visitas asignadas
            if len(tiendasRuta) == 0:
                continue

            # Ruta entre la oficina y la primera tienda
            X[c,d,0,tiendasRuta[0]] = 1

            # Rutas entre las tiendas intermedias
            for i in range(len(tiendasRuta) - 1):

                X[c,d,tiendasRuta[i],tiendasRuta[i+1]] = 1

            # Ruta entre la última tienda y la oficina
            X[c,d,tiendasRuta[-1],0] = 1

        # Si quedan tiendas sin asignar, no existe solución factible
        if len(tiendasPendientes) > 0:
            return None, None
        
    return V, X




###################################### MENSAJES DE LA SIMULACIÓN ######################################

'''
    Muestra el inicio de una nueva simulación del modelo para un número
    concreto de comerciantes.

    Argumentos:
        - numComerciantes (int): Número de comerciantes de la simulación.
'''
def inicioSimulacion(numComerciantes):
    
    com = "comerciante" if numComerciantes == 1 else "comerciantes"
    print(f"\n  **** Simulando con {numComerciantes} {com} ****\n")




'''
    Muestra el estado de resolución del solver.

    Argumentos:
        - estado (str):          Estado del solver.
        - numComerciantes (int): Número de comerciantes.
'''
def estadoSolver(estado, numComerciantes):

    com = "comerciante" if numComerciantes == 1 else "comerciantes"

    mensajes = {
        "OPTIMO": "\n **** Se encontró la solución óptima con",
        "FACTIBLE": "\n **** Se encontró una solución válida con",
        "INFACTIBLE": "\n **** El modelo no es factible para",
        "SIN_SOLUCION": "\n **** No se encontró una solución con"
    }

    print(f"{mensajes[estado]} {numComerciantes} {com} ****\n")




'''
    Muestra un mensaje indicando el inicio del cálculo del IIS (Irreducible Infeasible Set).

'''
def calculandoIIS():

    print("\n  **** Calculando IIS... ****\n\n")




'''
    Muestra un mensaje indicando que se ha alcanzado el número máximo
    de comerciantes permitido sin encontrar solución.

'''
def maximoComerciantes():

    print("\n **** Se ha alcanzado el máximo de comerciantes. Terminando ejecución... ****")




'''
    Muestra un mensaje indicando que una iteración MPC
    no encontró solución factible.

    Argumentos:
        - dia (int): Índice del día de la iteración MPC.
'''
def iteracionMPCSinSolucion(dia):

    print(f"\n **** Iteración Día {dia+1} sin solución. Parando MPC... ****")




'''
    Muestra el tiempo total de simulación de un modelo.

    Argumentos:
        - tiempo (timedelta): Tiempo total de ejecución.

        - tipo (str, opcional): Tipo de simulación.
'''
def tiempoSimulacion(tiempo, tipo="SIMPLE"):

    mensajes = {
        "SIMPLE": f"\n ⏱ Tiempo total de la optimización del modelo: {tiempo}\n",
        "MPC": f"\n   ⏱ Tiempo total de la optimización del modelo MPC: {tiempo}\n"
    }

    print(mensajes[tipo])




'''
    Muestra una línea horizontal de separación.

    Argumentos:
        - simbolo (str): Carácter utilizado.
'''
def separador(simbolo="-"):

    ancho = shutil.get_terminal_size().columns // len(simbolo)
    print("\n" + simbolo * ancho)




###################################### FINALIZACIÓN DEL PROGRAMA ######################################

'''
    Finaliza la ejecución del programa.
'''
def finalizarEjecucion():

    sys.exit()  # Cerramos la ejecución del programa