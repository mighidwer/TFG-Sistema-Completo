::
:: ----------------------------------------------------------------------------------------------------
:: Trabajo Fin de Grado: "Optimización de rutas de operadores en sistemas logísticos"
::
:: Grado en Ingeniería de las Tecnologías de Telecomunicación (GITT)
::
:: @author: Miguel Hidalgo Wert
:: ----------------------------------------------------------------------------------------------------
::
::  · iniciarServidor.bat
::
::     Este script inicia el servidor OSRM (OpenStreetMap). En función del perfil seleccionado
::     (foot o bike), realiza la validación de parámetros, prepara los datos necesarios, ejecuta
::     los procesos de extracción y construcción de la red de enrutamiento cuando es necesario y,
::     finalmente, pone en marcha el servidor OSRM en el puerto correspondiente.
::

@echo off
set ESPACIO=------------------------------------------------------------------------------------------
:: Nos colocamos en el directorio padre Recursos/
set BASEDIR=%~dp0..
:: Normalizamos la ruta del directorio
for %%i in ("%BASEDIR%") do set BASEDIR=%%~fi



:: =========================
:: Validación del parámetro
:: =========================

:: Verificamos si se ha introducido el parámetro necesario para iniciar el servidor
if "%1"=="" (
    echo(
    echo %ESPACIO%
    echo  Uso: iniciarServidor.bat ^<foot^|bike^>
    echo %ESPACIO%
    exit /b 1
)

:: Verificamos si se ha introducido un modo válido como parámetro
set MODO=%1

if not "%MODO%"=="foot" if not "%MODO%"=="bike" (
    echo(
    echo %ESPACIO%
    echo  Modo no valido: %MODO%
    echo  Modos permitidos: foot, bike
    echo %ESPACIO%
    exit /b 1
)



:: =========================
:: Configuración
:: =========================

:: Definimos las variables en función del modo elegido
set MAPA=%BASEDIR%\OSRM\maps\sevilla.osm.pbf
set DATA=%BASEDIR%\OSRM\data\%MODO%


if "%MODO%"=="foot" (
    set LUA=%BASEDIR%\OSRM\profiles\foot.lua
    set PUERTO=5000
) else if "%MODO%"=="bike" (
    set LUA=%BASEDIR%\OSRM\profiles\bicycle.lua
    set PUERTO=5001
)


set OSRMFILE=%DATA%\sevilla.osrm

if not exist "%DATA%" mkdir "%DATA%"

echo(
echo %ESPACIO%
echo  === MODO SELECCIONADO: %MODO% ===
echo %ESPACIO%



:: =========================
:: Extracción de datos
:: =========================

:: Verificamos si el archivo OSRM ya ha sido extraído
if not exist "%DATA%\sevilla.osrm.names" (
    echo(
    echo %ESPACIO%
    echo  === Extrayendo datos con perfil "%MODO%" ===
    echo %ESPACIO%

    :: Copiamos el mapa a la carpeta del perfil
    copy "%MAPA%" "%DATA%\sevilla.osm.pbf" >nul

    pushd "%DATA%"
    "%BASEDIR%\OSRM\osrm-extract.exe" -p "%LUA%" "sevilla.osm.pbf"
    popd
) else (
    echo(
    echo %ESPACIO%
    echo  === Los datos con perfil "%MODO%" ya han sido extraidos ===
    echo %ESPACIO%
)





:: =========================
:: Construcción de la red
:: =========================

:: Verificamos si la red de enrutamiento ya ha sido construida
if not exist "%DATA%\sevilla.osrm.hsgr" (
    echo(
    echo %ESPACIO%
    echo  === Contrayendo la red de enrutamiento del perfil "%MODO%" ===
    echo %ESPACIO%

    "%BASEDIR%\OSRM\osrm-contract.exe" "%DATA%\sevilla.osrm"
) else (
    echo(
    echo %ESPACIO%
    echo  === La red de enrutamiento del perfil "%MODO%" ya ha sido construida ===
    echo %ESPACIO%
)



:: =========================
:: Arranque del servidor
:: =========================

echo(
echo %ESPACIO%
echo  === Iniciando el servidor OSRM del perfil "%MODO%" en puerto %PUERTO% ===
echo %ESPACIO%
"%BASEDIR%\OSRM\osrm-routed.exe" "%DATA%\sevilla.osrm" --port %PUERTO%


:: Comprobamos si se ha iniciado el servidor OSRM correctamente
if %errorlevel% neq 0 (
    echo(
    echo %ESPACIO%
    ::echo Error en osrm-routed. Saliendo...
    echo  Cerrando servidor...
    echo %ESPACIO%
    exit /b %errorlevel%
)