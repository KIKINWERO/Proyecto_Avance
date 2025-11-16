# API de Predicción de Niveles de Obesidad

**Autor:** Euipo 7 MLOPs MNA
**Fecha:** 15 de noviembre de 2025
**Versión:** 1.0.0

## Descripción General

Esta API REST proporciona un servicio de predicción de niveles de obesidad basado en hábitos alimenticios y condición física de individuos. La API está diseñada siguiendo las mejores prácticas de MLOps para servir modelos de machine learning en producción.

El modelo utilizado es un clasificador que predice 7 categorías diferentes de niveles de obesidad con una precisión del **97%** según las métricas de evaluación del modelo entrenado.

## Propuesta de Arquitectura Completa

La siguiente es la propuesta completa de arquitectura de la API siguiendo las mejores prácticas de MLOps. **Nota importante:** Para este ejercicio académico, solo se implementará el endpoint `/predict`. Los demás endpoints se documentan aquí como parte de la arquitectura ideal para producción.

### Endpoints Propuestos

```
POST   /api/v1/predict          # Predicción individual (IMPLEMENTADO)
POST   /api/v1/predict/batch    # Predicción en lote (Futuro)
GET    /health                  # Health check básico (Futuro)
GET    /health/ready            # Readiness probe - modelo cargado (Futuro)
GET    /health/live              # Liveness probe - API funcionando (Futuro)
GET    /api/v1/models            # Listar modelos disponibles (Futuro)
GET    /api/v1/models/{version}  # Información de modelo específico (Futuro)
GET    /docs                     # Documentación Swagger/OpenAPI (Automático FastAPI)
GET    /redoc                    # Documentación ReDoc (Automático FastAPI)
```

### Implementación Actual

**Para este ejercicio, solo se implementará:**
- `POST /api/v1/predict` - Endpoint de predicción individual

## Endpoint de Predicción: `/api/v1/predict`

### Descripción

Este endpoint recibe las características de un individuo y retorna la predicción del nivel de obesidad junto con las probabilidades asociadas a cada clase.

### Método HTTP

`POST`

### URL

```
/api/v1/predict
```

### Input (Request Body)

El endpoint recibe un objeto JSON con las siguientes características basadas en el dataset original (`data/raw/obesity_estimation_original.csv`):

#### Estructura del Request (ejemplo)

```json
{
  "Gender": "Female",
  "Age": 21.0,
  "Height": 1.62,
  "Weight": 64.0,
  "family_history_with_overweight": "yes",
  "FAVC": "no",
  "FCVC": 2.0,
  "NCP": 3.0,
  "CAEC": "Sometimes",
  "SMOKE": "no",
  "CH2O": 2.0,
  "SCC": "no",
  "FAF": 0.0,
  "TUE": 1.0,
  "CALC": "no",
  "MTRANS": "Public_Transportation"
}
```

#### Descripción de Campos

| Campo | Tipo | Descripción | Valores Permitidos |
|-------|------|-------------|-------------------|
| `Gender` | string | Género del individuo | `"Female"`, `"Male"` |
| `Age` | float | Edad en años | Número entre 0 y 120 |
| `Height` | float | Altura en metros | Número positivo (ej: 1.62) |
| `Weight` | float | Peso en kilogramos | Número positivo (ej: 64.0) |
| `family_history_with_overweight` | string | Historial familiar de sobrepeso | `"yes"`, `"no"` |
| `FAVC` | string | Frecuencia de consumo de alimentos altos en calorías | `"yes"`, `"no"` |
| `FCVC` | float | Frecuencia de consumo de vegetales | Número entre 1.0 y 3.0 |
| `NCP` | float | Número de comidas principales al día | Número entre 1.0 y 4.0 (ej: 1.0, 2.0, 3.0) |
| `CAEC` | string | Consumo de alimentos entre comidas | `"no"`, `"Sometimes"`, `"Frequently"`, `"Always"` |
| `SMOKE` | string | ¿Fuma? | `"yes"`, `"no"` |
| `CH2O` | float | Consumo diario de agua | Número entre 1.0 y 3.0 |
| `SCC` | string | Monitoreo de calorías consumidas | `"yes"`, `"no"` |
| `FAF` | float | Actividad física | Número entre 0.0 y 3.0 |
| `TUE` | float | Tiempo usando dispositivos electrónicos | Número entre 0.0 y 2.0 |
| `CALC` | string | Consumo de alcohol | `"no"`, `"Sometimes"`, `"Frequently"`, `"Always"` |
| `MTRANS` | string | Medio de transporte utilizado | `"Public_Transportation"`, `"Walking"`, `"Automobile"`, `"Motorbike"`, `"Bike"` |

### Output (Response)

#### Respuesta Exitosa (200 OK)

```json
{
  "prediction": "Normal_Weight",
  "probabilities": {
    "Insufficient_Weight": 0.05,
    "Normal_Weight": 0.75,
    "Overweight_Level_I": 0.12,
    "Overweight_Level_II": 0.05,
    "Obesity_Type_I": 0.02,
    "Obesity_Type_II": 0.01,
    "Obesity_Type_III": 0.00
  },
  "confidence": 0.75,
  "model_version": "1.0.0",
  "model_id": "obesity-classifier-v1",
  "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T10:30:00Z",
  "processing_time_ms": 45.2
}
```

