#!/bin/bash

# ejecuta el script graph_analysis.py y el output se almacena en metrics.json
step_init(){
    python src/graph_analysis.py --output metrics.json;
}

# ejecuta el script report_suite.py y genera el reporte en el archivo report.md
step_report(){
    python src/report_suite.py --format md --output metrics.json --output report.md;
}

# muestra el archivo report.md
step_preview(){
    less report.md;
}

main(){
    step_init
    step_report
    step_preview
}

main