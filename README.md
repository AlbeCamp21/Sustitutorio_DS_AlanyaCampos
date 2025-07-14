# EXAMEN SUSTITUTORIO V2

## Ejecución

```bash
$ source setup.sh
$ ./run.sh all
```

### Archivo `setup.sh`

| **Ejecutar primero**

Crea el siguiente entorno de trabajo:
1. Crea el entorno virtual `venv`.
2. Activa el entorno virtual.
3. Instala las herramientas dentro de `requirements.txt`.

### Archivo `run.sh`

Archivo ejecutador (en reemplazo de archivo `Makefile`) para la ejecución más rápida del proyecto, contiene las siguientes opciones:

- **lint**: Ejecuta los linters del proyecto, en este caso se usan solamente dos: `flake8` y `shellcheck`, cada uno de estos con sus propios archivos de configuración para omitir errores o advertencias muy críticas.
- **test**: Ejecuta `pytest` para cada archivo python que comience con: `test_*.py`. Se implementa también `coverage`, para que los tests abarquen como mínimo el 90% de los códigos python. Todo esto se indica en el archivo `pytest.ini`, donde se detalla que archivos testear, en base a qué, el porcentaje de cobertura, etc.
- **all**: Ejecuta todas las opciones de `run.sh` menos `help`.
- **help**: Muestra ayuda de cómo ejecutar el archivo `run.sh`.

**Ejemplo de ejecución:**

```bash
./run.sh <opción>
```

