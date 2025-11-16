# Guía de Integración del Modelo Real

Este documento describe la integración del modelo entrenado en la API. **La integración ya está completada** y este documento sirve como referencia para entender cómo funciona.

## Estado de la Integración

✅ **COMPLETADO** - El modelo está integrado y funcionando en la API.

## Arquitectura de la Integración

La integración sigue las mejores prácticas de MLOps con una estructura modular:

```
mlops_obesidad/
├── preprocessing/
│   ├── __init__.py
│   └── transformers.py          # DataCleanerTransformer
├── inference/
│   ├── __init__.py
│   ├── model_loader.py          # Carga y gestión del modelo
│   └── predictor.py             # Funciones de predicción
├── utils/
│   └── plots.py                 # Utilidades de visualización
└── config.py                    # Configuración de rutas
```

## Componentes Principales

### 1. Módulo de Preprocesamiento (`mlops_obesidad/preprocessing/`)

Contiene el transformador personalizado `DataCleanerTransformer` que es parte del pipeline del modelo. Este transformador:

- Estandariza valores nulos (NA, N/A, na, NaN, strings vacíos)
- Recorta espacios en columnas de tipo object
- Elimina columnas que están 100% nulas

**Importante:** Este transformador debe estar disponible para que pickle pueda cargar el modelo.

### 2. Módulo de Inferencia (`mlops_obesidad/inference/`)

#### `model_loader.py`

Gestiona la carga del modelo en memoria:

- `load_model(model_path=None)`: Carga el modelo desde un archivo pickle
- `get_model()`: Obtiene el modelo cargado (lo carga si no está cargado)

El modelo se carga una sola vez y se mantiene en memoria para mejor rendimiento.

#### `predictor.py`

Contiene las funciones para hacer predicciones:

- `request_to_dataframe(request)`: Convierte un `PredictionRequest` a un DataFrame
- `predict_single(request)`: Realiza una predicción individual

### 3. Integración con la API (`API/services.py`)

La función `real_predict()` ahora:

1. Usa el módulo de inferencia para hacer predicciones reales
2. Maneja errores con fallback a función dummy si es necesario
3. Convierte las probabilidades al formato esperado por la API

### 4. Carga del Modelo en Startup (`API/main.py`)

El modelo se carga automáticamente cuando la API inicia:

```python
@app.on_event("startup")
async def startup_event():
    from mlops_obesidad.inference import load_model
    load_model()
```

## Flujo de Predicción

1. **Cliente envía request** → `POST /api/v1/predict` con JSON
2. **API valida request** → Pydantic valida el schema
3. **Router llama a `real_predict()`** → `API/services.py`
4. **`real_predict()` usa `predict_single()`** → `mlops_obesidad/inference/predictor.py`
5. **`predict_single()` convierte request a DataFrame** → `request_to_dataframe()`
6. **Modelo hace predicción** → El pipeline completo procesa los datos
7. **Resultado se formatea** → Se crea `PredictionResponse`
8. **API retorna respuesta** → JSON con predicción y probabilidades

## Formato del Modelo

El modelo está guardado en:
```
models/xgboost_model_artifacts.pkl
```

Contiene un diccionario con:
- `'model'`: Pipeline completo (DataCleanerTransformer + Preprocessor + XGBClassifier)
- `'label_encoder'`: LabelEncoder para decodificar las clases

**Características importantes:**
- El modelo incluye el pipeline completo de preprocesamiento
- Los datos de entrada deben estar en formato crudo (raw)
- No se necesita preprocesamiento manual antes de la predicción

## Orden de Clases

El orden de las clases en `OBESITY_CLASSES` debe coincidir con el orden del `label_encoder` del modelo:

```python
OBESITY_CLASSES = [
    "Insufficient_Weight",
    "Normal_Weight",
    "Obesity_Type_I",
    "Obesity_Type_II",
    "Obesity_Type_III",
    "Overweight_Level_I",
    "Overweight_Level_II",
]
```

Este orden coincide con: `label_encoder.classes_`

## Conversión de Request a DataFrame

La función `request_to_dataframe()` convierte un `PredictionRequest` (Pydantic) a un DataFrame de pandas:

