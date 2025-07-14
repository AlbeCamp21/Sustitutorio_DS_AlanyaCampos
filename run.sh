#!/bin/bash

# detectando el directorio donde está el script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# BASE_DIR="$DIR/.."

STEP=$1
case $STEP in
    requirements)
        echo "prueba exitosa"
        ;;
    saludo)
        echo "saludo"
        ;;
    lint)
        echo "======Ejecutando linters======"
        echo "------flake8------"
        flake8 --max-complexity 10 src scripts
        if [[ "$?" -ne 0 ]]; then
            echo "Linter flake8 falló"
            exit 1
        fi
        echo "------shellcheck------"
        SH_FILES=$(find . -type f -name "*.sh" -not -path "./venv/*")
        for sh in $SH_FILES; do
            shellcheck "$sh"
            if [[ $? -ne 0 ]]; then
                echo "Linter shellcheck falló en $sh"
                exit 1
            fi
        done
        ;;
    test)
        echo "======PYTEST======"
        pytest
        ;;
    help)
        echo "======AYUDA======"
        echo "Opciones válidas:"
        echo "    lint"
        echo "    test"
        echo "    help"
        echo "Ejemplo:"
        echo "    ./run.sh lint"
        ;;
    *)
        echo "Paso desconocido: $STEP"
        exit 0;
esac