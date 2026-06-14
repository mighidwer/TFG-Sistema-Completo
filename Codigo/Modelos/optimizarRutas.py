# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · optimizarRutas.py

    Este fichero implementa el modelo matemático de optimización de rutas de operadores.
    Se encarga de construir el problema, definir variables de decisión, restricciones
    y función objetivo. Tras esto, resuelve el modelo mediante Gurobi.
    
"""

# Importación de librerías estándar
from datetime import datetime, timedelta

# Importación de dependencias externas
import gurobipy

# Importación de módulos propios del proyecto
from Modelos import solver, postprocesado, herramientasModelo



'''
    Construye el modelo matemático de optimización mediante Gurobi, definiendo las variables
    de decisión, restricciones y función objetivo del problema. Tras esto, ejecuta el solver
    y devuelve las variables y parámetros de la solución obtenida.

    Argumentos:
        - datos (dict[str, Any]):              Diccionario con la configuración completa del problema y los datos necesarios para la simulación.
        - numComerciantesFijo (int, opcional): Indica el número de comerciantes encontrado en la primera iteración de la optimización MPC.
        - diaIteracionMPC (int):               Día de la iteración actual de la simulación MPC.

    Devuelve:
        - resultados (dict[str, Any]): Diccionario con las variables de decisión y los parámetros obtenidos tras la optimización del modelo.
'''
def ejecutar(datos, numComerciantesFijo=None, diaIteracionMPC=0):
       
    # Instante inicial de la optimización del modelo
    start = datetime.now()

    
#######################################################################################################
######################################### DATOS DEL PROBLEMA ##########################################
#######################################################################################################
    
############################ INFORMACIÓN BÁSICA Y DIMENSIONES DEL PROBLEMA ############################
    
    dimensiones = datos["dimensiones"]
    
##### NÚMERO TOTAL DE TIENDAS #####
    
    numTiendasReal = dimensiones["numTiendasReal"]
    
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

    pedidoMinimo = logistica["pedidoMinimo"]

##### RETRASO EN LA ENTREGA DE PEDIDOS #####

    retrasoEntrega = logistica["retrasoEntrega"]

##### PEDIDOS PENDIENTES DE ENTREGA (MPC) #####

    pedidosPendientes = logistica["pedidosPendientes"]

##### MÁXIMO DE DÍAS CONSECUTIVOS DE TRABAJO #####

    maxDiasConsecutivos = logistica["maxDiasConsecutivos"]

##### DESCANSO OBLIGATORIO (MPC) #####

    descansoObligatorio = logistica["descansoObligatorio"]
    

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
        
    ##### TIENDAS VISITADAS #####

        # Creamos todas las variables V
        V = model.addVars(numComerciantes, numDias, range(1, numTiendas), vtype=gurobipy.GRB.BINARY, name="V")
        
        # Convertimos el tupledict de Gurobi a un diccionario "normal"
        V = herramientasModelo.convertirDiccionario(V)

    ##### CAMINOS ENTRE TIENDAS #####

        # Creamos todas las variables X
        X = model.addVars(((c,d,i,j) for c in range(numComerciantes) for d in range(numDias) for i in range(numTiendas) for j in range(numTiendas) if i != j),
                          vtype=gurobipy.GRB.BINARY, name="X")
        
        # Convertimos el tupledict de Gurobi a un diccionario "normal"
        X = herramientasModelo.convertirDiccionario(X)

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

        # Creamos los índices para la variable L
        indicesL = [(c, d) for c in range(numComerciantes) for d in range(numDias)]
        
        # Creamos todas las variables L (salvo para los comerciantes obligados a descansar el primer día)
        L = model.addVars([(c,d) for (c,d) in indicesL if not (d == 0 and descansoObligatorio.get(c,False))], vtype=gurobipy.GRB.BINARY, name="L")
        
        # Convertimos el tupledict de Gurobi a un diccionario "normal" y añadimos los valores iniciales para los comerciantes obligados a descansar
        L = herramientasModelo.convertirDiccionario(L, indicesL, valorInicial=lambda c,d: 0 if (d == 0 and descansoObligatorio.get(c,False)) else None)


################################# IMPLEMENTACIÓN DE LAS RESTRICCIONES #################################
    
########## BLOQUE 1 - DOMINIO Y ESTRUCTURA DEL ROUTING ##########
    
    ##### MÁXIMO UNA VISITA AL DÍA A CADA TIENDA #####
    
        for d in range(numDias):
            for i in range(1, numTiendas):
                visitas = gurobipy.quicksum(V[c,d,i] for c in range(numComerciantes))
                
                model.addConstr(visitas <= 1, name=f"UnaSolaVisita_d{d}_i{i}")

    ##### GRADO DE VISITA Y CONTINUIDAD DE LA RUTA #####

        for c in range(numComerciantes):
            for d in range(numDias):
                for k in range(1, numTiendas):
                    entradaTienda = gurobipy.quicksum(X[c,d,i,k] for i in range(numTiendas) if i != k)
                    salidaTienda = gurobipy.quicksum(X[c,d,k,j] for j in range(numTiendas) if j != k)
                    
                    model.addConstr(entradaTienda == V[c,d,k], name=f"EntradaTienda_c{c}_d{d}_i{k}")
                    model.addConstr(salidaTienda == V[c,d,k], name=f"SalidaTienda_c{c}_d{d}_i{k}")
        
    ##### INICIO Y FINAL DE LA RUTA EN LA OFICINA #####
        
        for c in range(numComerciantes):
            for d in range(numDias):
                entradaOficina = gurobipy.quicksum(X[c,d,i,0] for i in range(1, numTiendas))
                salidaOficina = gurobipy.quicksum(X[c,d,0,j] for j in range(1, numTiendas))
    
                model.addConstr(entradaOficina == L[c,d], name=f"EntradaOficina_c{c}_d{d}")
                model.addConstr(salidaOficina == L[c,d], name=f"SalidaOficina_c{c}_d{d}")
                
    ##### ELIMINACIÓN DE SUBRUTAS (Miller–Tucker–Zemlin, MTZ) #####
        
        # Creamos una variable auxiliar para calcular las rutas, definirá el orden de visita de las tiendas
        o = model.addVars(numComerciantes, numDias, numTiendas, vtype=gurobipy.GRB.CONTINUOUS, lb=0, ub=numTiendasReal-1, name="o")
        
        for c in range(numComerciantes):
            for d in range(numDias):
                for i in range(1, numTiendas):
                    for j in range(1, numTiendas):
                        if i != j:
                            model.addConstr(o[c,d,i] - o[c,d,j] + numTiendasReal * X[c,d,i,j] <= numTiendasReal-1, name=f"MTZ_c{c}_d{d}_i{i}_j{j}")

########## BLOQUE 2 - CALENDARIO LABORAL ##########

    ##### DÍAS DE DESCANSO #####
    
        for c in range(numComerciantes):
            for d in range(numDias):
                visitas = gurobipy.quicksum(V[c,d,i] for i in range(1, numTiendas))
                
                model.addConstr(visitas <= L[c,d] * numTiendasReal, name=f"DiasDeDescanso_c{c}_d{d}")
        
    ##### LÍMITE DE DÍAS CONSECUTIVOS TRABAJADOS #####
    
        for c in range(numComerciantes):
            for d in range(numDias - maxDiasConsecutivos):
                diasTrabajadosVentana = gurobipy.quicksum(L[c,d+tau] for tau in range(maxDiasConsecutivos+1))
                
                model.addConstr(diasTrabajadosVentana <= maxDiasConsecutivos, name=f"DiasConsecutivosTrabajados_c{c}_d{d}")
                
########## BLOQUE 3 - RECURSOS DIARIOS ##########

    ##### LÍMITE DE DISTANCIA DIARIA #####
        
        distanciaTotal = [[0 for d in range(numDias)] for c in range(numComerciantes)]
        
        for c in range(numComerciantes):
            for d in range(numDias):
                distanciaTotal[c][d] = gurobipy.quicksum(distanciaRutas[i][j] * X[c,d,i,j] for i in range(numTiendas) for j in range(numTiendas) if i != j)
                
                model.addConstr(distanciaTotal[c][d] <= distanciaMax, name=f"DistanciaTotal_c{c}_d{d}")
        
    ##### LÍMITE DE TIEMPO DIARIO #####
        
        tiempoTotal = [[0 for d in range(numDias)] for c in range(numComerciantes)]
        
        for c in range(numComerciantes):
            for d in range(numDias):
                tiempoDesplazamiento = gurobipy.quicksum(tiempoRutas[i][j] * X[c,d,i,j] for i in range(numTiendas) for j in range(numTiendas) if i != j)
                numeroVisitas = gurobipy.quicksum(V[c,d,i] for i in range(1, numTiendas))
                tiempoTiendas = tiempoVisita * numeroVisitas
                tiempoTotal[c][d] = tiempoDesplazamiento + tiempoTiendas
                
                model.addConstr(tiempoTotal[c][d] <= tiempoMax, name=f"TiempoTotal_c{c}_d{d}")
                
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


############################################### RETURN ################################################

    return postprocesado.construirSalida(model, tiempoSimulacionTotal, numComerciantes, demandaTienda, variables={"V": V, "X": X, "S": S, "U": U, "L": L})