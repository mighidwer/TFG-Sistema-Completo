# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · configuracion.py

    Este fichero contiene la configuración general del problema de optimización.
    Incluye todos los parámetros estructurales, operativos, económicos y de simulación
    del sistema, permitiendo definir de forma centralizada los distintos escenarios de
    simulación utilizados por los modelos de optimización.
    
"""

# Importación de librerías estándar
from decimal import Decimal

# Importación de módulos propios del proyecto
from Modelos import herramientasModelo
import matrizRutas
import utilidades



'''
    Proporciona todos los parámetros utilizados por los distintos modelos del sistema.
    Además, construye los datos derivados necesarios para la ejecución de los experimentos.

    Devuelve:
        - config (dict[str, Any]): Diccionario que contiene toda la información necesaria para ejecutar los modelos de optimización y realizar el posterior análisis de resultados.
'''
def obtenerConfig():
    
#######################################################################################################
######################################### DATOS DEL PROBLEMA ##########################################
#######################################################################################################
    
############################ INFORMACIÓN BÁSICA Y DIMENSIONES DEL PROBLEMA ############################

##### INFORMACIÓN DE LAS TIENDAS #####

    nombres, direcciones, tipos, latitudes, longitudes = utilidades.obtenerInfo()
    
##### NÚMERO TOTAL DE TIENDAS #####
#!!!
    numTiendasReal = 15 # len(nombres)-1  # La primera "tienda" es la oficina, por eso no la contamos como tienda
    
    numTiendas = numTiendasReal + 1  # Añadimos la oficina para la simulación
    
##### NÚMERO DE DÍAS #####

    numDiasReal = 7  # Días "reales" que se tendrán en cuenta para la lectura de los datos finales
    
    numDias = numDiasReal + 2  # Horizonte ampliado, añadimos días "ficticios" con penalización de stock sobrante
   
##### NÚMERO DE TIPOS DE BEBIDA #####

    precioBase = [1.50, 2.50, 2.00] #, 1.75]  # Precio base de las bebidas

    numBebidas = len(precioBase)
    
##### NÚMERO DE COMERCIANTES #####

    minNumComerciantes = 2  # Número mínimo de comerciantes

    maxNumComerciantes = 6  # Número máximo de comerciantes
    
##### NÚMERO DE ESCENARIOS A SIMULAR #####

    numEscenarios = 3


################################ MODO DE TRANSPORTE Y LÍMITES FÍSICOS #################################

##### MODO DE DESPLAZAMIENTO #####

    modos = ["foot", "bike"]
    
    modo = modos[1]  # (0) foot, (1) bike

##### DISTANCIA TOTAL MÁXIMA POR DÍA #####
    
    if modo == "foot":
        distanciaMax = 5  # En kilometros
    elif modo == "bike":
        distanciaMax = 8  # En kilometros

##### TIEMPO MÁXIMO DE TRABAJO POR JORNADA #####
    
    tiempoMax = 6  # En horas


################################# RESTRICCIONES DE VISITAS Y ENTREGAS #################################
    
##### TIEMPO DE VISITA EN CADA TIENDA #####
    
    tiempoVisita = 0.25  # En horas (15 minutos)
    
##### PEDIDO MÍNIMO #####

    pedidoMinimo = 0.15  # En porcentaje (15% de la capacidad de la tienda)

##### RETRASO EN LA ENTREGA DE PEDIDOS #####

    retrasoEntrega = 1  # En días (mínimo 1)
    
##### PEDIDOS PENDIENTES DE ENTREGA (MPC) #####

    pedidosPendientes = [[[0 for b in range(numBebidas)] for i in range(numTiendas)] for d in range(retrasoEntrega)]

##### MÁXIMO DE DÍAS CONSECUTIVOS DE TRABAJO #####
    
    maxDiasConsecutivos = 3

##### DESCANSO OBLIGATORIO (MPC) #####

    descansoObligatorio = {}

##### FRECUENCIA DE LAS VISITAS (MODELOS ALTERNATIVOS) #####

    frecuenciaVisita = 2  # Cada cuántos días se realizan las visitas


################################ CONDICIONES COMERCIALES Y FINANCIERAS ################################

##### COSTE POR DÍA TRABAJADO DE LOS COMERCIANTES #####

    costeDia = 50

##### COSTE POR HORA TRABAJADA DE LOS COMERCIANTES #####

    costeHora = 10
    
##### COMISIÓN POR VENTAS #####
    
    comision = Decimal("0.05")  # En porcentaje (5% de las ventas)


######################################### DATOS DE LAS RUTAS ##########################################
    
##### DISTANCIA TIENDA i - TIENDA j #####
    
    distanciaRutas = matrizRutas.leerDatos(f"DatosRutas/distanciaRutas{modo.capitalize()}.csv")
                  
##### TIEMPO TIENDA i - TIENDA j #####

    tiempoRutas = matrizRutas.leerDatos(f"DatosRutas/tiempoRutas{modo.capitalize()}.csv")
    
##### RUTA TIENDA i - TIENDA j #####

    rutas = matrizRutas.leerDatos(f"DatosRutas/rutas{modo.capitalize()}.csv")
    

################################# INFORMACIÓN SEGÚN EL TIPO DE TIENDA #################################
    
##### CAPACIDAD DE LAS TIENDAS #####
    
    capacidadTienda = herramientasModelo.generarCapacidadTienda(numTiendas, tipos)

##### STOCK INICIAL DE LAS TIENDAS #####
    
    stockInicial = herramientasModelo.generarStockInicial(numEscenarios, numTiendas, numBebidas, tipos)

##### DEMANDA MEDIA DIARIA DE LAS TIENDAS #####
    
    demandaTienda = herramientasModelo.generarDemandaTienda(numEscenarios, numTiendas, numBebidas, numDias, tipos)
    
##### PRECIO DE LA BEBIDA PARA CADA TIENDA #####
    
    precioBebida = herramientasModelo.generarPrecioBebida(numTiendas, numBebidas, tipos, precioBase)
    
    
###################################### OPTIMIZACIÓN Y SIMULACIÓN ######################################

##### TIEMPO DE SIMULACIÓN #####
#!!!
    tiempoSimulacion = 600  # En segundos, (0) para simular sin límite de tiempo

##### TIEMPO DE ESPERA PARA ACTIVAR EL CONTROL DEL GAP #####

    tiempoGap = 300  # En segundos, (0) para simular sin activar el control del gap

##### MARGEN DE OPTIMALIDAD (GAP) #####

    gapMaximo = 0.02  # En porcentaje (2%)
        
##### PENALIZACIÓN STOCK SOBRANTE #####

    epsilon = 1e-4  # 1e-3
    
##### CÁLCULO IIS (Irreducible Infeasible Set) #####

    calculoIIS = True  # (True) Calcula IIS, (False) No calcula IIS
        
        
        
#######################################################################################################
############################################## RETURN #################################################
#######################################################################################################

    return {
        
        ########## INFORMACIÓN BÁSICA Y DIMENSIONES DEL PROBLEMA ##########

        "dimensiones": {

            "nombres": nombres,
            "direcciones": direcciones,
            "tipos": tipos,
            "latitudes": latitudes,
            "longitudes": longitudes,

            "numTiendasReal": numTiendasReal,
            "numTiendas": numTiendas,

            "numDiasReal": numDiasReal,
            "numDias": numDias,

            "precioBase": precioBase,
            "numBebidas": numBebidas,

            "minNumComerciantes": minNumComerciantes,
            "maxNumComerciantes": maxNumComerciantes,

            "numEscenarios": numEscenarios
        },

        ########## MODO DE TRANSPORTE Y LÍMITES FÍSICOS ##########
        
        "transporte": {
            
            "modos": modos,
            "modo": modo,

            "distanciaMax": distanciaMax,
            "tiempoMax": tiempoMax,
        },

        ########## RESTRICCIONES DE VISITAS Y ENTREGAS ##########

        "logistica": {

            "tiempoVisita": tiempoVisita,
            
            "pedidoMinimo": pedidoMinimo,
            "retrasoEntrega": retrasoEntrega,
            "pedidosPendientes": pedidosPendientes,
            
            "maxDiasConsecutivos": maxDiasConsecutivos,
            "descansoObligatorio": descansoObligatorio,
            "frecuenciaVisita": frecuenciaVisita
        },

        ########## CONDICIONES COMERCIALES Y FINANCIERAS ##########

        "costes": {

            "costeDia": costeDia,
            "costeHora": costeHora,
            "comision": comision
        },

        ########## DATOS DE LAS RUTAS ##########

        "datosRutas": {

            "distanciaRutas": distanciaRutas,
            "tiempoRutas": tiempoRutas,
            "rutas": rutas
        },

        ########## INFORMACIÓN SEGÚN EL TIPO DE TIENDA ##########

        "tiendas": {

            "capacidadTienda": capacidadTienda,
            "stockInicial": stockInicial,
            "demandaTienda": demandaTienda,
            "precioBebida": precioBebida
        },

        ########## OPTIMIZACIÓN Y SIMULACIÓN ##########

        "optimizacion": {

            "tiempoSimulacion": tiempoSimulacion,
            "tiempoGap": tiempoGap,

            "gapMaximo": gapMaximo,

            "epsilon": epsilon,

            "calculoIIS": calculoIIS
        }
    }