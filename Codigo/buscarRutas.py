# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"

Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)

@author: Miguel Hidalgo Wert
----------------------------------------------------------------------------------------------------

 · buscarRutas.py

    Este fichero contiene la aplicación "BUSCAR RUTAS" que nos permite consultar al servidor OSRM
    para obtener la distancia, el tiempo y la ruta entre dos tiendas, además de poder comprobar
    un listado con la información de cada una de las tiendas existentes.
    
"""

# Importación de módulos propios del proyecto
import presentacion
import utilidades
import osrm



'''
    Ejecuta la aplicación "BUSCAR RUTAS", que permite consultar rutas entre tiendas
    utilizando el servidor OSRM y visualizar los resultados.

    La función actúa como controlador principal del flujo de la aplicación:

        - Carga los datos de las tiendas.
        - Muestra el menú de interacción al usuario.
        - Permite:
            1. Visualizar listado de tiendas.
            2. Calcular distancia, tiempo y ruta entre dos tiendas.
            3. Salir de la aplicación.
'''
def ejecutarApp():
            
    # Obtenemos la información de las tiendas
    nombres, direcciones, tipos, latitudes, longitudes = utilidades.obtenerInfo()
    
    while True:

        opcion = presentacion.menuBuscarRutas()
        
        
        if opcion == "1":  # VER LISTADO DE LAS TIENDAS
            
            graf = input("\n\t ¿Desea ver la representación de las tiendas en el mapa? (s/n): ")
            if graf.lower() == "s":  # Si se quieren mostrar las tiendas
                utilidades.mapa(latitudes, longitudes)
                
            # Listamos todas las tiendas junto a su información
            utilidades.listarTiendas(nombres, direcciones, tipos, latitudes, longitudes)


        elif opcion == "2":  # CALCULAR EL TIEMPO ENTRE DOS TIENDAS
        
            # Seleccionamos las tiendas que vamos a consultar
            t1, t2 = utilidades.seleccionarTiendas(nombres)
            
            modo = None
            
            while modo != "foot" and modo != "bike":
                # Menú que se muestra por pantalla para seleccionar el modo de desplazamiento
                
                print("\n\t· Modos de desplazamiento disponibles: (1) A pie / (2) En bici")                        
                opcionModo = input("\t  - Selecciona el modo de desplazamiento: ")
                
                if opcionModo == "1":
                    modo = "foot"
                    
                elif opcionModo == "2":                            
                    modo = "bike"
                
                else:
                    print("\t\t *Modo no válido*")
                    
            try:
                # Iniciamos el servidor correspondiente al modo de desplazamiento elegido
                osrm.iniciarServidor(modo)
                
                # Realizamos la consulta
                distancia, tiempo, ruta = osrm.obtenerRuta(modo, latitudes[t1], longitudes[t1], latitudes[t2], longitudes[t2])
                
                # Transformamos el tiempo obtenido en la consulta al formato horas y minutos
                horas, minutos = utilidades.formatoTiempo(tiempo)
                
                graf = input("\n\t  ¿Desea ver la ruta entre las tiendas en el mapa? (s/n): ")
                if graf.lower() == "s":  # Si se quiere ver la ruta entre las tiendas
                    utilidades.mapa(latitudes, longitudes, modo, nombres, t1, t2, distancia, horas, minutos, ruta)
                
                print(f"\n\t{'TIENDA DE PARTIDA:':>21} {nombres[t1]} [{direcciones[t1]}]")
                print(f"\t{'TIENDA DE DESTINO:':>21} {nombres[t2]} [{direcciones[t2]}]")
                print(f"\t{'DISTANCIA:':>21} {distancia} km")
                if horas == 0:
                    print(f"\t{'TIEMPO:':>21} {minutos} min")
                else:
                    print(f"\t{'TIEMPO:':>21} {horas} h {minutos} min")
                
            finally:
                # Detenemos el servidor tras la consulta
                osrm.detenerServidor()

            
        elif opcion == "3":  # SALIR
            presentacion.mensajeMenu("CERRANDO")
            break
        
        
        else:
            presentacion.mensajeMenu("OPCION_NO_VALIDA")