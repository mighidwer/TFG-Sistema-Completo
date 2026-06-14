# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · presentacion.py

    Este fichero agrupa todas las funciones relacionadas con la presentación
    por consola de los distintos elementos del sistema.
    
"""

# Importación de librerías estándar
import shutil



#################################### UTILIDADES DE REPRESENTACIÓN #####################################

'''
    Obtiene el ancho del terminal.

    Devuelve:
        - ancho (int): Número de columnas del terminal.
'''
def definirAncho():
    
    ancho = shutil.get_terminal_size().columns
    
    return ancho




'''
    Devuelve la indentación correspondiente al nivel del menú.

    Argumentos:
        - nivel (int): Nivel del menú (1 → Menú principal, 2 → Submenú).

    Devuelve:
        - str: Cadena de tabulaciones/espacios para alinear texto.
'''
def indentacionMenu(nivel):

    if nivel == 1:
        return "\t\t"
    elif nivel == 2:
        return "\t\t   "
    
    return "\t\t"




######################################## TÍTULOS Y ENCABEZADOS ########################################

'''
    Muestra un título centrado con un borde decorativo.

    Argumentos:
        - texto (str):   Texto del título.
        - simbolo (str): Símbolo decorativo del borde.
'''
def tituloMenu(texto, simbolo):
    
    ancho = definirAncho()
    
    print("\n\n" + simbolo * ancho)
    print(texto.center(ancho))
    print(simbolo * ancho + "\n")




'''
    Muestra un encabezado de la sección.

    Argumentos:
        - texto (str): Texto del encabezado de la sección.
'''
def encabezadoSeccion(texto):
    
    print("\n\t" + "-" * (len(texto) + 12))
    print(f"\t----- {texto} -----")
    print("\t" + "-" * (len(texto) + 12))




'''
    Muestra un mensaje destacado entre líneas separadoras para indicar
    el inicio de un nuevo proceso dentro de la aplicación.

    Argumentos:
        - texto (str): Mensaje que se muestra por pantalla.
'''
def mostrarProceso(texto):

    ancho = definirAncho()
    
    print("\n" + "=" * ancho)
    print(f"\n\t{texto}")
    print("\n" + "=" * ancho)




################################################ MENÚS ################################################

'''
    Muestra el menú principal de la aplicación.

    Devuelve:
        - opcion (str): Opción seleccionada por el usuario.
'''
def menuMain():
    ancho = definirAncho()
    print("\n\n" + "=" * ancho)
    print("TRABAJO FIN DE GRADO".center(ancho))
    print("Optimización de rutas de operadores en sistemas logísticos".center(ancho))
    print("\n" + "Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)".center(ancho))
    print("Autor: Miguel Hidalgo Wert".center(ancho))
    print("=" * ancho + "\n")
    print("   1. APLICACIÓN 'BUSCAR RUTAS'")
    print("   2. SIMULACIÓN SIMPLE")
    print("   3. SIMULACIÓN MPC")
    print("   4. SALIR")
    opcion = input("\t - Selecciona una opción: ")
    
    return opcion




'''
    Menú de selección de modelos alternativos.
    
    Argumentos:
        - mpc (bool): Indica si estamos en simulación MPC (True) o simple (False).

    Devuelve:
        - opcion (str): Opción seleccionada por el usuario.
'''
def menuModelos(mpc):
    
    # Definimos el tipo de simulación
    modo = "MPC" if mpc else "SIMPLE"
    
    tituloMenu(f"SIMULACIÓN {modo} - MODELOS DISPONIBLES", "-")
    print("\t  1. MODELO DE OPTIMIZACIÓN")
    print("\t  2. MODELO ALEATORIO")
    print("\t  3. MODELO SECUENCIAL")
    print("\t  4. MODELO GREEDY")
    print("\t  5. VOLVER ATRÁS")
    opcion = input("\t\t- Selecciona una opción: ")
    
    return opcion




'''
    Menú de la aplicación "BUSCAR RUTAS".

    Devuelve:
        - opcion (str): Opción seleccionada por el usuario.
'''
def menuBuscarRutas():
    
    tituloMenu("APLICACIÓN 'BUSCAR RUTAS'", "#")
    print("   1. VER LISTADO DE TIENDAS DEL CENTRO DE SEVILLA")
    print("   2. CALCULAR RUTA ENTRE DOS TIENDAS")
    print("   3. SALIR")
    opcion = input("\t - Selecciona una opción: ")
    
    return opcion
    
    


'''
    Menú de información del modelo de optimización.

    Devuelve:
        - opcion (str): Opción seleccionada por el usuario.
'''
def menuOptimizacion():

    tituloMenu("INFORMACIÓN DEL MODELO", "#")
    print("   1. INFORME MODELO MATEMÁTICO")
    print("   2. INFORME VENTAS")
    print("   3. INFORME COMERCIANTES")
    print("   4. SALIR")
    opcion = input("\t - Selecciona una opción: ")
    
    return opcion




'''
    Menú del informe de ventas.

    Devuelve:
        - opcion (str): Opción seleccionada por el usuario.
'''
def menuVentas():

    tituloMenu("INFORME VENTAS", "-")
    print("\t  1. EVOLUCIÓN DEL STOCK DE LAS TIENDAS")
    print("\t  2. DESGLOSE DE VENTAS E INGRESOS")
    print("\t  3. VOLVER ATRÁS")
    opcion = input("\t\t- Selecciona una opción: ")
    
    return opcion




'''
    Menú del informe de comerciantes.

    Devuelve:
        - opcion (str): Opción seleccionada por el usuario.
'''
def menuComerciantes():

    tituloMenu("INFORME COMERCIANTES", "-")
    print("\t  1. RUTAS DIARIAS DE CADA COMERCIANTE")
    print("\t  2. DESGLOSE DE SUELDOS POR COMERCIANTE")
    print("\t  3. VOLVER ATRÁS")
    opcion = input("\t\t- Selecciona una opción: ")
    
    return opcion




'''
    Muestra un mensaje relacionado con la navegación
    de los menús de la aplicación.

    Argumentos:
        - mensaje (str):         Tipo de mensaje.
        - nivel (int, opcional): Nivel del menú (1 → Menú principal, 2 → Submenú).
'''
def mensajeMenu(mensaje, nivel=1):

    mensajes = {
        "OPCION_NO_VALIDA": "*Opción no válida*",
        "CERRANDO": "*Cerrando programa*"
    }

    texto = mensajes[mensaje]

    print(f"{indentacionMenu(nivel)}{texto}")