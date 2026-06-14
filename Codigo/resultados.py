# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · resultados.py

    Este fichero se encarga del cálculo y análisis de los resultados obtenidos tras
    la resolución del modelo de optimización.
    Incluye funciones para la visualización de resultados y navegación mediante
    menús interactivos.
    
"""

# Importación de librerías estándar
from decimal import Decimal, ROUND_HALF_UP

# Importación de módulos propios del proyecto
import presentacion
import solucion



'''
    A partir de las variables de decisión y la configuración del problema,
    calcula métricas reales asociadas a la simulación.

    Además, proporciona un menú interactivo para visualizar informes y
    presentaciones gráficas de la solución obtenida.

    Argumentos:
        - config (dict[str, Any]):     Configuración general del problema.
        - resultados (dict[str, Any]): Resultados obtenidos tras la optimización.
'''
def procesarResultados(datos, resultados):
    
#######################################################################################################
######################################### DATOS DEL PROBLEMA ##########################################
#######################################################################################################
    
############################ INFORMACIÓN BÁSICA Y DIMENSIONES DEL PROBLEMA ############################
    
    dimensiones = datos["dimensiones"]
    
##### INFORMACIÓN DE LAS TIENDAS #####
    
    nombres = dimensiones["nombres"]
    
    direcciones = dimensiones["direcciones"]
    
    latitudes = dimensiones["latitudes"]
    
    longitudes = dimensiones["longitudes"]
    
##### NÚMERO TOTAL DE TIENDAS #####
    
    numTiendasReal = dimensiones["numTiendasReal"]
    
    numTiendas = dimensiones["numTiendas"]

##### NÚMERO DE DÍAS #####
    
    numDiasReal = dimensiones["numDiasReal"]

##### NÚMERO DE TIPOS DE BEBIDA #####
    
    numBebidas = dimensiones["numBebidas"]

##### NÚMERO DE ESCENARIOS A SIMULAR #####

    numEscenarios = dimensiones["numEscenarios"]


################################ MODO DE TRANSPORTE Y LÍMITES FÍSICOS #################################

    transporte = datos["transporte"]

##### MODO DE DESPLAZAMIENTO #####
    
    modo = transporte["modo"]

##### DISTANCIA TOTAL MÁXIMA POR DÍA #####

    distanciaMax = transporte["distanciaMax"]

##### TIEMPO MÁXIMO DE TRABAJO POR JORNADA #####

    tiempoMax = transporte["tiempoMax"]


################################# RESTRICCIONES DE VISITAS Y ENTREGAS #################################

    logistica = datos["logistica"]

##### TIEMPO DE VISITA EN CADA TIENDA #####

    tiempoVisita = logistica["tiempoVisita"]

##### RETRASO EN LA ENTREGA DE PEDIDOS #####

    retrasoEntrega = logistica["retrasoEntrega"]


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

##### RUTA TIENDA i - TIENDA j #####

    rutas = datosRutas["rutas"]


################################# INFORMACIÓN SEGÚN EL TIPO DE TIENDA #################################
    
    tiendas = datos["tiendas"]

##### CAPACIDAD DE LAS TIENDAS #####

    capacidadTienda = tiendas["capacidadTienda"]

##### PRECIO DE LA BEBIDA PARA CADA TIENDA #####

    precioBebida = tiendas["precioBebida"]



#######################################################################################################
######################################## SOLUCIÓN DEL PROBLEMA ########################################
#######################################################################################################

####################################### DATOS DE LA SIMULACIÓN ########################################

    datosSimulacion = resultados["datosSimulacion"]
    
##### NÚMERO DE COMERCIANTES #####

    numComerciantes = datosSimulacion["numComerciantes"]
    
##### DEMANDA TOTAL #####

    demandaTienda = datosSimulacion["demandaTienda"]
    
##### TIEMPO DE SIMULACIÓN TOTAL #####

    tiempoSimulacionTotal = datosSimulacion["tiempoSimulacionTotal"]


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
    
    

#######################################################################################################
########################################## RESULTADOS REALES ##########################################
#######################################################################################################
    
######################################## TRABAJO COMERCIANTES #########################################

########## TIEMPO ##########
    
    # TIEMPO TOTAL POR DÍA Y COMERCIANTE
    tiempoComercianteDia = [[0 for d in range(numDiasReal)] for c in range(numComerciantes)]
    
    for c in range(numComerciantes):
        for d in range(numDiasReal):
            tiempoDesplazamiento = sum(tiempoRutas[i][j] * X[c,d,i,j] for i in range(numTiendas) for j in range(numTiendas) if i != j)
            numeroVisitas = sum(V[c,d,i] for i in range(1, numTiendas))
            tiempoTiendas = tiempoVisita * numeroVisitas
            
            tiempoComercianteDia[c][d] = Decimal(str(tiempoDesplazamiento + tiempoTiendas)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    # TIEMPO TOTAL
    tiempoTrabajoTotal = sum(tiempoComercianteDia[c][d] for d in range(numDiasReal) for c in range(numComerciantes))
    
########## DISTANCIA ##########
  
    # DISTANCIA TOTAL POR DÍA Y COMERCIANTE
    distanciaComercianteDia = [[0 for d in range(numDiasReal)] for c in range(numComerciantes)]
    
    for c in range(numComerciantes):
        for d in range(numDiasReal):
            distanciaDesplazamiento = sum(distanciaRutas[i][j] * X[c,d,i,j] for i in range(numTiendas) for j in range(numTiendas) if i != j)
            
            distanciaComercianteDia[c][d] = Decimal(str(distanciaDesplazamiento)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # DISTANCIA TOTAL
    distanciaRecorridaTotal = sum(distanciaComercianteDia[c][d] for d in range(numDiasReal) for c in range(numComerciantes))


######################################### COMPRAS E INGRESOS ##########################################
    
########## UNIDADES COMPRADAS ##########
            
    # POR TIENDA Y TIPO
    udsCompradasTiendaTipo = [[0 for b in range(numBebidas)] for i in range(numTiendas)]
    
    for i in range(1, numTiendas):
        for b in range(numBebidas):
            udsCompradasTiendaTipo[i][b] = int(sum(U[d,i,b] for d in range(numDiasReal)))         
            
    # TOTAL POR TIENDA
    udsCompradasTienda = [0 for i in range(numTiendas)]
    
    for i in range(1, numTiendas):
        udsCompradasTienda[i] = sum(udsCompradasTiendaTipo[i][b] for b in range(numBebidas))
        
    # TOTAL POR TIPO
    udsCompradasTipo = [0 for b in range(numBebidas)]
    
    for b in range(numBebidas):
        udsCompradasTipo[b] = sum(udsCompradasTiendaTipo[i][b] for i in range(1, numTiendas))

    # TOTAL
    udsCompradasTotal = sum(udsCompradasTienda[i] for i in range(numTiendas))

########## INGRESOS ##########
            
    # POR TIENDA Y TIPO
    ingresosTiendaTipo = [[0 for b in range(numBebidas)] for i in range(numTiendas)]
    
    for i in range(1, numTiendas):
        for b in range(numBebidas):
            sumaIngresos = precioBebida[i][b] * int(sum(U[d,i,b] for d in range(1, numDiasReal)))
            ingresosTiendaTipo[i][b] = Decimal(str(sumaIngresos)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
               
    # TOTAL POR TIENDA
    ingresosTienda = [0 for i in range(numTiendas)]
    
    for i in range(numTiendas):
        sumaIngresos = sum(ingresosTiendaTipo[i][b] for b in range(numBebidas))
        ingresosTienda[i] = Decimal(str(sumaIngresos)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
    # TOTAL POR TIPO
    ingresosTipo = [0 for b in range(numBebidas)]
    
    for b in range(numBebidas):
        sumaIngresos = sum(ingresosTiendaTipo[i][b] for i in range(1, numTiendas))
        ingresosTipo[b] = Decimal(str(sumaIngresos)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    # TOTAL
    ingresosTotal = sum(ingresosTienda[i] for i in range(numTiendas))


############################################### VENTAS ################################################
    
########## UNIDADES VENDIDAS ##########
            
    # POR COMERCIANTE
    udsVendidasComerciante = [0 for c in range(numComerciantes)]

    for c in range(numComerciantes):
        udsVendidasComerciante[c] = sum(U[d+retrasoEntrega,i,b] * V[c,d,i] for b in range(numBebidas) for i in range(1, numTiendas) for d in range(numDiasReal-retrasoEntrega))
    
    # TOTAL
    udsVendidasTotal = sum(udsVendidasComerciante[c] for c in range(numComerciantes))
    
    
######################################### SUELDO COMERCIANTES #########################################
    
########## COMISIONES ##########

    # POR COMERCIANTE
    comisionComerciante = [0 for c in range(numComerciantes)]

    for c in range(numComerciantes):
        dineroComision = comision * sum(U[d+retrasoEntrega,i,b] * V[c,d,i] * precioBebida[i][b] for b in range(numBebidas) for i in range(1, numTiendas) for d in range(numDiasReal-retrasoEntrega))
        comisionComerciante[c] = Decimal(str(dineroComision)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    # TOTAL
    comisionTotal = sum(comisionComerciante[c] for c in range(numComerciantes))

########## DÍAS TRABAJADOS ##########
    
    # POR COMERCIANTE
    sueldoDiaComerciante = [0 for c in range(numComerciantes)]
    
    for c in range(numComerciantes):  
        sueldo = sum(L[c,d] * costeDia for d in range(numDiasReal))
        sueldoDiaComerciante[c] = Decimal(str(sueldo)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    # TOTAL
    sueldoDiaTotal = sum(sueldoDiaComerciante[c] for c in range(numComerciantes))

########## HORAS TRABAJADAS ##########
    
    # POR COMERCIANTE
    sueldoHoraComerciante = [0 for c in range(numComerciantes)]
    
    for c in range(numComerciantes):
        sueldo = sum(tiempoComercianteDia[c][d] * costeHora for d in range(numDiasReal))
        sueldoHoraComerciante[c] = Decimal(str(sueldo)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    # TOTAL
    sueldoHoraTotal = sum(sueldoHoraComerciante[c] for c in range(numComerciantes))

########## SUELDO TOTAL ##########
    
    # POR COMERCIANTE
    sueldoComerciante = [0 for c in range(numComerciantes)]
    
    for c in range(numComerciantes):
        sueldoComerciante[c] = sueldoDiaComerciante[c] + sueldoHoraComerciante[c] + comisionComerciante[c]

    # TOTAL
    sueldoTotal = sum(sueldoComerciante[c] for c in range(numComerciantes))
    
    
########################################## NÚMERO DE VISITAS ##########################################
    
########## VISITAS REALIZADAS ##########
    
    # TOTAL
    visitasTotal = sum(V[c,d,i] for i in range(1, numTiendas) for d in range(numDiasReal) for c in range(numComerciantes))
    
    
############################################## BENEFICIO ##############################################
    
########## FUNCIÓN OBJETIVO: MAXIMIZAR BENEFICIO TOTAL ##########

    # TOTAL
    beneficioTotal = ingresosTotal - sueldoTotal
    


#######################################################################################################
########################################## MENÚ DEL PROGRAMA ##########################################
#######################################################################################################
    
    while True:        

        opcion = presentacion.menuOptimizacion()
            
        
        if opcion == "1":  # INFORME MODELO MATEMÁTICO
            
            solucion.informeModeloMatematico(numVariables, numRestricciones,
                                             modo, numTiendasReal, numDiasReal, numBebidas, numComerciantes, numEscenarios, retrasoEntrega, tiempoSimulacionTotal,
                                             udsVendidasTotal, visitasTotal, distanciaRecorridaTotal, tiempoTrabajoTotal,
                                             ingresosTotal, sueldoTotal, beneficioTotal)


        elif opcion == "2":  # INFORME VENTAS

            while True:

                opcion = presentacion.menuVentas()
                    
                if opcion == "1":  # EVOLUCIÓN DEL STOCK DE BEBIDAS
                
                    solucion.graficaStock(S, U, V, demandaTienda, capacidadTienda, numTiendas, numBebidas, numDiasReal, numComerciantes, numEscenarios, nombres)

                elif opcion == "2":  # DESGLOSE DE VENTAS E INGRESOS
             
                    solucion.desgloseVentas(numTiendas, numBebidas, precioBebida, udsCompradasTiendaTipo, ingresosTiendaTipo, udsCompradasTienda, ingresosTienda, udsCompradasTipo, ingresosTipo, udsCompradasTotal, ingresosTotal)
        
                elif opcion == "3":  # VOLVER ATRÁS

                    break
                                
                else:
                    presentacion.mensajeMenu("OPCION_NO_VALIDA", 2)


        elif opcion == "3":  # INFORME COMERCIANTES

            while True:

                opcion = presentacion.menuComerciantes()

                if opcion == "1":  # RUTAS DIARIAS DE CADA COMERCIANTE
                
                    secuencias = solucion.obtenerSecuenciaVisitas(X, numTiendas, numComerciantes, numDiasReal)

                    solucion.mapaRutas(modo, latitudes, longitudes, nombres, direcciones, secuencias, rutas, numComerciantes, numDiasReal, distanciaComercianteDia, distanciaMax, tiempoComercianteDia, tiempoMax)

                elif opcion == "2":  # DESGLOSE DE VENTAS POR COMERCIANTE
                    
                    solucion.desgloseSueldos(numComerciantes, sueldoTotal, sueldoDiaTotal, sueldoHoraTotal, comisionTotal, sueldoComerciante, udsVendidasComerciante, sueldoDiaComerciante, sueldoHoraComerciante, comisionComerciante)
                
                elif opcion == "3":  # VOLVER ATRÁS

                    break
                
                else:
                    presentacion.mensajeMenu("OPCION_NO_VALIDA", 2)


        elif opcion == "4":  # SALIR
            presentacion.mensajeMenu("CERRANDO")
            break
        
        else:
            presentacion.mensajeMenu("OPCION_NO_VALIDA")