```python
def request_to_dataframe(request: PredictionRequest) -> pd.DataFrame:
    data = {
        "Gender": [request.Gender.value],
        "Age": [request.Age],
        "Height": [request.Height],
        # ... todos los campos
    }
    return pd.DataFrame(data)
```

Los enums de Pydantic se convierten a sus valores string usando `.value`.

## Manejo de Errores

La integración incluye manejo robusto de errores:

1. **Modelo no cargado**: Si el modelo no se puede cargar, se usa función dummy como fallback
2. **Error durante predicción**: Si hay error en la predicción, se usa función dummy como fallback
3. **Logs informativos**: Todos los errores se registran en los logs

## Pruebas

### 1. Verificar que el modelo se carga

Al iniciar la API, deberías ver en los logs:
```
[INFO] Cargando modelo desde: models/xgboost_model_artifacts.pkl
[SUCCESS] Modelo cargado exitosamente
```

### 2. Probar con un request

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

### 3. Verificar respuesta

La respuesta debe incluir:
- `prediction`: Clase predicha (ej: "Normal_Weight")
- `probabilities`: Diccionario con probabilidades para cada clase
- `confidence`: Probabilidad de la clase predicha
- `model_version`: "1.0.0"
- `model_id`: "obesity-classifier-v1"

## Dependencias

Asegúrate de tener instaladas todas las dependencias:

```bash
pip install -r requirements.txt
```

**Importante:** El modelo fue entrenado con `scikit-learn==1.6.1`. Asegúrate de tener esta versión instalada para compatibilidad.

## Estructura de Archivos

```
Proyecto_Avance/
├── mlops_obesidad/
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   └── transformers.py
│   ├── inference/
│   │   ├── __init__.py
│   │   ├── model_loader.py
│   │   └── predictor.py
│   ├── utils/
│   │   └── plots.py
│   └── config.py
├── API/
│   ├── services.py          # real_predict() implementada
│   ├── main.py              # Carga modelo en startup
│   └── routers.py
├── models/
│   └── xgboost_model_artifacts.pkl
└── requirements.txt
```

## Checklist de Integración

- [x] Modelo guardado en `models/`
- [x] Estructura modular creada (`preprocessing/`, `inference/`, `utils/`)
- [x] Función `real_predict()` implementada
- [x] Función `request_to_dataframe()` implementada
- [x] Función `predict_single()` implementada
- [x] Modelo se carga en `startup_event()`
- [x] Orden de clases verificado y actualizado
- [x] Preprocesamiento manejado por el pipeline del modelo
- [x] Manejo de errores implementado
- [x] Logs informativos agregados
- [x] Documentación actualizada

## Notas Importantes

1. **Formato del Modelo:** El modelo incluye un pipeline completo, por lo que solo necesitas pasar datos crudos.

2. **Orden de Clases:** El orden de `OBESITY_CLASSES` coincide con `label_encoder.classes_`.

3. **Manejo de Errores:** Si el modelo no está disponible, la API usa función dummy como fallback.

4. **Performance:** El modelo se carga una sola vez al inicio y se mantiene en memoria.

5. **Versionado:** Actualiza `MODEL_VERSION` y `MODEL_ID` en `services.py` cuando cambies de modelo.

6. **Compatibilidad de Versiones:** El modelo requiere `scikit-learn==1.6.1` para cargar correctamente.

## Troubleshooting

### Error: "Can't get attribute 'DataCleanerTransformer'"

**Solución:** Asegúrate de que `mlops_obesidad.preprocessing.transformers` esté importado antes de cargar el modelo.

### Error: "Modelo no disponible"

**Solución:** Verifica que el archivo `models/xgboost_model_artifacts.pkl` exista y sea accesible.

### Error: "InconsistentVersionWarning" de scikit-learn

**Solución:** Instala la versión correcta: `pip install scikit-learn==1.6.1`

### Las probabilidades no coinciden con las clases

**Solución:** Verifica que el orden de `OBESITY_CLASSES` coincida con `label_encoder.classes_`.

## Soporte

Si encuentras problemas:

1. Verifica los logs de la API para mensajes de error
2. Asegúrate de que todas las dependencias estén instaladas
3. Verifica que el formato del modelo sea compatible
4. Revisa que el orden de clases sea correcto
