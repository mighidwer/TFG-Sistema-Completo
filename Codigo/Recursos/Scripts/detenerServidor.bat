::
:: ----------------------------------------------------------------------------------------------------
:: Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"
::
:: Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)
::
:: @author: Miguel Hidalgo Wert
:: ----------------------------------------------------------------------------------------------------
::
::  · detenerServidor.bat
::
::     Este script detiene el servidor OSRM (OpenStreetMap), finalizando el proceso asociado al
::     servicio de enrutamiento y verificando si la operación se ha realizado correctamente.
::

@echo off
set ESPACIO=------------------------------------------------------------------------------------------



echo(
echo %ESPACIO%
echo  === Deteniendo OSRM ===
echo %ESPACIO%
taskkill /F /IM osrm-routed.exe



:: Comprobamos si el servidor se ha detenido correctamente
if %errorlevel% neq 0 (
    echo(
    echo %ESPACIO%
    echo  No se pudo detener OSRM o ya estaba cerrado.
    echo %ESPACIO%
) else (
    echo(
    echo %ESPACIO%
    echo  OSRM detenido con éxito.
    echo %ESPACIO%
)