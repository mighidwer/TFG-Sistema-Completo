# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · leyenda.py

    Este fichero contiene funciones para ajustar los parámetros comunes de las leyendas,
    representar elementos repetitivos y gestionar la elección de colores y tonos.
 
"""

# Importación de librerías estándar
import colorsys

# Importación de dependencias externas
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt



######################################### FUNCIONES GENERALES #########################################

'''
    Crea una portada, mostrando un título centrado.

    Argumentos:
        - titulo (str):    Texto principal de la portada.
        - ancho (float):   Ancho de la figura.
        - alto (float):    Alto de la figura.
'''
def portada(titulo, ancho=8, alto=4):

    # Creamos el plot de la portada
    fig, eje = plt.subplots(figsize=(ancho, alto))
    eje.axis("off")  # Ocultamos los ejes

    # Título principal
    eje.text(0.5, 0.55, titulo, ha="center", va="center", fontsize=22, fontweight="bold", 
            bbox=dict(boxstyle="round,pad=0.7", edgecolor="black", facecolor="#f0f0f0", linewidth=2))

    plt.show()




######################################### PARÁMETROS LEYENDA ##########################################

'''
    Ajusta los parámetros comunes de las leyendas.
    
    Argumentos:
        - numSecciones (int): Número de secciones que tendrá la leyenda.
        
    Devuelve:
        - tuple: (espaciadoLineas, anchoCuadro, alturaCuadro, separacionSimbolo, separacionColumnas), donde:
            - espaciadoLineas (float):    Separación vertical entre líneas continuas.
            - anchoCuadro (float):        Anchura de los cuadros utilizados para representar los iconos de los elementos.
            - alturaCuadro (float):       Altura de los cuadros utilizados para representar los iconos de los elementos.
            - separacionSimbolo (float):  Separación horizontal entre un elemento de la leyenda y su símbolo.
            - separacionColumnas (float): Separación horizontal entre columnas.
'''
def parametrosLeyenda(numSecciones):
    # Ajustamos el espaciado entre las líneas
    espaciadoLineas = 0.14 / numSecciones
    
    # Ajustamos el tamaño de los recuadros pequeños de la leyenda
    anchoCuadro  = 0.04
    alturaCuadro = 0.075 / numSecciones
    
    # Separación horizontal relativa entre un elemento de la leyenda y su símbolo
    separacionSimbolo = 0.06
    
    # Separación horizontal relativa de las columnas
    separacionColumnas = 0.69 / numSecciones
    
    return espaciadoLineas, anchoCuadro, alturaCuadro, separacionSimbolo, separacionColumnas




########################################## ELEMENTOS LEYENDA ##########################################

'''
    Escribe el título de una sección dentro del gráfico de la leyenda
    y actualiza la posición vertical para el siguiente elemento.

    Argumentos:
        - seccion (str):                 Texto del título de la sección.
        - posicionEjeY (float):          Posición vertical actual del eje Y (en coordenadas relativas).
        - numSecciones (int):            Número de secciones que tendrá la leyenda.
        - ax_leg (matplotlib.axes.Axes): Eje donde se escribe el título.

    Devuelve:
        - posicionEjeY (float): Nueva posición vertical (ejeY) actualizada para continuar añadiendo elementos.
'''
def titulo(seccion, posicionEjeY, numSecciones, ax_leg):
    # Leemos los parámetros necesarios
    espaciadoLineas = parametrosLeyenda(numSecciones)[0]
    
    # Escribimos el título de la sección
    ax_leg.text(0.5, posicionEjeY, seccion, transform=ax_leg.transAxes, fontsize=14, fontweight='bold', ha='center', va='center')
    
    # Ajustamos la nueva altura de trabajo
    posicionEjeY -= espaciadoLineas * 1.2
    
    return posicionEjeY  # Devolvemos la nueva posición vertical




'''
   Dibuja un recuadro de color en la leyenda junto con su texto descriptivo
   y actualiza la posición vertical para el siguiente elemento.

   Argumentos:
       - texto (str):                   Descripción del elemento representado.
       - color (str):                   Color de relleno del recuadro.
       - posicionEjeX (float):          Posición horizontal del recuadro (en coordenadas relativas).
       - posicionEjeY (float):          Posición vertical actual (en coordenadas relativas).
       - numSecciones (int):            Número de secciones que tendrá la leyenda.
       - ax_leg (matplotlib.axes.Axes): Eje donde se dibuja el recuadro.
       - hatch (str, opcional):         Patrón de relleno (por defecto vacío).

   Devuelve:
       - posicionEjeY (float): Nueva posición vertical (ejeY) actualizada para continuar añadiendo elementos.
'''
def cuadro(texto, color, posicionEjeX, posicionEjeY, numSecciones, ax_leg, hatch=""):
    # Leemos los parámetros necesarios
    espaciadoLineas, anchoCuadro, alturaCuadro, separacionSimbolo, *_ = parametrosLeyenda(numSecciones)
    
    # Representamos el recuadro junto a su texto
    rect = mpatches.Rectangle((posicionEjeX, posicionEjeY - alturaCuadro/2), anchoCuadro, alturaCuadro, transform=ax_leg.transAxes, facecolor=color, edgecolor='black', hatch=hatch)
    ax_leg.add_patch(rect)
    ax_leg.text(posicionEjeX + separacionSimbolo, posicionEjeY, texto, transform=ax_leg.transAxes, fontsize=13, ha='left', va='center')
    
    # Ajustamos la nueva altura de trabajo
    posicionEjeY -= espaciadoLineas
    
    return posicionEjeY  # Devolvemos la nueva posición vertical




'''
    Dibuja una línea divisoria horizontal entre secciones de la leyenda
    y actualiza la posición vertical para el siguiente elemento.

    Argumentos:
        - posicionEjeY (float):          Posición vertical actual (en coordenadas relativas).
        - numSecciones (int):            Número de secciones que tendrá la leyenda.
        - ax_leg (matplotlib.axes.Axes): Eje donde se dibuja la línea divisoria.

    Devuelve:
        - posicionEjeY (float): Nueva posición vertical (ejeY) actualizada para continuar añadiendo elementos.
'''
def linea(posicionEjeY, numSecciones, ax_leg):
    # Leemos los parámetros necesarios
    espaciadoLineas = parametrosLeyenda(numSecciones)[0]
    
    # Dibujamos la línea divisoria
    posicionEjeY -= espaciadoLineas * 0.5
    ax_leg.plot([0.08, 0.92], [posicionEjeY, posicionEjeY], transform=ax_leg.transAxes, color="gray", lw=1.5, ls="-", alpha=0.7)

    posicionEjeY -= espaciadoLineas * 1.5
    
    return posicionEjeY  # Devolvemos la nueva posición vertical




######################################### GESTIÓN DE COLORES ##########################################

'''
    Genera una lista de colores a utilizar en función del número de elementos pasado como argumento.

    Argumentos:
        - numElementos (int):     Número de elementos a los que se les debe asignar un color.
        - tonos (bool, opcional): Habilita (True) o no (False) la creación de distintos tonos de cada color.
        - uso (str, opcional):    Define el uso de la paleta de colores a utilizar, permitiendo personalizarla.

    Devuelve:
        - colores (list[str] | list[dist[str, str]]): Lista de colores, uno para cada elemento.
            - Si tonos = False -> list[str]
            - Si tonos = True  -> list[dist[str, str]]
'''
def generarColores(numElementos, tonos=False, uso="stock"):
    # Paleta de colores base que se va a utilizar en las gráficas
    coloresBase = [
        "#1f77b4",  # Azul
        "#2ca02c",  # Verde
        "#d62728",  # Rojo
        "#fde208",  # Amarillo
        "#8f1fcf",  # Morado
        "#ff7f0e",  # Naranja
        "#8c564b",  # Marrón
    ]
    
    # Si los colores son para comerciantes, eliminamos varios colores de la paleta
    if uso == "comerciantes":
        coloresBase.pop(5)  # Posición del color naranja
        coloresBase.pop(4)  # Posición del color morado
        coloresBase.pop(1)  # Posición del color verde
    
    colores = []  # Lista de colores que se van a usar
    for i in range(numElementos):
        base = coloresBase[i % len(coloresBase)]  # Por si nos pasamos del límite de colores, volvemos al primero
        
        if tonos:  # Si se quieren tener distintos tonos del mismo color...
            # Añadimos todos los tonos del color a la lista
            colores.append(generarTonos(base))
            
        else:  # Si no se quieren generar distintos tonos...
            # Añadimos sólo el color base a la lista
            colores.append(base)
    
    return colores




'''
    Crea un conjunto de tres tonos a partir de un color base.

    Argumentos:
        - base (str): Código hexadecimal del color base.

    Devuelve:
        - dict[str, str]: Diccionario con los tonos generados:
            + "stock":  Tono original.
            + "compra": Tono más claro.
            + "venta":  Tono más oscuro.
'''
def generarTonos(base):
    return {  # Devuelve el color base (stock) y sus modificaciones (compra y venta)
        "stock": base,
        "compra": ajustarTono(base, factorLuz=1.35, factorSat=0.95),
        "venta": ajustarTono(base, factorLuz=0.75, factorSat=1.15)
    }




'''
    Modifica la luminosidad y saturación de un color dado, generando un nuevo tono.

    Argumentos:
        - base (str):        Código hexadecimal del color base a ajustar.
        - factorLuz (float): Valor para la luminosidad.
        - factorSat (float): Valor para la saturación.

    Devuelve:
        - str: Código hexadecimal del color ajustado tras modificar la luminosidad y la saturación.
'''
def ajustarTono(base, factorLuz, factorSat):
    # Obtenemos los datos rgb del color base
    rgb = mcolors.hex2color(base)
    h, l, s = colorsys.rgb_to_hls(*rgb)
    # Y ajustamos la luz y la saturación para cambiar el tono según corresponda
    l = min(1, max(0, l * factorLuz))
    s = min(1, max(0, s * factorSat))
    
    return mcolors.to_hex(colorsys.hls_to_rgb(h, l, s))  # Devolvemos el código hexadecimal del nuevo tono generado