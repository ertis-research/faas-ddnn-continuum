Funciones de ejemplo para desplegar en Function Mesh

# Requisitos

Una instalación de Function Mesh funcionando, con Apache Pulsar Package
Management Service activado

## Echo Lambda

```sh
# Subir la lambda
$PULSAR_HOME/bin/pulsar-admin packages upload function://public/default/echo@0.1 --path "$PWD/echo.py" --description "echoes the input"
# Desplegar el artefacto
```