#### Descripción de Campos de Respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `prediction` | string | Clase predicha (la más probable) |
| `probabilities` | object | Probabilidades para cada clase (suman 1.0) |
| `confidence` | float | Confianza de la predicción (probabilidad de la clase predicha) |
| `model_version` | string | Versión del modelo utilizado |
| `model_id` | string | Identificador del modelo |
| `prediction_id` | string | UUID único para esta predicción (para tracking) |
| `timestamp` | string | Timestamp ISO 8601 de cuando se hizo la predicción |
| `processing_time_ms` | float | Tiempo de procesamiento en milisegundos |

#### Clases de Predicción

El modelo puede predecir las siguientes 7 categorías de niveles de obesidad:

1. **`Insufficient_Weight`** - Peso Insuficiente
2. **`Normal_Weight`** - Peso Normal
3. **`Overweight_Level_I`** - Sobrepeso Nivel I
4. **`Overweight_Level_II`** - Sobrepeso Nivel II
5. **`Obesity_Type_I`** - Obesidad Tipo I
6. **`Obesity_Type_II`** - Obesidad Tipo II
7. **`Obesity_Type_III`** - Obesidad Tipo III

**Nota:** Según el reporte de clasificación del modelo, el accuracy general es del **97%**, con métricas individuales por clase que van desde 0.93 a 1.00 en precisión y recall.

### Respuestas de Error

#### 400 Bad Request - Validación Fallida

```json
{
  "error": "ValidationError",
  "message": "Invalid input data",
  "details": {
    "field": "Age",
    "issue": "Value must be between 0 and 120"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 422 Unprocessable Entity - Datos Inválidos

```json
{
  "error": "ValidationError",
  "message": "Invalid categorical value",
  "details": {
    "field": "Gender",
    "issue": "Value must be one of: 'Female', 'Male'"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 503 Service Unavailable - Modelo No Disponible

```json
{
  "error": "ModelNotReady",
  "message": "Model is not loaded or ready for predictions",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 500 Internal Server Error

```json
{
  "error": "InternalServerError",
  "message": "An unexpected error occurred during prediction",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Ejemplo de Uso

### Request con cURL

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": "Female",
    "Age": 21.0,
    "Height": 1.62,
    "Weight": 64.0,
    "family_history_with_overweight": "yes",
    "FAVC": "no",
    "FCVC": 2.0,
    "NCP": 3.0,
    "CAEC": "Sometimes",
    "SMOKE": "no",
    "CH2O": 2.0,
    "SCC": "no",
    "FAF": 0.0,
    "TUE": 1.0,
    "CALC": "no",
    "MTRANS": "Public_Transportation"
  }'
```

### Request con Python

```python
import requests

url = "http://localhost:8000/api/v1/predict"
data = {
    "Gender": "Female",
    "Age": 21.0,
    "Height": 1.62,
    "Weight": 64.0,
    "family_history_with_overweight": "yes",
    "FAVC": "no",
    "FCVC": 2.0,
    "NCP": 3.0,
    "CAEC": "Sometimes",
    "SMOKE": "no",
    "CH2O": 2.0,
    "SCC": "no",
    "FAF": 0.0,
    "TUE": 1.0,
    "CALC": "no",
    "MTRANS": "Public_Transportation"
}

response = requests.post(url, json=data)
result = response.json()
print(f"Predicción: {result['prediction']}")
print(f"Confianza: {result['confidence']}")
```

## Características Técnicas

### Framework

- **FastAPI**: Framework web moderno y rápido para construir APIs con Python
- **Pydantic**: Validación automática de datos de entrada y salida
- **Uvicorn**: Servidor ASGI de alto rendimiento

### Validación

- Validación automática de tipos de datos
- Validación de rangos para valores numéricos
- Validación de valores permitidos para campos categóricos
- Mensajes de error descriptivos

### Documentación Automática

FastAPI genera automáticamente:
- **Swagger UI**: Disponible en `/docs`
- **ReDoc**: Disponible en `/redoc`
- **OpenAPI Schema**: Disponible en `/openapi.json`

### Preprocesamiento

El modelo espera datos en el mismo formato que el dataset original. El preprocesamiento (one-hot encoding, normalización, etc.) se realiza internamente antes de la predicción.

## Arquitectura Futura (No Implementada)

### Health Checks

Los endpoints de health checks permitirían:
- Verificar que la API está funcionando (`/health`)
- Verificar que el modelo está cargado y listo (`/health/ready`)
- Verificar que la API está viva (`/health/live`)

### Batch Predictions

El endpoint `/api/v1/predict/batch` permitiría procesar múltiples predicciones en una sola solicitud, optimizando el throughput.

### Model Management

Los endpoints de gestión de modelos permitirían:
- Listar modelos disponibles
- Obtener información de versiones específicas
- Cambiar entre versiones de modelos

### Monitoreo y Observabilidad

- Logging estructurado de todas las predicciones
- Métricas de latencia y throughput
- Tracking de errores y excepciones
- Integración con sistemas de monitoreo (Prometheus, Grafana)

### Seguridad

- Autenticación mediante API keys
- Rate limiting para prevenir abuso
- Validación exhaustiva de inputs
- HTTPS en producción

## Referencias

- **Dataset Original**: `data/raw/obesity_estimation_original.csv`
- **UCI Repository**: [Estimation of Obesity Levels Based On Eating Habits and Physical Condition](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition)
- **Modelo**: Clasificador con 97% de accuracy según reporte de clasificación

## Notas de Implementación

- Esta API está diseñada para servir el modelo de predicción de obesidad desarrollado en el proyecto MLOps
- El modelo fue entrenado con datos de individuos de México, Perú y Colombia
- La precisión del modelo es del 97% según las métricas de evaluación
- Para este ejercicio académico, solo se implementa el endpoint `/predict`
- La arquitectura completa documentada aquí representa las mejores prácticas de MLOps para producción

