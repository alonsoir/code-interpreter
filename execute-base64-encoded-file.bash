#!/bin/bash

# Activar entorno virtual
echo "Activando entorno virtual..."
# Copiar el archivo .env al directorio del script
cp .env $(dirname "$0")
pipenv shell
base64 -d encoded_script.py.b64 | python -
# Desactivar entorno virtual
echo "Desactivando entorno virtual..."
exit