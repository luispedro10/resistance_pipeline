#!/bin/bash
# Configuración inicial, por ejemplo, establecer variables de entorno específicas
export DISPLAY=host.docker.internal:0

# Asegúrate de activar el entorno correcto
source /miniconda/bin/activate tesisenv

# Comando para iniciar tu aplicación
python /app/gui.py
