#!/bin/bash

# Verificar si pipenv está instalado
if ! command -v pipenv &> /dev/null; then
    echo "pipenv no está instalado. Instalando pipenv..."
    pip install pipenv
fi

# Crear entorno virtual con pipenv e instalar dependencias
echo "Creando entorno virtual y instalando dependencias..."
pipenv install

# Copiar el archivo .env al directorio del script
cp .env $(dirname "$0")

# Codificar el archivo main-generated-python-code.py a base64
base64 -w 0 main-python-generator-code.py > encoded_script.py.b64

# Activar entorno virtual
echo "Activando entorno virtual..."
pipenv shell

# Decodificar y ejecutar el script base64
echo "Decodificando y ejecutando el script base64..."
base64 -d encoded_script.py.b64 > decoded_script.py
python decoded_script.py

# Desactivar entorno virtual
echo "Desactivando entorno virtual..."
exit
