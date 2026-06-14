# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · horizonteDeslizante.py

    Este fichero implementa una estrategia MPC (Model Predictive Control)
    mediante horizonte deslizante para reoptimizar dinámicamente las rutas
    de reparto y la planificación logística a lo largo del horizonte temporal.

    En cada iteración del MPC:
        1. Se resuelve el problema completo de optimización.
        2. Se conservan únicamente las decisiones correspondientes al primer día.
        3. Se actualiza el estado del sistema utilizando los resultados obtenidos:
            - Stock de las tiendas
            - Pedidos pendientes
            - Demanda simulada
        4. Se desplaza el horizonte temporal un día hacia adelante.
        5. Se vuelve a resolver el modelo desde el nuevo estado actualizado.

    Además, durante cada iteración:
        - Se generan nuevos escenarios de demanda.
        - Se actualiza la cola FIFO de pedidos pendientes según el retraso
          de entrega configurado.
        - Se ajustan automáticamente los pedidos pendientes para evitar
          sobrealmacenamiento en las tiendas, respetando la capacidad máxima
          agregada de cada una.
        - Se almacenan de forma acumulada las variables de decisión obtenidas
          en todas las iteraciones de la simulación MPC.

    De esta forma, el sistema se adapta continuamente a la evolución de la
    demanda y del stock disponible utilizando siempre la información más
    reciente del sistema.
    
