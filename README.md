## Descripción del proyecto

Este proyecto automatiza la auditoría de registros de mascotas mediante la implementación de reglas de validación divididas en dos grandes bloques: **Estructurales** y **Semánticas**. Los registros que cumplen con todos los criterios se consolidan como listos para producción, mientras que las anomalías son aisladas para su posterior revisión en auditorías de calidad.

## Reglas de Validación Implementadas

### 1. Validaciones Estructurales
Garantizan que la anatomía de los datos cumpla con los tipos y rangos técnicos esperados utilizando la librería de validación de esquemas **Pandera**.
* **`id_mascota`**: Debe ser un valor de tipo entero (`int`) y no se permiten valores nulos.
* **`especie`**: Se valida que pertenezca estrictamente a la lista de especies admitidas: `['perro', 'gato', 'conejo', 'pez', 'loro']`.
* **`peso_kg`**: Se restringe a un rango físico realista entre **0.05 kg** y **120 kg**.
* **`fecha_consulta`**: Corresponde a un formato de fecha y hora válido (`datetime`), aplicando coacción de tipos automática.

### 2. Validaciones Semánticas (Lógica de Negocio)
Aseguran la coherencia e integridad de la información cruzando variables o analizando el contexto de los datos utilizando máscaras nativas de `pandas`.
* **Condición de Obesidad**: Si el campo `rango_peso` es igual a `'obeso'`, se valida que:
    * Si es un `perro`, el `peso_kg` debe ser mayor a **30**.
    * Si es un `gato`, el `peso_kg` debe ser mayor a **6**.
* **Consistencia de Contacto**: Si un mismo dueño aparece con 2 o más consultas (`2+`), se verifica que el correo electrónico (`email`) registrado sea idéntico y consistente en todos sus registros.
* **Regla Libre (Propia)**: 
    * *Regla:* **Validación de Coherencia de Especie y Rango de Peso Máximo**.
    * *Justificación:* Si la especie es `'pez'` o `'conejo'`, el `rango_peso` no puede ser nunca `'obeso'` ni superar los 15 kg, ya que biológicamente representaría un error de carga de datos en estas especies específicas en el contexto de nuestra clínica.



## Flujo de Separación + Logs

El script procesa el archivo de entrada y realiza un seguimiento detallado del ciclo de vida de los datos:

1. **Segmentación de Archivos**:
    * `mascotas_validas.csv`: Contiene únicamente los registros que aprobaron el 100% de las validaciones estructurales y semánticas.
    * `mascotas_invalidas.csv`: Contiene las filas que fallaron en una o más reglas, ideal para auditorías de calidad.
2. **Sistema de Logs**: El script genera un archivo persistente en `logs/validacion.log` y a su vez imprime en consola el estado detallado y el conteo exacto de registros con inconsistencias detectadas.
3. **Métrica Final**: Al finalizar la ejecución, se muestra en pantalla el porcentaje exacto (`%`) de registros válidos sobre el total analizado:
    ```text
    [INFO] Validación finalizada con éxito.
    [RESULTADO] Registros válidos: X% del total de datos analizados.
    ```

INTEGRANTES:

NIKOLAS SOTOMAIOR.

FERNANDO VILLALOBOS.

FELIPE ARRIAGADDA.

JOAN ROJAS

##  Estructura del Proyecto

El repositorio sigue las mejores prácticas de desarrollo, modularización y separación de entornos:

```text
├── data/

│   ├── raw/                  # Archivos originales de entrada

│   └── processed/            # Resultados del pipeline (validas / invalidas)

├── logs/                     # Archivos .log de auditoría

├── pipeline_validacion.py    # Script principal automatizado

└── README.md                 # Documentación del proyecto

