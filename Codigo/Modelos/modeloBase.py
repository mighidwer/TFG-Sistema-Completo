# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · modeloBase.py

    Este fichero implementa la parte común de los modelos alternativos desarrollados.
    
"""

# Importación de librerías estándar
from datetime import datetime, timedelta

# Importación de dependencias externas
import gurobipy

# Importación de módulos propios del proyecto
from Modelos import solver, postprocesado, herramientasModelo



'''
    Implementa la parte común de los modelos alternativos de optimización de rutas.
    Construye el modelo matemático, define las variables de decisión, restricciones
    y función objetivo, ejecuta el solver y devuelve las variables y parámetros de
    la solución obtenida.

    Argumentos:
        - datos (dict[str, Any]):              Diccionario con la configuración completa del problema y los datos necesarios para la simulación.
        - generarVisitasRutas (Callable):      Función encargada de generar las variables prefijadas de visitas y rutas para un número determinado de comerciantes.
        - numComerciantesFijo (int, opcional): Indica el número de comerciantes encontrado en la primera iteración de la optimización MPC.
        - diaIteracionMPC (int):               Día de la iteración actual de la simulación MPC.

    Devuelve:
        - resultados (dict[str, Any]): Diccionario con las variables de decisión y los parámetros obtenidos tras la optimización del modelo.
'''
def ejecutar(datos, generarVisitasRutas, numComerciantesFijo=None, diaIteracionMPC=0):
       
    # Instante inicial de la optimización del modelo
    start = datetime.now()

    
#######################################################################################################
######################################### DATOS DEL PROBLEMA ##########################################
#######################################################################################################
    
############################ INFORMACIÓN BÁSICA Y DIMENSIONES DEL PROBLEMA ############################
    
    dimensiones = datos["dimensiones"]
    
##### NÚMERO TOTAL DE TIENDAS #####
    
    numTiendas = dimensiones["numTiendas"]

##### NÚMERO DE DÍAS #####
    
    numDiasReal = dimensiones["numDiasReal"]
    
    numDias = dimensiones["numDias"]

##### NÚMERO DE TIPOS DE BEBIDA #####
    
    numBebidas = dimensiones["numBebidas"]

##### NÚMERO DE COMERCIANTES #####

    minNumComerciantes = dimensiones["minNumComerciantes"]
    
    maxNumComerciantes = dimensiones["maxNumComerciantes"]

##### NÚMERO DE ESCENARIOS A SIMULAR #####

    numEscenarios = dimensiones["numEscenarios"]


################################ MODO DE TRANSPORTE Y LÍMITES FÍSICOS #################################

    transporte = datos["transporte"]

##### DISTANCIA TOTAL MÁXIMA POR DÍA #####

    distanciaMax = transporte["distanciaMax"]

##### TIEMPO MÁXIMO DE TRABAJO POR JORNADA #####

    tiempoMax = transporte["tiempoMax"]


################################# RESTRICCIONES DE VISITAS Y ENTREGAS #################################

    logistica = datos["logistica"]

##### TIEMPO DE VISITA EN CADA TIENDA #####

    tiempoVisita = logistica["tiempoVisita"]

##### PEDIDO MÍNIMO #####   

    pedidoMinimo = 0  # Al tener rutas prefijadas, no podemos obligar a hacer un pedido mínimo tras cada visita

##### RETRASO EN LA ENTREGA DE PEDIDOS #####

    retrasoEntrega = logistica["retrasoEntrega"]

##### PEDIDOS PENDIENTES DE ENTREGA (MPC) #####

    pedidosPendientes = logistica["pedidosPendientes"]

##### FRECUENCIA DE LAS VISITAS (MODELOS ALTERNATIVOS) #####

    frecuenciaVisita = logistica["frecuenciaVisita"]
    

################################ CONDICIONES COMERCIALES Y FINANCIERAS ################################
    
    costes = datos["costes"]

##### COSTE POR DÍA TRABAJADO DE LOS COMERCIANTES #####

    costeDia = costes["costeDia"]

##### COSTE POR HORA TRABAJADA DE LOS COMERCIANTES #####

    costeHora = costes["costeHora"]

##### COMISIÓN POR VENTAS #####

    comision = costes["comision"]


######################################### DATOS DE LAS RUTAS ##########################################
    
    datosRutas = datos["datosRutas"]

##### DISTANCIA TIENDA i - TIENDA j #####

    distanciaRutas = datosRutas["distanciaRutas"]

##### TIEMPO TIENDA i - TIENDA j #####

    tiempoRutas = datosRutas["tiempoRutas"]


################################# INFORMACIÓN SEGÚN EL TIPO DE TIENDA #################################
    
    tiendas = datos["tiendas"]

##### CAPACIDAD DE LAS TIENDAS #####

    capacidadTienda = tiendas["capacidadTienda"]

##### STOCK INICIAL DE LAS TIENDAS #####

    stockInicial = tiendas["stockInicial"]

##### DEMANDA MEDIA DIARIA DE LAS TIENDAS #####

    demandaTienda = tiendas["demandaTienda"]
    
##### PRECIO DE LA BEBIDA PARA CADA TIENDA #####

    precioBebida = tiendas["precioBebida"]


###################################### OPTIMIZACIÓN Y SIMULACIÓN ######################################
    
    optimizacion = datos["optimizacion"]

##### TIEMPO DE SIMULACIÓN #####

    tiempoSimulacion = optimizacion["tiempoSimulacion"]

##### TIEMPO DE ESPERA PARA ACTIVAR EL CONTROL DEL GAP #####

    tiempoGap = optimizacion["tiempoGap"]

##### MARGEN DE OPTIMALIDAD (GAP) #####

    gapMaximo = optimizacion["gapMaximo"]

##### PENALIZACIÓN STOCK SOBRANTE #####

    epsilon = optimizacion["epsilon"]

##### CÁLCULO IIS (Irreducible Infeasible Set) #####

    calculoIIS = optimizacion["calculoIIS"]


######################################## AJUSTE DE LA DEMANDA #########################################

    # Ajustamos la demanda en función del stock disponible
    demandaTienda = herramientasModelo.ajustarDemanda(demandaTienda, stockInicial, pedidosPendientes, retrasoEntrega, numEscenarios, numTiendas, numBebidas)



#######################################################################################################
########################################## MODELO MATEMÁTICO ##########################################
#######################################################################################################

    # Comprobamos si se ha fijado un número de comerciantes
    if numComerciantesFijo is not None:
        # Si se ha fijado, realizamos el proceso de optimización con ese valor fijo (Simulación MPC)
        rangoComerciantes = [numComerciantesFijo]
    
    else:
        # Si no se ha fijado, realizamos el proceso iterativo para encontrar el número mínimo de comerciantes necesarios
        rangoComerciantes = range(minNumComerciantes, maxNumComerciantes+1)


    for numComerciantes in rangoComerciantes:
        
        herramientasModelo.inicioSimulacion(numComerciantes)
        
        # Creamos el modelo
        model = gurobipy.Model(f"optimizacion_rutas_{numComerciantes}com")

    
###################################### DECLARACIÓN DE VARIABLES #######################################
        
    ##### TIENDAS VISITADAS - CAMINOS ENTRE TIENDAS #####
         
        # Obtenemos las visitas y las rutas preasignadas
        V, X = generarVisitasRutas(numComerciantes, numDias, numTiendas, distanciaRutas, tiempoRutas, distanciaMax, tiempoMax, tiempoVisita, frecuenciaVisita, diaIteracionMPC)
        
        if V is None or X is None:
            herramientasModelo.estadoSolver("SIN_SOLUCION", numComerciantes)
            
            herramientasModelo.separador()
            
            if numComerciantes == maxNumComerciantes:
                herramientasModelo.maximoComerciantes()
                herramientasModelo.finalizarEjecucion()  # Cerramos la ejecución del programa
                
            continue  # Pasamos a la siguiente iteración del número de comerciantes
        
    ##### STOCK DE LAS TIENDAS #####
    
        # Creamos los índices para la variable S
        indicesS = [(e,d,i,b) for e in range(numEscenarios) for d in range(numDias) for i in range(1, numTiendas) for b in range(numBebidas)]
        
        # Creamos todas las variables B (salvo para d=0)
        S = model.addVars([(e,d,i,b) for (e,d,i,b) in indicesS if d > 0], vtype=gurobipy.GRB.INTEGER, lb=0,
            ub={(e,d,i,b): capacidadTienda[i] for e in range(numEscenarios) for d in range(1, numDias) for i in range(1, numTiendas) for b in range(numBebidas)}, name="S")
        
        # Convertimos el tupledict de Gurobi a un diccionario "normal" y añadimos los valores para d=0
        S = herramientasModelo.convertirDiccionario(S, indicesS, valorInicial=lambda e,d,i,b: stockInicial[e][i][b] if d == 0 else None)

    ##### UNIDADES ENTREGADAS #####

        # Creamos los índices para la variable U
        indicesU = [(d,i,b) for d in range(numDias) for i in range(1, numTiendas) for b in range(numBebidas)]

        # Creamos todas las variables U (salvo para los días anteriores al retraso de entrega)
        U = model.addVars([(d,i,b) for (d,i,b) in indicesU if d >= retrasoEntrega], vtype=gurobipy.GRB.INTEGER, lb=0,
            ub={(d,i,b): capacidadTienda[i] for d in range(retrasoEntrega, numDias) for i in range(1, numTiendas) for b in range(numBebidas)}, name="U")

        # Convertimos el tupledict de Gurobi a un diccionario "normal" y añadimos los valores iniciales para los días sin entregas posibles
        U = herramientasModelo.convertirDiccionario(U, indicesU, valorInicial=lambda d,i,b: pedidosPendientes[d][i][b] if 1 <= d <= retrasoEntrega else 0)

    ##### DÍAS LABORALES #####
        
        # Creamos los índices para el parámetro U
        indicesL = [(c,d) for c in range(numComerciantes) for d in range(numDias)]

        L = {}

        for c in range(numComerciantes):
            for d in range(numDias):
                # Leemos las visitas (ya están programadas) para saber qué días son laborales
                visitas = sum(V[c,d,i] for i in range(1, numTiendas))
                L[c,d] = 1 if visitas > 0 else 0

        L = herramientasModelo.convertirDiccionario(L, indicesL, valorInicial=0)
        
    ##### TIEMPO DE TRABAJO (PREFIJADO) #####
        
        tiempoTotal = [[0 for d in range(numDias)] for c in range(numComerciantes)]
        
        # Calculamos el tiempo total de trabajo para las rutas prefijadas
        for c in range(numComerciantes):
            for d in range(numDias):
                tiempoRuta = sum(tiempoRutas[i][j] * X[c,d,i,j] for i in range(numTiendas) for j in range(numTiendas) if i != j)
                visitas = sum(V[c,d,i] for i in range(1, numTiendas))
                tiempoTotal[c][d] = tiempoRuta + visitas * tiempoVisita


################################# IMPLEMENTACIÓN DE LAS RESTRICCIONES #################################
                
########## BLOQUE 4 - LOGÍSTICA E INVENTARIO ##########
    
    ##### BALANCE DE STOCK DIARIO #####
        
        for e in range(numEscenarios):
            for d in range(numDias - 1):  # Hasta el penúltimo día
                for i in range(1, numTiendas):
                    for b in range(numBebidas):
                        stockHoy = S[e,d,i,b]
                        udsRecibidas = U[d,i,b]
                        stockManana = S[e,d+1,i,b]
                        
                        model.addConstr(stockManana == stockHoy + udsRecibidas - demandaTienda[e][d][i][b], name=f"StockMañana_e{e}_d{d+1}_i{i}_b{b}")

    ##### CAPACIDAD DE ALMACENAMIENTO #####
        
        for e in range(numEscenarios):
            for d in range(numDias):
                for i in range(1, numTiendas):
                    stockTotal = gurobipy.quicksum(S[e,d,i,b] for b in range(numBebidas))
                    entregasTotal = gurobipy.quicksum(U[d,i,b] for b in range(numBebidas))
                    
                    model.addConstr(stockTotal + entregasTotal <= capacidadTienda[i], name=f"Capacidad_e{e}_d{d}_i{i}")
                    
    ##### ENTREGAS CONDICIONADAS A VISITA PREVIA Y PEDIDO MÍNIMO #####

        for d in range(numDias - retrasoEntrega):
            for i in range(1, numTiendas):
                visita = gurobipy.quicksum(V[c,d,i] for c in range(numComerciantes))  # Si la tienda ha sido visitada este día, valdrá 1
                udsTotales = gurobipy.quicksum(U[d+retrasoEntrega,i,b] for b in range(numBebidas))

                model.addConstr(udsTotales <= visita * capacidadTienda[i], name=f"VisitaPrevia_d{d}_i{i}")
                model.addConstr(udsTotales >= visita * int(pedidoMinimo * capacidadTienda[i]), name=f"PedidoMinimo_d{d}_i{i}")

    
########################################## FUNCIÓN OBJETIVO ###########################################
            
    ##### MAX: UDS. VENDIDAS * PRECIO BEBIDAS - (DÍAS TRABAJADOS * SUELDO POR DÍA + HORAS TRABAJADAS * SUELDO POR HORA + COMISIÓN) #####

        # Ingresos totales por la venta de bebidas
        ingresosTotal = gurobipy.quicksum(U[d,i,b] * precioBebida[i][b] for d in range(retrasoEntrega, numDias) for i in range(1, numTiendas) for b in range(numBebidas))
        
        # Sueldo por día trabajado de los comerciantes
        sueldoDias = gurobipy.quicksum(L[c,d] * costeDia for c in range(numComerciantes) for d in range(numDias))
        
        # Sueldo por hora trabajada de los comerciantes
        sueldoHoras = sum(tiempoTotal[c][d] * costeHora for c in range(numComerciantes) for d in range(numDias))
        
        # Comisión total para los comerciantes
        comisionTotal = gurobipy.quicksum(U[d,i,b] * precioBebida[i][b] * comision for d in range(retrasoEntrega, numDias) for i in range(1, numTiendas) for b in range(numBebidas))
        
        # Penalización del stock sobrante en los días "ficticios"
        penalizacionStock = gurobipy.quicksum(S[e,d,i,b] for e in range(numEscenarios) for d in range(numDiasReal, numDias) for i in range(1, numTiendas) for b in range(numBebidas))
        
        # Sueldo total de los comerciantes
        sueldoComerciantes = sueldoDias + sueldoHoras + comisionTotal
        
        # Función objetivo: Maximizar beneficio neto
        model.setObjective(ingresosTotal - sueldoComerciantes - epsilon * penalizacionStock, gurobipy.GRB.MAXIMIZE)

    
    
#######################################################################################################
############################################# SIMULACIÓN ##############################################
#######################################################################################################

###################################### CONFIGURACIÓN DEL SOLVER #######################################
        
        configSolver = {"tiempoSimulacion": tiempoSimulacion, "tiempoGap": tiempoGap, "gapMaximo": gapMaximo, "calculoIIS": calculoIIS}
        

######################################## EJECUCIÓN DEL SOLVER #########################################
        
        model = solver.ejecutar(model, configSolver, numComerciantes)

        
########################################## ESTADO DEL SOLVER ##########################################
        
        if model.status == gurobipy.GRB.OPTIMAL:  # Encontramos la solución óptima para el número de comerciantes 
            break
        
        elif model.status in [gurobipy.GRB.TIME_LIMIT, gurobipy.GRB.INTERRUPTED] and model.SolCount > 0:  # Encontramos una solución válida tras el tiempo máximo de simulación
            break
        
        else:  # Si no la encontramos...
                        
            if model.status == gurobipy.GRB.INFEASIBLE:  # Si no existe ninguna solución factible...  
                
                if numComerciantesFijo is not None:  # Si estamos en una simulación MPC...
                    return None  # No devolvemos ningún resultado
            
            herramientasModelo.separador()
            
            if numComerciantes == maxNumComerciantes:  # Si hemos llegado al máximo de comerciantes sin encontrar solución...                
                herramientasModelo.maximoComerciantes()
                herramientasModelo.finalizarEjecucion()  # Cerramos la ejecución del programa
    


#######################################################################################################
############################################## SOLUCIÓN ###############################################
#######################################################################################################

############################################ TIEMPO TOTAL #############################################
    
    # Instante final de la optimización del modelo
    end = datetime.now()
    
    # Calculamos el tiempo de simulación total
    tiempoSimulacionTotal = timedelta(seconds=round((end - start).total_seconds()))
    
    # Mostramos el tiempo total de la simulación
    herramientasModelo.tiempoSimulacion(tiempoSimulacionTotal)
    
    return postprocesado.construirSalida(model, tiempoSimulacionTotal, numComerciantes, demandaTienda, variables={"V": V, "X": X, "S": S, "U": U, "L": L})