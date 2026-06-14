# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · solucion.py

    Este fichero contiene las funciones que nos permiten representar los distintos datos
    de la solución obtenida tras la simulación del problema de optimización, tanto en
    formato gráfico como en formato de texto.
 
"""

# Importación de librerías estándar
import json

# Importación de dependencias externas
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# Importación de módulos propios del proyecto
import presentacion
import utilidades
import leyenda



###################################### INFORME MODELO MATEMÁTICO ######################################

'''
    Muestra por pantalla un informe del modelo matemático y de los principales
    resultados globales obtenidos en la simulación.

    Argumentos:
        - numVariables (int):              Número total de variables del modelo.
        - numRestricciones (int):          Número total de restricciones del modelo.

        - modo (str):                      Modo de desplazamiento.
        - numTiendasReal (int):            Número de tiendas consideradas.
        - numDiasReal (int):               Número de días simulados.
        - numBebidas (int):                Número de tipos de bebidas.
        - numComerciantes (int):           Número de comerciantes.
        - numEscenarios (int):             Número de escenarios simulados.
        - retrasoEntrega (int):            Retraso en la entrega de pedidos.
        - tiempoSimulacionTotal (float):   Tiempo total de optimización del modelo.

        - udsVendidasTotal (int):          Unidades totales vendidas.
        - visitasTotal (int):              Número total de visitas realizadas.
        - distanciaRecorridaTotal (float): Distancia total recorrida (km).
        - tiempoTrabajoTotal (float):      Tiempo total de trabajo (horas).

        - ingresosTotal (float):           Ingresos totales del sistema.
        - sueldoTotal (float):             Coste total en sueldos.
        - beneficioTotal (float):          Beneficio total del sistema.
'''
def informeModeloMatematico(numVariables, numRestricciones,
                            modo, numTiendasReal, numDiasReal, numBebidas, numComerciantes, numEscenarios, retrasoEntrega, tiempoSimulacionTotal,
                            udsVendidasTotal, visitasTotal, distanciaRecorridaTotal, tiempoTrabajoTotal,
                            ingresosTotal, sueldoTotal, beneficioTotal):

    presentacion.tituloMenu("INFORME MODELO MATEMÁTICO", "-")

    print("\t  FUNCIÓN OBJETIVO")
    print("\t   · Maximizar: beneficioTotal = ingresosTotal - sueldoTotal")

    print("\n\t  TAMAÑO DEL MODELO")
    print(f"\t   · Número de variables: {numVariables}")
    print(f"\t   · Número de restricciones: {numRestricciones}")

    print("\n\t  DATOS DE LA SIMULACIÓN:")
    print(f"\t   · Modo de desplazamiento: {modo}")
    print(f"\t   · Tiendas: {numTiendasReal}")
    print(f"\t   · Días: {numDiasReal}")
    print(f"\t   · Bebidas: {numBebidas}")
    print(f"\t   · Comerciantes: {numComerciantes}")
    print(f"\t   · Escenarios simulados: {numEscenarios}")
    print(f"\t   · Retraso en la entrega: {retrasoEntrega}")
    print(f"\t   · Tiempo total de la optimización del modelo: {tiempoSimulacionTotal}")

    print("\n\t  RESULTADOS GLOBALES")
    print(f"\t   · Unidades Vendidas Totales: {udsVendidasTotal} unidades")
    print(f"\t   · Visitas Totales Realizadas: {visitasTotal} visitas")
    print(f"\t   · Distancia Recorrida Total: {distanciaRecorridaTotal} km")
    print(f"\t   · Tiempo de Trabajo Total: {tiempoTrabajoTotal} h")

    print("\n\t  RESUMEN ECONÓMICO")
    print(f"\t   · Ingresos Totales: {ingresosTotal} €")
    print(f"\t   · Sueldo Comerciantes: {sueldoTotal} €")
    print(f"\t   · Beneficio Total: {beneficioTotal} €")




########################################### INFORME VENTAS ############################################

'''
    Representa gráficamente el stock, las ventas y las visitas de comerciantes
    para cada tienda a lo largo de varios días, junto con una leyenda explicativa.

    Argumentos:
        - S (dict[tuple[int,int,int,int], gurobi.var]): Variables enteras 4D que almacenan el stock inicial de cada día para cada tipo de bebida en cada una de las tiendas.
        - U (dict[tuple[int,int,int], gurobi.var]):     Variables enteras 3D que almacenan las unidades entregadas cada día de cada tipo de bebida en cada una de las tiendas.
        - V (dict[tuple[int,int,int], gurobi.var]):     Variables binarias 3D que almacenan las visitas realizadas por los comerciantes.
        - demandaTienda (list[list[list[list[int]]]]):  Demanda diaria de cada tipo de bebida en cada una de las tiendas para cada escenario simulado.
        - capacidadTienda (list[int]):                  Capacidad máxima de cada tienda.
        - numTiendas (int):                             Número total de tiendas.
        - numBebidas (int):                             Número de tipos de bebida.
        - numDias (int):                                Número de días.
        - numComerciantes (int):                        Número de comerciantes.
        - numEscenarios (int):                          Número de escenarios simulados.
        - nombres (list[str]):                          Lista con los nombres de las tiendas.
'''
def graficaStock(S, U, V, demandaTienda, capacidadTienda, numTiendas, numBebidas, numDias, numComerciantes, numEscenarios, nombres):       
    
    # Obtenemos los colores (y sus tonos) que se van a utilizar en la representación del stock
    coloresBebidas = leyenda.generarColores(numBebidas+1, tonos=True, uso="stock")  # Generamos un color de más para usarlo en la leyenda para los "Tipos de Unidades"
    colorVisita = "#9b59b6"  # Púrpura, color para marcar las visitas de los comerciantes
    
    # Creamos la portada
    leyenda.portada("EVOLUCIÓN DEL STOCK\nDE LAS TIENDAS")
    
    
    ###################################################
    ######           BLOQUE 1: LEYENDA           ######
    ###################################################
    
    numSecciones = 3  # Número de secciones que tendrá la leyenda
    
    # Leemos los parámetros necesarios
    espaciadoLineas, anchoCuadro, alturaCuadro, separacionSimbolo, separacionColumnas = leyenda.parametrosLeyenda(numSecciones)
    
    # Calculamos el número de filas y columnas de la primera sección, que influirán en el tamaño total del plot de la leyenda
    bebidasColumna    = 5  # Máximo de bebidas por columna
    numColumnasBebida = int(np.ceil(numBebidas / bebidasColumna))
    numLineasBebida   = min(numBebidas, bebidasColumna)

    # Ajustamos el tamaño del plot según el contenido que va a tener
    anchoTotal  = 5.2 + 1.5  * numColumnasBebida
    alturaTotal = 4.5 + 0.75 * numLineasBebida

    # Creamos el plot de la leyenda
    figLeyendaleg, ejeLeyenda = plt.subplots(figsize=(anchoTotal, alturaTotal))
    ejeLeyenda.axis('off')  # Ocultamos los ejes

    # ========================================
    #  SECCIÓN 1: TIPO DE BEBIDA
    # ========================================
    
    # Calculamos el ancho total esta sección
    anchoTotalBebidas = numColumnasBebida * separacionColumnas
    
    # Marcamos el punto horizontal inicial relativo para que las columnas queden centradas
    inicioEjeX = 0.52 - anchoTotalBebidas/2
    
    # Creamos una variable que nos permite conocer la posición vertical relativa del plot en la que estamos trabajando, con un valor inicial
    posicionEjeY = 0.9
    
    # Añadimos el título de la sección y actualizamos la posición vertical relativa
    posicionEjeY = leyenda.titulo("TIPO DE BEBIDA", posicionEjeY, numSecciones, ejeLeyenda)
    
    # Almacenamos la posición vertical relativa de la primera fila
    inicioEjeY = posicionEjeY
    
    # Imprimimos todas las bebidas que hay junto a un cuadro que muestra su color
    for b, color in enumerate(coloresBebidas[:-1]):  # No llegamos al último color, ya que se usa únicamente para el símbolo de la leyenda, no es una bebida más
        columna      = b // bebidasColumna                      # Calculamos la columna a la que pertenece
        fila         = b % bebidasColumna                       # Calculamos la fila a la que pertenece
        posicionEjeX = inicioEjeX + columna*separacionColumnas  # Calculamos la posición horizontal relativa
        
        if fila == 0:  # Si iniciamos una nueva columna...
            posicionEjeY = inicioEjeY  # Tomamos la posición vertical relativa de la primera fila

        # Añadimos los elementos de esta sección
        posicionEjeY = leyenda.cuadro(f"Bebida {b+1}", color["stock"], posicionEjeX, posicionEjeY, numSecciones, ejeLeyenda)

    # Calculamos la nueva posición vertical relativa de trabajo, en función del número de filas que se hayan creado
    posicionEjeY = inicioEjeY - min(numBebidas, bebidasColumna)*espaciadoLineas
    
    # Añadimos una línea horizontal de separación y actualizamos la posición vertical relativa
    posicionEjeY = leyenda.linea(posicionEjeY, numSecciones, ejeLeyenda)

    # ========================================
    #  SECCIÓN 2: TIPO DE UNIDADES
    # ========================================
    
    # Añadimos el título de la sección y actualizamos la posición vertical relativa
    posicionEjeY = leyenda.titulo("TIPO DE UNIDADES", posicionEjeY, numSecciones, ejeLeyenda)
    
    # Marcamos un nuevo punto horizontal relativo para iniciar la escritura y que quede centrado
    posicionEjeX = 0.28 + numColumnasBebida*0.015
    
    # Escogemos un color de referencia para esta sección (elegimos el último, no representa ninguna bebida)
    colorRef = coloresBebidas[-1]
    
    # Añadimos los elementos de esta sección y actualizamos la posición vertical relativa
    posicionEjeY = leyenda.cuadro("Unidades almacenadas", colorRef["stock"], posicionEjeX, posicionEjeY, numSecciones, ejeLeyenda)

    posicionEjeY = leyenda.cuadro("Unidades que llegan", colorRef["compra"], posicionEjeX, posicionEjeY, numSecciones, ejeLeyenda)
    
    posicionEjeY = leyenda.cuadro("Unidades vendidas", colorRef["venta"], posicionEjeX, posicionEjeY, numSecciones, ejeLeyenda, hatch="//")
    
    # Añadimos una línea horizontal de separación y actualizamos la posición vertical relativa
    posicionEjeY = leyenda.linea(posicionEjeY, numSecciones, ejeLeyenda)

    # ========================================
    #  SECCIÓN 3: OTROS
    # ========================================
    
    # Añadimos el título de la sección y actualizamos la posición vertical relativa
    posicionEjeY = leyenda.titulo("OTROS", posicionEjeY, numSecciones, ejeLeyenda)
    
    # Marcamos un nuevo punto horizontal relativo para iniciar la escritura y que quede centrado
    posicionEjeX = 0.31 + numColumnasBebida*0.015

    # Representamos la capacidad de la tienda
    ejeLeyenda.plot([posicionEjeX, posicionEjeX + anchoCuadro], [posicionEjeY, posicionEjeY], transform=ejeLeyenda.transAxes, color='red', linestyle='--', linewidth=2)
    ejeLeyenda.text(posicionEjeX + separacionSimbolo, posicionEjeY, "Capacidad Tienda", transform=ejeLeyenda.transAxes, fontsize=13, ha='left', va='center')
    
    # Actualizamos la posición vertical relativa
    posicionEjeY -= espaciadoLineas
    
    # Representamos la visita de los comerciantes
    tri = mpatches.RegularPolygon((posicionEjeX + anchoCuadro/2, posicionEjeY), 3, radius=alturaCuadro/2, orientation=np.pi, transform=ejeLeyenda.transAxes, facecolor=colorVisita, edgecolor='black')
    ejeLeyenda.add_patch(tri)
    ejeLeyenda.text(posicionEjeX + separacionSimbolo, posicionEjeY, "Visita Comerciante", transform=ejeLeyenda.transAxes, fontsize=13, ha='left', va='center')

    # Añadimos un marco a toda la leyenda
    marco = mpatches.Rectangle((0.05, 0.05), 0.9, 0.9, transform=ejeLeyenda.transAxes, facecolor='none', edgecolor='gray', linewidth=2, linestyle='-')
    ejeLeyenda.add_patch(marco)

    # Mostramos el plot de la leyenda
    plt.show()


    ###################################################
    ######     BLOQUE 2: GRÁFICAS POR TIENDA     ######
    ###################################################
    
    diasEjeX = 7  # Número máximo de días a representar en una fila (una semana)
    for e in range(numEscenarios):
    
        # ========================================
        #  SECCIÓN 1: INFO ESCENARIO
        # ========================================
        
        if numEscenarios != 1:  # Si tenemos más de un escenario...
            
            # Creamos el plot para la portada de cada escenario
            fig, eje = plt.subplots(figsize=(8, 4))
            eje.axis("off")  # Ocultamos los ejes
            
            # Añadimos el texto con un marco
            eje.text(0.5, 0.5, f"GRÁFICAS ESCENARIO {e+1}", ha="center", va="center", fontsize=20, fontweight="bold", fontstyle="italic",
                    bbox=dict(boxstyle="round,pad=0.6", edgecolor="black", facecolor="#f0f0f0", linewidth=2))
            
            # Mostramos el plot
            plt.show()
        
        # ========================================
        #  SECCIÓN 2: GRÁFICAS
        # ========================================
        
        for i in range(1, numTiendas):  # Para cada tienda...
            filas = int(np.ceil(numDias / diasEjeX))  # Calculamos el número de filas (semanas)
            
            # Creamos el plot con el tamaño adecuado según el número de semanas
            fig, ejeSub = plt.subplots(filas, 1, figsize=(12, 5*filas), sharey=True)
            
            if filas == 1:  # Si sólo hay una fila...
                ejeSub = [ejeSub]  # Trabajamos con listas igualmente, para evitar errores
    
            for fila in range(filas):  # Para cada fila...
                inicio = fila * diasEjeX               # Calculamos el día inicial
                fin = min(inicio + diasEjeX, numDias)  # Calculamos el día final
                dias = np.arange(inicio, fin)          # Creamos una lista con los días de esa semana
                
                # Seleccionamos el eje de la fila con la que estamos trabajando
                eje = ejeSub[fila]
                
                # Representamos el stock inicial de cada día junto a las unidades que llegan ese mismo día (en la misma columna)
                baseStock = np.zeros(len(dias))  # Creamos la base del stock para cada día
                
                for b in range(numBebidas):  # Para cada tipo de bebida...
                    stockInicial = [S[e,d,i,b] for d in dias]  # Leemos el stock inicial de cada día
                    entregas = [U[d,i,b] for d in dias]      # Leemos las unidades entregadas cada día
                    
                    # Mostramos el stock inicial de cada bebida
                    eje.bar(dias - 0.2, stockInicial, width=0.2, bottom=baseStock, color=coloresBebidas[b]["stock"])
                    # Mostramos las unidades que llegan de cada bebida
                    eje.bar(dias - 0.2, entregas, width=0.2, bottom=np.array(baseStock) + np.array(stockInicial), color=coloresBebidas[b]["compra"])
                    # Añadimos un borde para cada tipo de bebida (stock inicial + unidades entregadas)
                    eje.bar(dias - 0.2, np.array(stockInicial) + np.array(entregas), width=0.2, bottom=baseStock, color='none', edgecolor='black')
                    
                    # Actualizamos el punto más bajo de la gráfica del stock tras añadir un tipo de bebida
                    baseStock += np.array(stockInicial) + np.array(entregas)
    
                # Representamos las ventas de cada día
                baseVentas = np.zeros(len(dias))  # Creamos la base de las ventas para cada día
                
                for b in range(numBebidas):  # Para cada tipo de bebida...
                    ventas = [demandaTienda[e][d][i][b] for d in dias]  # Leemos las ventas de cada día
                    
                    # Mostramos las unidades vendidas de cada bebida
                    eje.bar(dias + 0.2, ventas, width=0.2, bottom=baseVentas, color=coloresBebidas[b]["venta"], hatch='//', edgecolor='black')
                    
                    # Actualizamos el punto más bajo de la gráfica de las ventas tras añadir un tipo de bebida
                    baseVentas += ventas
    
                # Representamos la capacidad de cada tienda
                eje.axhline(capacidadTienda[i], color='red', linestyle='--', label="Capacidad Tienda")
    
                # Representamos las visitas de los comerciantes
                for c in range(numComerciantes):  # Para cada comerciante...
                    visitas = [V[c,d,i] for d in dias]  # Leemos las tiendas que visita cada día
                    for x, v in enumerate(visitas):
                        if v == 1:  # Si ha visitado la tienda...
                            # Marcamos los días en los que se produjeron las visitas 
                            eje.scatter(dias[x], capacidadTienda[i]*1.05, marker='v', color=colorVisita, s=150, edgecolor='black')
                            # Y añadimos el identificador de dicho comerciante
                            eje.text(dias[x], capacidadTienda[i]*1.09, str(c+1), color='black', fontsize=11, ha='center', va='bottom')
    
                # Ajustamos el tamaño del eje Y
                eje.set_ylim(0, capacidadTienda[i] * 1.25)
                
                # Mostramos la información de los ejes
                eje.set_ylabel("Stock")
                eje.set_xticks(dias)
                eje.set_xticklabels([f"Día {d+1}" for d in dias])
                
                # Añadimos un título a cada subplot
                if filas > 1:  # Si hay más de una semana...
                    eje.set_title(f"Semana {fila+1}")
    
            # Mostramos la etiqueta del eje X (aunque haya más de un fila sólo se muestra una vez)
            ejeSub[-1].set_xlabel("Días")
            
            if numEscenarios != 1:  # Si tenemos más de un escenario...
                # Añadimos un título al plot indicando el escenario al que corresponde
                fig.suptitle(f"ESCENARIO {e+1}: {nombres[i]} (Tienda {i})", fontsize=15, y=0.93)
            else:  # Si sólo tenemos un escenario...
                # Añadimos un título al plot sin indicar el escenario
                fig.suptitle(f"{nombres[i]} (Tienda {i})", fontsize=15, y=0.93)
            
            # Mostramos el plot de la gráfica
            plt.show()
    
    
    ###################################################
    ######     BLOQUE 3: INFORMACIÓN ESCRITA     ######
    ###################################################

    presentacion.encabezadoSeccion("EVOLUCIÓN DEL STOCK DE LAS TIENDAS")
    
    for e in range(numEscenarios):
        print(f"\n\t -- ESCENARIO {e+1} --")
        for i in range(1, numTiendas):
            print(f"\n\t  · TIENDA {i}")
            for d in range(numDias):
                print(f"\t\t  DÍA {d+1}")
                stockTotalBebidas = 0
                llegadasTotales = 0
                demandaTotal = 0
                for b in range(numBebidas):
                    print(f"\t\t\t- Stock de la Bebida {b+1}: {S[e,d,i,b]}")
                    print(f"\t\t\t   · Llegan {U[d,i,b]}\t· Se venden {demandaTienda[e][d][i][b]}")
                    stockTotalBebidas += S[e,d,i,b]
                    llegadasTotales += U[d,i,b]
                    demandaTotal += demandaTienda[e][d][i][b]
                print("\t\t\t-----------------------------------------------------------------")
                print(f"\t\t\t  · Stock Total Inicial = {stockTotalBebidas} / Capacidad = {capacidadTienda[i]}")
                if llegadasTotales > 0:
                    print(f"\t\t\t  · Stock Total tras Entrega del Pedido = {stockTotalBebidas+llegadasTotales} / Capacidad = {capacidadTienda[i]}")
                print("\t\t\t-----------------------------------------------------------------")




'''
    Muestra por pantalla un desglose detallado de las ventas e ingresos de
    cada tienda mediante tablas compactas y adaptables al número de bebidas.

    Para cada tienda se muestra:
        - El coste por unidad de cada bebida.
        - Las unidades compradas de cada bebida.
        - Los ingresos generados por cada bebida.
        - El total de unidades compradas en la tienda.
        - Los ingresos totales de la tienda.

    Finalmente, se muestra una tabla resumen global con:
        - Las unidades totales compradas por tipo de bebida.
        - Los ingresos totales generados por cada tipo de bebida.
        - El total global de unidades compradas.
        - Los ingresos globales finales.

    Argumentos:
        - numTiendas (int):                         Número total de tiendas.
        - numBebidas (int):                         Número total de tipos de bebida.
        - precioBebida (list[list[float]]):         Matriz con el precio por unidad de cada bebida en cada tienda.
        - udsCompradasTiendaTipo (list[list[int]]): Matriz con las unidades compradas por tienda y tipo de bebida.
        - ingresosTiendaTipo (list[list[float]]):   Matriz con los ingresos por tienda y tipo de bebida.
        - udsCompradasTienda (list[int]):           Lista con las unidades totales compradas en cada tienda.
        - ingresosTienda (list[float]):             Lista con los ingresos totales de cada tienda.
        - udsCompradasTipo (list[int]):             Lista con las unidades totales compradas por tipo de bebida.
        - ingresosTipo (list[float]):               Lista con los ingresos totales por tipo de bebida.
        - udsCompradasTotal (int):                  Número total de unidades compradas entre todas las tiendas.
        - ingresosTotal (float):                    Ingresos totales obtenidos entre todas las tiendas.
'''
def desgloseVentas(numTiendas, numBebidas, precioBebida, udsCompradasTiendaTipo, ingresosTiendaTipo, udsCompradasTienda, ingresosTienda, udsCompradasTipo, ingresosTipo, udsCompradasTotal, ingresosTotal):

    presentacion.encabezadoSeccion("DESGLOSE DE VENTAS E INGRESOS")
    
    # Definimos las funciones auxiliares
    def linea():
        # Dibuja una línea horizontal de separación de la tabla
        print("\t  +----------+-------------+-----------+--------------+")
        
    def filaTabla(col1, col2, col3, col4, alineacion="^"):
        # Imprime una fila de la tabla, en función de la alineación elegida
        print(f"\t  | " f"{col1:{alineacion}8} | " f"{col2:{alineacion}11} | " f"{col3:{alineacion}9} | " f"{col4:{alineacion}12} |")

    # ========================================
    #  SECCIÓN 1: TABLAS TIENDAS
    # ========================================
    
    for i in range(1, numTiendas):
        
        print(f"\n\t -- TIENDA {i} --")

        linea()
        filaTabla("Bebida", "Coste/Ud", "Uds", "Ingresos")
        linea()

        for b in range(numBebidas):

            filaTabla(f"{b+1}", f"{precioBebida[i][b]} €/ud", f"{udsCompradasTiendaTipo[i][b]} uds", f"{ingresosTiendaTipo[i][b]} €", ">")

        linea()

        print(f"\t   · Unidades totales compradas : {udsCompradasTienda[i]} uds")
        print(f"\t   · Ingresos totales generados : {ingresosTienda[i]} €")

    # ========================================
    #  SECCIÓN 2: TABLA GENERAL
    # ========================================

    print("\n\t -- INFORMACIÓN GLOBAL --")

    linea()
    filaTabla("Bebida", "Uds totales", "", "Ingresos")
    linea()

    for b in range(numBebidas):

        filaTabla(f"{b+1}", f"{udsCompradasTipo[b]} uds", "", f"{ingresosTipo[b]} €", ">")
        
    linea()

    print(f"\t   · Unidades totales compradas : {udsCompradasTotal} uds")
    print(f"\t   · Ingresos totales generados : {ingresosTotal} €")




######################################## INFORME COMERCIANTES #########################################

'''
    Obtiene la secuencia de visitas a las tiendas por cada comerciante y día.

    Argumentos:
        - X (dict[tuple[int,int,int,int], gurobi.var]): Variables binarias 4D que indican los arcos seleccionados por cada comerciante y día.
        - numTiendas (int):                             Número total de tiendas (incluyendo la oficina).
        - numComerciantes (int):                        Número total de comerciantes.
        - numDias (int):                                Número total de días.

    Devuelve:
        - secuencias (dict[tuple[int,int], list[int]]): Diccionario con las secuencias de visita por comerciante y día.
             + Claves (tuple[int,int]): Tuplas (comerciante, día)
             + Valores (list[int]):     Lista de índices de tiendas visitadas en orden, comenzando y terminando en la oficina.
'''
def obtenerSecuenciaVisitas(X, numTiendas, numComerciantes, numDias):

    secuencias = {}  # {(c,d): [0, tienda1, tienda2, ..., 0]}

    for c in range(numComerciantes):
        for d in range(numDias):
            secuencia = [0]  # Empiezamos en la oficina (tienda 0)
            actual = 0
            visitados = set()
            while True:
                siguiente = None
                for j in range(numTiendas):
                    if j == actual:  # Evitamos i == j
                        continue
                    var = X[c,d,actual,j]
                    if var is not None and var > 0.5:  # Si el camino existe y se ha utilizado
                        siguiente = j  # Marcamos la siguiente tienda en la ruta
                        break

                if siguiente is None or siguiente in visitados:
                    break  # No hay más caminos usados
                
                secuencia.append(siguiente)
                visitados.add(siguiente)
                actual = siguiente

                if actual == 0:  # Vuelta a la oficina
                    break

            # Nos aseguramos que termina en la oficina
            if secuencia[-1] != 0:
                secuencia.append(0)

            secuencias[(c,d)] = secuencia  # Guardamos la secuencia para cada comerciante y cada día

    return secuencias  # Devolvemos todas las secuencias




'''
    Representa las rutas completas de cada comerciante para cada día en el que trabaja
    al menos un comerciante, mostrando el orden de visita de las tiendas.

    Argumentos:
        - modo (str, opcional):                         Modo de desplazamiento. Si se especifica, se representa la ruta.
        - latitudes (list[float]):                      Lista con las latitudes de la oficina y las tiendas.
        - longitudes (list[float]):                     Lista con las longitudes de la oficina y las tiendas.
        - nombres (list[str]):                          Lista con los nombres de las tiendas.
        - direcciones (list[str]):                      Lista con las direcciones de las tiendas.
        - secuencias (dict[tuple[int,int], list[int]]): Diccionario con las secuencias de visita por comerciante y día.
             + Claves (tuple[int,int]): Tuplas (comerciante, día)
             + Valores (list[int]):     Lista de índices de tiendas.
        - rutas (pd.DataFrame):                         DataFrame que contiene la ruta entre cada par de tiendas en formato JSON.
        - numComerciantes (int):                        Número total de comerciantes.
        - numDias (int):                                Número total de días.
        - distanciaComercianteDia (list[list[float]]):  Lista que almacena la distancia total recorrida por los comerciantes cada día.
        - distanciaMax (float):                         Distancia máxima que puede recorrer un comerciante durante una jornada laboral.
        - tiempoComercianteDia (list[list[float]]):     Lista que almacena el tiempo total de trabajo de los comerciantes cada día.
        - tiempoMax (float):                            Tiempo máximo que puede trabajar un comerciante durante una jornada laboral.
'''
def mapaRutas(modo, latitudes, longitudes, nombres, direcciones, secuencias, rutas, numComerciantes, numDias, distanciaComercianteDia, distanciaMax, tiempoComercianteDia, tiempoMax):

    # Le asignamos un color a cada comerciante y a la oficina
    coloresComerciantes = leyenda.generarColores(numComerciantes+1, uso="comerciantes")
    
    # Índices del fichero "rutas.csv"
    tiendas = ["oficina" if i == 0 else f"tienda {i}" for i in range(len(nombres))]
    
    # Creamos la portada
    leyenda.portada("RUTAS DIARIAS\nDE CADA COMERCIANTE")
    
    
    ###################################################
    ######           BLOQUE 1: LEYENDA           ######
    ###################################################
    
    numSecciones = 2  # Número de secciones que tendrá la leyenda
    
    # Leemos los parámetros necesarios
    espaciadoLineas, anchoCuadro, alturaCuadro, separacionSimbolo, separacionColumnas = leyenda.parametrosLeyenda(numSecciones)
    
    # Calculamos el número de filas y columnas de la primera sección, que influirán en el tamaño total del plot de la leyenda
    numComerciantesMapa = 4  # Número máximo de comerciantes por mapa y por columna de la leyenda
    numColumnasComerciante = int(np.ceil(numComerciantes / numComerciantesMapa))
    numLineasComerciante   = min(numComerciantes, numComerciantesMapa)

    # Ajustamos el tamaño del plot según el contenido que va a tener
    anchoTotal  = 5.2 + 1.5  * numColumnasComerciante
    alturaTotal = 3.6 + 0.75 * numLineasComerciante

    # Creamos el plot de la leyenda
    figLeyendaleg, ejeLeyenda = plt.subplots(figsize=(anchoTotal, alturaTotal))
    ejeLeyenda.axis('off')  # Ocultamos los ejes

    # ========================================
    #  SECCIÓN 1: COMERCIANTES
    # ========================================
    
    # Calculamos el ancho total esta sección
    anchoTotalComerciantes = numColumnasComerciante * separacionColumnas
    
    # Marcamos el punto horizontal inicial relativo para que las columnas queden centradas
    inicioEjeX = 0.5 - anchoTotalComerciantes/2
    
    # Creamos una variable que nos permite conocer la posición vertical relativa del plot en la que estamos trabajando, con un valor inicial
    posicionEjeY = 0.9
    
    # Añadimos el título de la sección y actualizamos la posición vertical relativa
    posicionEjeY = leyenda.titulo("COMERCIANTES", posicionEjeY, numSecciones, ejeLeyenda)
    
    # Almacenamos la posición vertical relativa de la primera fila
    inicioEjeY = posicionEjeY
    
    # Imprimimos todos los comerciantes que hay junto a un cuadro que muestra su color
    for c, color in enumerate(coloresComerciantes[:-1]):  # No llegamos al último color, ya que se usa únicamente para el símbolo de la leyenda; no es un comerciante más
        columna      = c // numComerciantesMapa                 # Calculamos la columna a la que pertenece
        fila         = c % numComerciantesMapa                  # Calculamos la fila a la que pertenece
        posicionEjeX = inicioEjeX + columna*separacionColumnas  # Calculamos la posición horizontal relativa
        
        if fila == 0:  # Si iniciamos una nueva columna...
            posicionEjeY = inicioEjeY  # Tomamos la posición vertical relativa de la primera fila
            
            if numColumnasComerciante > 1:  # Si hay más de una columna
                # Añadimos el identificador
                ejeLeyenda.text(posicionEjeX + 0.1, posicionEjeY, f"[{columna+1}/{numColumnasComerciante}]", transform=ejeLeyenda.transAxes, fontsize=13, ha='left', va='center')
                
                # Actualizamos la posición vertical relativa
                posicionEjeY -= espaciadoLineas
        
        # Representamos el color de cada comerciante
        ejeLeyenda.plot([posicionEjeX, posicionEjeX + anchoCuadro], [posicionEjeY, posicionEjeY], transform=ejeLeyenda.transAxes, color=coloresComerciantes[c], linewidth=3)
        ejeLeyenda.text(posicionEjeX + separacionSimbolo, posicionEjeY, f"Comerciante {c+1}", transform=ejeLeyenda.transAxes, fontsize=13, ha='left', va='center')
        
        # Actualizamos la posición vertical relativa
        posicionEjeY -= espaciadoLineas
        
    # Calculamos la nueva posición vertical relativa de trabajo, en función del número de filas que se hayan creado
    posicionEjeY = inicioEjeY - min(numComerciantes, numComerciantesMapa)*espaciadoLineas
    
    # Añadimos una línea horizontal de separación y actualizamos la posición vertical relativa
    posicionEjeY = leyenda.linea(posicionEjeY, numSecciones, ejeLeyenda)

    # ========================================
    #  SECCIÓN 2: ELEMENTOS DEL MAPA
    # ========================================
    
    # Añadimos el título de la sección y actualizamos la posición vertical relativa
    posicionEjeY = leyenda.titulo("ELEMENTOS DEL MAPA", posicionEjeY, numSecciones, ejeLeyenda)

    # Marcamos un nuevo punto horizontal relativo para iniciar la escritura y que quede centrado
    posicionEjeX = 0.3 + numColumnasComerciante*0.015

    # Escogemos un color de referencia para esta sección (elegimos el último, no representa ningún comerciante)
    colorRef = coloresComerciantes[-1]

    # Representamos el icono de la oficina
    ejeLeyenda.scatter(posicionEjeX + anchoCuadro/2, posicionEjeY, marker='s', s=100, color="green", edgecolors='black', transform=ejeLeyenda.transAxes)
    ejeLeyenda.text(posicionEjeX + separacionSimbolo, posicionEjeY, "Oficina", transform=ejeLeyenda.transAxes, fontsize=13, ha='left', va='center')

    # Actualizamos la posición vertical
    posicionEjeY -= espaciadoLineas

    # Representamos el icono de las tiendas
    ejeLeyenda.scatter(posicionEjeX + anchoCuadro/2, posicionEjeY, marker='o', s=80, c=colorRef, edgecolors='black', transform=ejeLeyenda.transAxes)
    ejeLeyenda.text(posicionEjeX + separacionSimbolo, posicionEjeY, "Tienda", transform=ejeLeyenda.transAxes, fontsize=13, ha='left', va='center')

    # Actualizamos la posición vertical
    posicionEjeY -= espaciadoLineas

    # Representamos el numero del orden de secuencia
    ejeLeyenda.text(posicionEjeX, posicionEjeY, " 1", transform=ejeLeyenda.transAxes, fontsize=13, ha='left', va='center')
    ejeLeyenda.text(posicionEjeX + separacionSimbolo, posicionEjeY, "Orden de visita", transform=ejeLeyenda.transAxes, fontsize=13, ha='left', va='center')

    # Actualizamos la posición vertical
    posicionEjeY -= espaciadoLineas

    # Representamos el icono de las rutas de los comerciantes
    ejeLeyenda.plot([posicionEjeX, posicionEjeX + anchoCuadro], [posicionEjeY, posicionEjeY], transform=ejeLeyenda.transAxes, color=colorRef, linewidth=3)
    ejeLeyenda.text(posicionEjeX + separacionSimbolo, posicionEjeY, "Ruta del comerciante", transform=ejeLeyenda.transAxes, fontsize=13, ha='left', va='center')

    # Añadimos un marco a toda la leyenda
    marco = mpatches.Rectangle((0.05, 0.05), 0.9, 0.9, transform=ejeLeyenda.transAxes, facecolor='none', edgecolor='gray', linewidth=2, linestyle='-')
    ejeLeyenda.add_patch(marco)

    # Mostramos el plot de la leyenda
    plt.show()


    ###################################################
    ######      BLOQUE 2: GRÁFICAS POR DÍA       ######
    ###################################################
    
    # Calculamos el número de mapas necesarios
    numMapas = int(np.ceil(numComerciantes / numComerciantesMapa))
    
    for d in range(numDias):

        for m in range(numMapas):
            
            # Definimos el primer y el último comerciante de este mapa
            primerComerc = m * numComerciantesMapa
            ultimoComerc = min(primerComerc + numComerciantesMapa, numComerciantes)
    
            # Creamos el mapa base
            fig, eje = utilidades.crearMapa(latitudes, longitudes)
           
            # Representamos la oficina
            utilidades.dibujarTienda(eje, 0, latitudes[0], longitudes[0], etiqueta="Oficina")
            
            trabajoComerc = False
            
            for c in range(primerComerc, ultimoComerc):
                
                if len(secuencias.get((c,d),[0])) <= 1:  # Si un comerciante no trabaja este día...
                    continue  # Pasamos al siguiente
                
                trabajoComerc = True
                
                # Obtenemos la secuencia específica
                secuencia = secuencias[(c,d)]
                    
                # Dibujamos la ruta completa por tramos
                for s in range(len(secuencia)-1):
                    t1, t2 = secuencia[s], secuencia[s+1]
    
                    ruta_str = rutas.loc[tiendas[t1], tiendas[t2]]  # Leemos la información de las rutas
                    ruta = json.loads(ruta_str)
    
                    # Dibujamos la ruta entre dos tiendas
                    utilidades.dibujarRuta(eje, ruta, color=coloresComerciantes[c])
    
                # Representamos la ubicación de las tiendas y el orden de visita
                for orden, i in enumerate(secuencia):
                    if i == 0:  # Si el índice es 0 (oficina)...
                        continue  # La ignoramos, ya la hemos representado
                    
                    utilidades.dibujarTienda(eje, i, latitudes[i], longitudes[i], color=coloresComerciantes[c], texto=str(orden))
            
            if not trabajoComerc:  # Si no trabaja ningún comerciante de este grupo...
                plt.close(fig)  # No mostramos el mapa
                continue
        
            if numMapas > 1:
                eje.set_title(f"Rutas de los Comerciantes - Día {d+1} [{m+1}/{numMapas}]")
            else:
                eje.set_title(f"Rutas de los Comerciantes - Día {d+1}")
            
            plt.show()
        
        
    ###################################################
    ######     BLOQUE 3: INFORMACIÓN ESCRITA     ######
    ###################################################

    presentacion.encabezadoSeccion("RUTAS DIARIAS DE CADA COMERCIANTE")
    
    # Mostramos la información de la oficina
    print(f"\n\t -- {nombres[0]} -- {direcciones[0]}")
    
    for d in range(numDias):
        print(f"\n\t   · DÍA {d+1}")
        for c in range(numComerciantes):
            print(f"\t\t  COMERCIANTE {c+1}")             
            
            if tiempoComercianteDia[c][d] != 0:
                horas, minutos = utilidades.formatoTiempo(tiempoComercianteDia[c][d])
                print("\t\t   ----------------------------------------------------")
                if horas == 0:
                    print(f"\t\t\t - Tiempo de trabajo: {minutos} min  \t(max: {tiempoMax} h)")
                else:
                    print(f"\t\t\t - Tiempo de trabajo: {horas} h {minutos} min  \t(max: {tiempoMax} h)")

                print(f"\t\t\t - Distancia recorrida: {distanciaComercianteDia[c][d]} km  \t(max: {distanciaMax} km)")
                print("\t\t   ----------------------------------------------------")

            secuencia = secuencias.get((c, d), [0])                            
            
            # Almacenamos las tiendas visitadas en orden
            destinos = [s for s in secuencia if s != 0]
            
            if len(destinos) != 0:  # Si se visita alguna tienda...
                cnt = 1  # Contador de destinos
                
                for s in destinos:  # Mostramos la secuencia de tiendas visitadas
                    print(f"\t\t\t· Destino {cnt}: {nombres[s]}  (Tienda {s})")
                    print(f"\t\t\t  - Dirección: {direcciones[s]}")
                    
                    cnt += 1  # Incrementamos el contador de destinos
    
            else:  # Si no se visita ninguna tienda...
                print("\t\t\t· Sin tiendas que visitar")




'''
    Muestra por pantalla un informe detallado del sueldo total de los comerciantes,
    incluyendo el desglose por días trabajados, horas trabajadas y comisiones,
    así como el salario individual de cada comerciante.

    Argumentos:
        - numComerciantes (int):               Número total de comerciantes.
        - sueldoTotal (float):                 Sueldo total acumulado de todos los comerciantes.
        - sueldoDiaTotal (float):              Parte del sueldo total correspondiente a los días trabajados.
        - sueldoHoraTotal (float):             Parte del sueldo total correspondiente a las horas trabajadas.
        - comisionTotal (float):               Parte del sueldo total correspondiente a las comisiones.
        - sueldoComerciante (list[float]):     Lista con el sueldo total de cada comerciante.
        - udsVendidasComerciante (list[int]):  Lista con las unidades vendidas por cada comerciante.
        - sueldoDiaComerciante (list[float]):  Lista con el sueldo por días trabajados de cada comerciante.
        - sueldoHoraComerciante (list[float]): Lista con el sueldo por horas trabajadas de cada comerciante.
        - comisionComerciante (list[float]):   Lista con la comisión obtenida por cada comerciante.
'''
def desgloseSueldos(numComerciantes, sueldoTotal, sueldoDiaTotal, sueldoHoraTotal, comisionTotal, sueldoComerciante, udsVendidasComerciante, sueldoDiaComerciante, sueldoHoraComerciante, comisionComerciante):    

    presentacion.encabezadoSeccion("DESGLOSE DE SUELDOS POR COMERCIANTE")
    
    print(f"\n\t · Sueldo Comerciantes: {sueldoTotal} €")
    print(f"\t\t- Sueldo por Días Trabajados = {sueldoDiaTotal} €")
    print(f"\t\t- Sueldo por Horas Trabajados = {sueldoHoraTotal} €")
    print(f"\t\t- Sueldo por Comisión = {comisionTotal} €")
    for c in range(numComerciantes):
        print("\t   --------------------------------------------------")
        print(f"\t\t · SUELDO COMERCIANTE {c+1}: {sueldoComerciante[c]} €")
        print(f"\t\t   - Uds vendidas = {udsVendidasComerciante[c]} unidades")
        print(f"\t\t   - Sueldo por Días Trabajados = {sueldoDiaComerciante[c]} €")
        print(f"\t\t   - Sueldo por Horas Trabajados = {sueldoHoraComerciante[c]} €")
        print(f"\t\t   - Sueldo por Comisión = {comisionComerciante[c]} €")