"""

# Importación de librerías estándar
from datetime import datetime, timedelta

# Importación de módulos propios del proyecto
from Modelos import herramientasModelo
import presentacion



'''
    Ejecuta una simulación MPC mediante horizonte deslizante.
    
    Para cada iteración:
        - Se resuelve el modelo completo de optimización.
        - Se almacenan únicamente los resultados correspondientes al primer día.
        - Se actualiza el stock inicial de las tiendas.
        - Se vuelve a resolver el problema desde el nuevo estado.
    
    Argumentos:
        - config (dict[str, Any]): Configuración general del problema.
        - modelo (module):         Módulo del modelo de optimización a utilizar. Debe implementar la función ejecutar(config).
    
    Devuelve:
        - resultadosMPC (dict[str, Any]): Diccionario con los resultados agregados de toda la simulación MPC.
'''
def ejecutar(config, modelo):
    
    # Instante inicial de la optimización del modelo
    start = datetime.now()
    

#######################################################################################################
######################################### DATOS DEL PROBLEMA ##########################################
#######################################################################################################
    
############################ INFORMACIÓN BÁSICA Y DIMENSIONES DEL PROBLEMA ############################
    
    dimensiones = config["dimensiones"]

##### INFORMACIÓN DE LAS TIENDAS #####
    
    tipos = dimensiones["tipos"]
    
##### NÚMERO TOTAL DE TIENDAS #####
    
    numTiendas = dimensiones["numTiendas"]

##### NÚMERO DE DÍAS #####
    
    numDiasReal = dimensiones["numDiasReal"]
    
    numDias = dimensiones["numDias"]

##### NÚMERO DE TIPOS DE BEBIDA #####
    
    numBebidas = dimensiones["numBebidas"]

##### NÚMERO DE ESCENARIOS A SIMULAR #####

    numEscenarios = dimensiones["numEscenarios"]


################################# RESTRICCIONES DE VISITAS Y ENTREGAS #################################

    logistica = config["logistica"]

##### RETRASO EN LA ENTREGA DE PEDIDOS #####

    retrasoEntrega = logistica["retrasoEntrega"]

##### MÁXIMO DE DÍAS CONSECUTIVOS DE TRABAJO #####

    maxDiasConsecutivos = logistica["maxDiasConsecutivos"]


################################# INFORMACIÓN SEGÚN EL TIPO DE TIENDA #################################
    
    tiendas = config["tiendas"]

##### CAPACIDAD DE LAS TIENDAS #####

    capacidadTienda = tiendas["capacidadTienda"]


    
#######################################################################################################
######################################## ALMACENAMIENTO GLOBAL ########################################
#######################################################################################################
    
    # Variables agregadas finales de toda la simulación MPC
    V_MPC = {}
    X_MPC = {}
    S_MPC = {}
    U_MPC = {}
    L_MPC = {}
    
    # Demanda diaria de cada iteración de la simulación MPC
    demandaTienda_MPC = [[[[0 for b in range(numBebidas)] for i in range(numTiendas)] for d in range(numDiasReal)] for e in range(numEscenarios)]
    
    
    
#######################################################################################################
######################################## HORIZONTE DESLIZANTE #########################################
#######################################################################################################
    
    numComerciantesFijo = None
    
    for d in range(numDiasReal):
    
        presentacion.encabezadoSeccion(f"ITERACIÓN MPC - DÍA {d+1}")
    
    
########################################## OPTIMIZACIÓN ###############################################
                
        # Ejecutamos el modelo completo
        resultados = modelo.ejecutar(config, numComerciantesFijo, d)

        if resultados is None:  # Si no obtenemos ningún resultado...
            
            herramientasModelo.iteracionMPCSinSolucion(d)
            herramientasModelo.finalizarEjecucion()
        
        
####################################### DATOS DE LA SIMULACIÓN ########################################

        datosSimulacion = resultados["datosSimulacion"]
    
##### NÚMERO DE COMERCIANTES #####

        numComerciantes = datosSimulacion["numComerciantes"]

##### DEMANDA DIARIA DE LAS TIENDAS #####

        demandaTienda = datosSimulacion["demandaTienda"]
        
        
########################################## DATOS DEL MODELO ###########################################

        datosModelo = resultados["datosModelo"]

##### NÚMERO DE VARIABLES #####

        numVariables = datosModelo["numVariables"]

##### NÚMERO DE RESTRICCIONES #####

        numRestricciones = datosModelo["numRestricciones"]


######################################## VARIABLES DE DECISIÓN ########################################

        variables = resultados["variablesDecision"]

##### TIENDAS VISITADAS #####

        V = variables["V"]

##### CAMINOS ENTRE TIENDAS #####

        X = variables["X"]

##### STOCK DE LAS TIENDAS #####

        S = variables["S"]

##### UNIDADES ENTREGADAS #####

        U = variables["U"]

##### DÍAS LABORALES #####

        L = variables["L"]
    

##################################### NÚMERO DE COMERCIANTES FIJO #####################################
    
        # Tras la primera iteración, fijamos el número de comerciantes
        if numComerciantesFijo is None:
        
            numComerciantesFijo = numComerciantes

            diasConsecutivos = {c: 0 for c in range(numComerciantes)}
            config["logistica"]["descansoObligatorio"] = {c: False for c in range(numComerciantes)}


#######################################################################################################
##################################### REGISTRO DE LOS RESULTADOS ######################################
#######################################################################################################

###################################### GENERACIÓN NUEVA DEMANDA #######################################

        config["tiendas"]["demandaTienda"] = herramientasModelo.generarDemandaTienda(numEscenarios, numTiendas, numBebidas, numDias, tipos)


########################################## TIENDAS VISITADAS ##########################################

        for c in range(numComerciantes):
            for i in range(1, numTiendas):
                # Guardamos el día actual de la simulación MPC
                V_MPC[c,d,i] = V[c,0,i]
    
    
######################################## CAMINOS ENTRE TIENDAS ########################################

        for c in range(numComerciantes):
            for i in range(numTiendas):
                for j in range(numTiendas):
                    if i != j:
                        # Guardamos el día actual de la simulación MPC
                        X_MPC[c,d,i,j] = X[c,0,i,j]


################################## ACTUALIZACIÓN PEDIDOS PENDIENTES ###################################

        for i in range(1, numTiendas):
            for b in range(numBebidas):

                # Desplazamos la cola
                for r in range(retrasoEntrega-1):

                    config["logistica"]["pedidosPendientes"][r][i][b] = config["logistica"]["pedidosPendientes"][r+1][i][b]

                # Añadimos el nuevo pedido al final de la cola FIFO
                config["logistica"]["pedidosPendientes"][retrasoEntrega-1][i][b] = U[retrasoEntrega,i,b]


###################################### AJUSTE PEDIDOS PENDIENTES ######################################

        for i in range(1, numTiendas):
            
            # Stock de cada escenario por bebidas
            stockEscenario = [[S[e,1,i,b] for b in range(numBebidas)] for e in range(numEscenarios)]

            for r in range(retrasoEntrega):

                # Stock total
                stockAgregado = [sum(stockEscenario[e]) for e in range(numEscenarios)]
                
                # Calculamos el espacio disponible en el escenario más restrictivo
                espacioDisponibleMinimo = min(capacidadTienda[i] - stockAgregado[e] for e in range(numEscenarios))
                
                # Pedido total pendiente del día r
                pedidoTotal = sum(config["logistica"]["pedidosPendientes"][r][i][b] for b in range(numBebidas))
                
                # Factor de ajuste
                factor = (min(1, espacioDisponibleMinimo / pedidoTotal) if pedidoTotal > 0 else 0)
                
                # Si el pedido es mayor que el espacio disponible (factor < 1), lo ajustamos proporcionalmente
                for b in range(numBebidas):
                    config["logistica"]["pedidosPendientes"][r][i][b] = int(config["logistica"]["pedidosPendientes"][r][i][b] * factor)
        
                # Actualizamos el stock de cada escenario por bebidas para el día siguiente
                for e in range(numEscenarios):
                    for b in range(numBebidas):
                
                        entregaBebida = config["logistica"]["pedidosPendientes"][r][i][b]
                        demandaBebida = config["tiendas"]["demandaTienda"][e][r+1][i][b]
                
                        stockEscenario[e][b] = max(0, stockEscenario[e][b] + entregaBebida - demandaBebida)


######################################### UNIDADES ENTREGADAS #########################################
        
        for i in range(1, numTiendas):
            for b in range(numBebidas):
                
                if d == 0:
                    # Día inicial sin entregas
                    U_MPC[d,i,b] = 0
                
                # Guardamos los pedidos que se entregarán el primer día de la siguiente iteración
                U_MPC[d+1,i,b] = config["logistica"]["pedidosPendientes"][0][i][b]


################################################ STOCK ################################################

        for e in range(numEscenarios):
            for i in range(1, numTiendas):
                for b in range(numBebidas):

                    if d == 0:
                        # Guardamos el stock inicial de la primera iteración
                        S_MPC[e,d,i,b] = S[e,0,i,b]

                    else:
                        # Calculamos el stock inicial de las siguientes iteraciones
                        S_MPC[e,d,i,b] = S_MPC[e,d-1,i,b] + U_MPC[d-1,i,b] - demandaTienda_MPC[e][d-1][i][b]

    
########################################### DÍAS LABORALES ############################################

        for c in range(numComerciantes):
            # Guardamos el día actual de la simulación MPC
            L_MPC[c,d] = L[c,0]
            
            # Almacenamos los días consecutivos de trabajo de cada comerciante
            if L[c,0] == 1:
                diasConsecutivos[c] += 1
            else:
                diasConsecutivos[c] = 0
            
            # Si llega al máximo de días consecutivos, forzamos descanso al día siguiente
            if diasConsecutivos[c] >= maxDiasConsecutivos:
                config["logistica"]["descansoObligatorio"][c] = True
                diasConsecutivos[c] = 0
            else:
                config["logistica"]["descansoObligatorio"][c] = False
            
       
########################################### DEMANDA DIARIA ############################################

        for e in range(numEscenarios):
            for i in range(1, numTiendas):
                for b in range(numBebidas):
                    # Guardamos el valor de la demanda real (ajustado por el modelo) del día actual de la simulación MPC
                    demandaTienda_MPC[e][d][i][b] = demandaTienda[e][0][i][b]


##################################### ACTUALIZACIÓN STOCK INICIAL #####################################
        
        for e in range(numEscenarios):
            for i in range(1, numTiendas):
                for b in range(numBebidas):
                    # Actualizamos el stock inicial para la siguiente iteración
                    config["tiendas"]["stockInicial"][e][i][b] = S[e,0,i,b] + config["logistica"]["pedidosPendientes"][0][i][b] - demandaTienda_MPC[e][d][i][b]



#######################################################################################################
############################################# RESOLUCIÓN ##############################################
#######################################################################################################

############################################ TIEMPO TOTAL #############################################
    
    # Instante final de la optimización del modelo
    end = datetime.now()
    
    # Calculamos el tiempo de simulación total
    tiempoSimulacionTotal = timedelta(seconds=round((end - start).total_seconds()))
    
    # Mostramos el tiempo total de la simulación MPC
    herramientasModelo.tiempoSimulacion(tiempoSimulacionTotal, "MPC")
    
    
    
#######################################################################################################
############################################### RETURN ################################################
#######################################################################################################
    
    return {
    
        ##### DATOS DE LA SIMULACIÓN #####
    
        "datosSimulacion": {
            "numComerciantes": numComerciantes,
            "demandaTienda": demandaTienda_MPC,
            "tiempoSimulacionTotal": tiempoSimulacionTotal
        },
        
        ##### DATOS DEL MODELO #####
        
        "datosModelo": {
            "numVariables": numVariables,
            "numRestricciones": numRestricciones
        },
            
        ##### VARIABLES DE DECISIÓN #####
    
        "variablesDecision": {
    
            "V": V_MPC,
            "X": X_MPC,
            "S": S_MPC,
            "U": U_MPC,
            "L": L_MPC
        }
    }