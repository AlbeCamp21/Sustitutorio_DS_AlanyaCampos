#!/bin/bash

# Analiza que comando de python (python o python3 tiene el equipo)
echo "======CREANDO SETUP DE TRABAJO======"
if command -v python &>/dev/null; then
    PYTHON_CMD=python
elif command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
fi
# Crea el entorno virtual de nombre venv
echo "------Creando entorno virtual------"
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
else
    echo "Entorno virtual 'venv' ya existe"
fi
# Activa el entorno virtual
echo "------Activando entorno virtual------"
source venv/bin/activate
echo "Entorno activado"
# Instala requerimientos
echo "------Instalando requerimientos------"
pip install --upgrade pip
pip install -r requirements.txt
echo "Requisitos instalados exitosamente"