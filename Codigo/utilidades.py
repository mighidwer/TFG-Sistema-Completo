# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · utilidades.py

    Este fichero contiene funciones generales que se utilizan a lo largo del proyecto.
    
"""

# Importación de librerías estándar
import shutil
import os

# Importación de dependencias externas
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd



###################################### CARGA Y GESTIÓN DE DATOS #######################################

'''
    Obtiene la información de las tiendas desde un archivo Excel.

    Devuelve:
        - tuple: (nombres, direcciones, tipos, latitudes, longitudes), donde:
            - nombres (pd.Series[str]):      Nombres de las tiendas.
            - direcciones (pd.Series[str]):  Direcciones de las tiendas.
            - tipos (pd.Series[str]):        Tipos de tiendas.
            - latitudes (pd.Series[float]):  Latitudes de las tiendas.
            - longitudes (pd.Series[float]): Longitudes de las tiendas.
'''
def obtenerInfo():
    
    # Verificamos si ya estamos dentro del directorio 'Recursos'
    if os.path.basename(os.getcwd()) != "Recursos":
        os.chdir(os.path.join(os.getcwd(), "Recursos"))

    df = pd.read_excel('DatosTiendas/infoTiendas.xlsx', sheet_name='Coordenadas', skiprows=2)
    
    nombres     = df.iloc[:,1]  # Lectura de la columna NOMBRE
    direcciones = df.iloc[:,2]  # Lectura de la columna DIRECCIÓN
    tipos       = df.iloc[:,3]  # Lectura de la columna TIPO
    latitudes   = df.iloc[:,4]  # Lectura de la columna LATITUD
    longitudes  = df.iloc[:,5]  # Lectura de la columna LONGITUD
             
    return nombres, direcciones, tipos, latitudes, longitudes  # Devolvemos la información de las tiendas




'''
    Muestra un listado de todas las tiendas con su información.

    Argumentos:
        - nombres (pd.Series[str]):      Lista con los nombres de las tiendas.
        - direcciones (pd.Series[str]):  Lista con las direcciones de las tiendas.
        - tipos (pd.Series[str]):        Lista con los tipos de las tiendas
        - latitudes (pd.Series[float]):  Lista con las latitudes de las tiendas.
        - longitudes (pd.Series[float]): Lista con las longitudes de las tiendas.
'''
def listarTiendas(nombres, direcciones, tipos, latitudes, longitudes):

    # Definimos el símbolo para separar las tiendas en la lista
    simbolo = "- "
    
    # Calculamos el ancho de la consola en función de la longitud del símbolo
    ancho = shutil.get_terminal_size().columns // len(simbolo)
    
    print("\n\t   NÚMERO TOTAL DE TIENDAS =", len(nombres)-1)
    
    for i in range(len(nombres)):
        
        print("\n" + simbolo * ancho)
        
        if i == 0:
            print("\n\t   🏢 OFICINA CENTRAL")
        else:
            print("\n\t   🏪 TIENDA", i)
            
        print("\t    - Nombre:", nombres[i])
        print("\t    - Dirección:", direcciones[i])
        print("\t    - Tipo:", tipos[i])
        #print("\t    - Latitudes:", latitudes[i])
        #print("\t    - Longitudes:", longitudes[i])




'''
    Permite al usuario seleccionar dos tiendas válidas.

    Argumentos:
        - nombres (pd.Series[str]): Lista con los nombres de las tiendas.

    Devuelve:
        - tuple: (t1, t2), donde:
            - t1 (int): Índice de la tienda de partida.
            - t2 (int): Índice de la tienda de destino.
'''
def seleccionarTiendas(nombres):
    
    numTiendas = len(nombres)-1
    print("\n\t  *Introduce \"0\" para seleccionar la oficina*")
    
    # Selección de la tienda de partida
    t1 = None
    while t1 is None:
        t1 = input(f"\t ¿Cuál es la TIENDA DE PARTIDA? (1-{numTiendas}): ")
        # Comprobamos si la entrada es un número
        if t1.isdigit():
            # Comprobamos si está dentro del rango
            if int(t1) > numTiendas:
                print("\t  *Tienda inexistente*")
                t1 = None
        else:
            print("\t  *Entrada no válida*")
            t1 = None
    
    # Selección de la tienda de destino
    t2 = None
    while t2 is None:
        t2 = input(f"\t ¿Cuál es la TIENDA DE DESTINO? (1-{numTiendas}): ")
        # Comprobamos si la entrada es un número
        if t2.isdigit():
            # Comprobamos si está dentro del rango
            if int(t2) > numTiendas:
                print("\t  *Tienda inexistente*")
                t2 = None
            # Comprobamos que no sea la misma tienda que t1
            if t2 != None and int(t2) == int(t1):
                print("\t  *Selecciona una tienda diferente a la de partida*")
                t2 = None
        else:
            print("\t  *Entrada no válida*")
            t2 = None
    
    return int(t1), int(t2)  # Devolvemos los índices de las tiendas seleccionadas




################################ FUNCIONES AUXILIARES DE VISUALIZACIÓN ################################

'''
    Crea y configura la figura base del mapa de Sevilla.

    Argumentos:
        - latitudes (list[float]):  Lista de latitudes de las tiendas.
        - longitudes (list[float]): Lista de longitudes de las tiendas.

    Devuelve:
        - tuple:
            - fig (matplotlib.figure.Figure): Figura creada.
            - eje (matplotlib.axes.Axes):     Ejes del gráfico.
'''
def crearMapa(latitudes, longitudes):

    # Cargamos la imagen del mapa de Sevilla
    mapa_img = mpimg.imread("Imagenes/sevilla.png")

    # Definimos los límites geográficos del mapa
    lat_min, lat_max = 37.373625, 37.406949
    lon_min, lon_max = -6.013400, -5.954082

    # Creamos la figura
    fig, eje = plt.subplots(figsize=(8, 6))

    # Mostramos el mapa en el fondo
    eje.imshow(mapa_img, extent=[lon_min, lon_max, lat_min, lat_max], aspect='auto')
    
    # Definimos los límites de representación sin salirnos de la imagen del mapa
    margen = 0.0025
    x_min = max(min(longitudes) - margen, lon_min)
    x_max = min(max(longitudes) + margen, lon_max)
    y_min = max(min(latitudes) - margen, lat_min)
    y_max = min(max(latitudes) + margen, lat_max)

    # Ajustamos los ejes
    eje.set_xlim(x_min, x_max)
    eje.set_ylim(y_min, y_max)

    # Mantenemos la escala 1:1 entre los ejes
    eje.set_aspect(1)

    # Etiquetas de los ejes
    eje.set_xlabel("Longitud")
    eje.set_ylabel("Latitud")

    return fig, eje




'''
    Representa una ruta sobre el mapa.

    Argumentos:
        - eje (matplotlib.axes.Axes):      Ejes del gráfico.
        - ruta (list[tuple[float,float]]): Coordenadas de la ruta.
        - color (str, opcional):           Color de la línea.
        - etiqueta (str, opcional):        Etiqueta para la leyenda.
'''
def dibujarRuta(eje, ruta, color="blue", etiqueta=None):

    # Desempaquetamos las coordenadas
    ruta_lon, ruta_lat = zip(*ruta)

    # Dibujamos la ruta
    eje.plot(ruta_lon, ruta_lat, linestyle='-', linewidth=2, color=color, label=etiqueta, zorder=1)




'''
    Representa una tienda u oficina sobre el mapa.

    Argumentos:
        - eje (matplotlib.axes.Axes): Ejes del gráfico.
        - i (int):                    Identificador de la tienda.
        - latitud (float):            Latitud.
        - longitud (float):           Longitud.
        - color (str, opcional):      Color personalizado.
        - etiqueta (str, opcional):   Etiqueta para la leyenda.
        - texto (str, opcional):      Texto mostrado junto al marcador.
'''
def dibujarTienda(eje, i, latitud, longitud, color=None, etiqueta=None, texto=None):

    # Configuración automática
    if i == 0:  # Para la oficina...
        color = "green" if color is None else color  # color = "#70E800" if color is None else color
        marcador = 's'

    else:  # Para las tiendas...
        color = "red" if color is None else color
        marcador = 'o'

    # Dibujamos marcador
    eje.scatter(longitud, latitud, c=color, marker=marcador, edgecolors='black', s=60, label=etiqueta, zorder=2)

    # Texto opcional
    if texto is not None:

        eje.text(longitud + 0.0002, latitud + 0.0003, texto, fontsize=10, fontweight='bold', color='black', zorder=3)




####################################### FORMATO Y VISUALIZACIÓN #######################################

'''
    Representa en un mapa las tiendas y, si se especifican, la ruta entre dos tiendas.

    Argumentos:
        - latitudes (list[float]):                   Lista de latitudes de las tiendas.
        - longitudes (list[float]):                  Lista de longitudes de las tiendas.
        - modo (str, opcional):                      Modo de desplazamiento. Si se especifica, se representa la ruta.
        - nombres (list[str], opcional):             Lista de nombres de las tiendas.
        - t1 (int, opcional):                        Índice de la tienda de partida.
        - t2 (int, opcional):                        Índice de la tienda de destino.
        - distancia (float):                         Distancia en kilómetros entre las dos tienda.
        - horas (int):                               Horas estimadas de la ruta entre las dos tiendas.
        - minutos (int):                             Minutos adicionales de la ruta entre las dos tiendas.
        - ruta (list[tuple[float,float]], opcional): Lista de coordenadas (longitud, latitud) de la ruta entre las dos tiendas.
'''
def mapa(latitudes, longitudes, modo=None, nombres=None, t1=None, t2=None, distancia=None, horas=None, minutos=None, ruta=None):

    # Creamos el mapa base
    fig, eje = crearMapa(latitudes, longitudes)
    
    # Si no se especifica el modo de desplazamiento, mostramos la oficina y todas las tiendas
    if modo is None:
        # Mostramos la oficina
        dibujarTienda(eje, 0, latitudes[0], longitudes[0], etiqueta="Oficina")
        
        # Mostramos todas las tiendas junto a su marcador identificativo
        for i in range(1, len(latitudes)):
            dibujarTienda(eje, i, latitudes[i], longitudes[i], etiqueta="Tiendas" if i == 1 else None, texto=str(i))
        
        eje.set_title("UBICACIÓN DE LAS TIENDAS EN SEVILLA")
    
    # Si se especifica el modo de desplazamiento, dibujamos la ruta y las tiendas seleccionadas
    else:
        
        # Representamos el origen y el destino de la ruta
        dibujarTienda(eje, t1, latitudes[t1], longitudes[t1], etiqueta="Oficina" if t1 == 0 else "Tienda", texto="INICIO")
        dibujarTienda(eje, t2, latitudes[t2], longitudes[t2], etiqueta="Oficina" if t2 == 0 else "Tienda", texto="FINAL")
        
        # Representamos la ruta
        dibujarRuta(eje, ruta, etiqueta="Ruta")
        
        eje.set_title(f"{nombres[t1]} - {nombres[t2]}")
    
        # Mostramos la información de la ruta en la parte inferior del mapa
        if horas == 0:
            info = f"Distancia: {distancia} km | Tiempo: {minutos} min"
        else:    
            info = f"Distancia: {distancia} km | Tiempo: {horas} h {minutos} min"
        
        eje.text(0.5, 0.075, f"Modo de Desplazamiento: {modo}", transform=eje.transAxes, fontsize=11,
                    ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.6))
        
        eje.text(0.5, 0.02, info, transform=eje.transAxes, fontsize=11,
                    ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.6))
    # Mostramos la leyenda del mapa
    eje.legend()
        
    # Mostramos el mapa con las tiendas
    plt.show()




'''
    Convierte el dato del tiempo al formato horas y minutos.
    
    Argumentos:
        - tiempo (float): Tiempo en formato de horas (con decimales).

    Devuelve:
        - tuple: (horas, minutos), donde:
            - horas (int):   Horas enteras.
            - minutos (int): Minutos adicionales.
'''
def formatoTiempo(tiempo):
    
    horas = int(tiempo)                 # Parte entera de la duración (horas)
    minutos = round((tiempo-horas)*60)  # Convertimos la parte decimal a minutos
    
    return horas, minutos