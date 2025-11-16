# Guía de Integración del Modelo Real

Este documento describe los pasos necesarios para integrar el modelo entrenado en la API, reemplazando la función dummy actual.

## Prerequisitos

- Modelo entrenado guardado (formato `.pkl`, `.joblib`, o similar)
- Pipeline de preprocesamiento (si aplica)
- Archivos de configuración del modelo (scaler, encoders, etc.)

## Pasos de Integración

### 1. Preparar el Modelo para Producción

Asegúrate de que el modelo esté guardado en el directorio `models/` del proyecto:

```
models/
└── obesity_classifier_v1.pkl  # o el nombre que hayas usado
```

Si el modelo incluye un pipeline completo (preprocesador + clasificador), asegúrate de guardarlo como un único objeto.

### 2. Actualizar `API/services.py`

Reemplaza la función `real_predict()` con la lógica real de predicción:

```python
import joblib
from pathlib import Path
from mlops_obesidad.config import MODELS_DIR

# Cargar modelo al inicio (se puede hacer en startup)
MODEL_PATH = MODELS_DIR / "obesity_classifier_v1.pkl"
model = None

def load_model():
    """Carga el modelo desde disco."""
    global model
    if model is None:
        logger.info(f"Cargando modelo desde: {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
        logger.success("Modelo cargado exitosamente")
    return model

def real_predict(request: PredictionRequest) -> PredictionResponse:
    """
    Función para predicción real con el modelo entrenado.
    
    Args:
        request: Datos de entrada para la predicción
        
    Returns:
        Respuesta con la predicción y probabilidades
    """
    start_time = time.time()
    
    # Cargar modelo si no está cargado
    model = load_model()
    
    # Convertir request a formato que el modelo espera
    # Si el modelo incluye el preprocesador, solo necesitas pasar los datos raw
    input_data = _prepare_input_data(request)
    
    # Realizar predicción
    prediction = model.predict(input_data)[0]
    
    # Obtener probabilidades (si el modelo las soporta)
    if hasattr(model, 'predict_proba'):
        probabilities_array = model.predict_proba(input_data)[0]
        probabilities = _array_to_probabilities_dict(probabilities_array)
    else:
        # Si no hay probabilidades, crear diccionario con 1.0 para la clase predicha
        probabilities = {cls: 0.0 for cls in OBESITY_CLASSES}
        probabilities[prediction] = 1.0
    
    # Calcular confianza
    confidence = probabilities[prediction]
    
    # Calcular tiempo de procesamiento
    processing_time = (time.time() - start_time) * 1000
    
    # Crear respuesta
    response = PredictionResponse(
        prediction=prediction,
        probabilities=PredictionProbabilities(**probabilities),
        confidence=round(confidence, 2),
        model_version=MODEL_VERSION,
        model_id=MODEL_ID,
        prediction_id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat() + "Z",
        processing_time_ms=round(processing_time, 2),
    )
    
    logger.info(f"Predicción real completada: {prediction} (confianza: {confidence:.2f})")
    
    return response

def _prepare_input_data(request: PredictionRequest):
    """
    Prepara los datos del request para el formato que espera el modelo.
    
    Si el modelo incluye el preprocesador en el pipeline, solo necesitas
    convertir el request a un DataFrame o array numpy con las columnas correctas.
    """
    import pandas as pd
    
    # Crear DataFrame con los datos del request
    data = {
        "Gender": [request.Gender.value],
        "Age": [request.Age],
        "Height": [request.Height],
        "Weight": [request.Weight],
        "family_history_with_overweight": [request.family_history_with_overweight.value],
        "FAVC": [request.FAVC.value],
        "FCVC": [request.FCVC],
        "NCP": [request.NCP],
        "CAEC": [request.CAEC.value],
        "SMOKE": [request.SMOKE.value],
        "CH2O": [request.CH2O],
        "SCC": [request.SCC.value],
        "FAF": [request.FAF],
        "TUE": [request.TUE],
        "CALC": [request.CALC.value],
        "MTRANS": [request.MTRANS.value],
    }
    
    df = pd.DataFrame(data)
    return df

def _array_to_probabilities_dict(probabilities_array):
    """
    Convierte un array de probabilidades a diccionario.
    
    Asegúrate de que el orden de las clases en OBESITY_CLASSES
    coincida con el orden que usa el modelo (label_encoder.classes_).
    """
    return {
        OBESITY_CLASSES[i]: float(prob)
        for i, prob in enumerate(probabilities_array)
    }
```

### 3. Cargar el Modelo al Iniciar la API

Actualiza `API/main.py` para cargar el modelo en el evento de startup:

```python
@app.on_event("startup")
async def startup_event():
    """Evento ejecutado al iniciar la aplicación."""
    logger.info("Iniciando API de Predicción de Niveles de Obesidad")
    logger.info(f"Versión: {__version__}")
    
    # Cargar modelo
    try:
        from API.services import load_model
        load_model()
        logger.success("Modelo cargado exitosamente")
    except Exception as e:
        logger.error(f"Error al cargar el modelo: {str(e)}")
        logger.warning("La API continuará usando función dummy")
```

### 4. Verificar el Orden de las Clases

**IMPORTANTE:** Asegúrate de que el orden de las clases en `OBESITY_CLASSES` en `services.py` coincida con el orden que usa el modelo. Puedes verificar esto con:

```python
# Si usaste LabelEncoder
label_encoder.classes_
# Debe coincidir con OBESITY_CLASSES
```

Si el orden es diferente, actualiza `OBESITY_CLASSES` o ajusta la función `_array_to_probabilities_dict()`.

### 5. Manejar el Preprocesamiento

Si el modelo **NO** incluye el preprocesador en el pipeline, necesitarás aplicar las transformaciones manualmente:

```python
def _prepare_input_data(request: PredictionRequest):
    """Prepara y preprocesa los datos."""
    import pandas as pd
    from sklearn.preprocessing import RobustScaler, OneHotEncoder
    from sklearn.impute import SimpleImputer
    
    # Crear DataFrame
    df = pd.DataFrame([...])  # como en el ejemplo anterior
    
    # Aplicar las mismas transformaciones que usaste en entrenamiento
    # 1. One-hot encoding para categóricas
    # 2. RobustScaler para numéricas
    # 3. Imputación si es necesario
    
    # Retornar datos preprocesados
    return df_processed
```

**Recomendación:** Si es posible, guarda el modelo como un pipeline completo que incluya el preprocesador. Esto simplifica mucho la integración.

### 6. Probar la Integración

1. **Iniciar la API:**
   ```bash
   conda run -n mlops python run_api.py
   ```

2. **Probar con un request de ejemplo:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d @test_request.json
   ```

3. **Verificar en los logs** que el modelo se cargó correctamente y que las predicciones son reales (no dummy).

### 7. Actualizar la Función Dummy (Opcional)

Una vez que el modelo real esté funcionando, puedes:

- Eliminar la función `dummy_predict()` si ya no la necesitas
- O mantenerla como fallback en caso de error al cargar el modelo

## Checklist de Integración

- [ ] Modelo guardado en `models/`
- [ ] Función `real_predict()` implementada
- [ ] Función `_prepare_input_data()` implementada
- [ ] Función `_array_to_probabilities_dict()` implementada
- [ ] Modelo se carga en `startup_event()`
- [ ] Orden de clases verificado
- [ ] Preprocesamiento implementado (si necesario)
- [ ] Pruebas realizadas con requests reales
- [ ] Logs verificados
- [ ] Documentación actualizada

## Notas Importantes

1. **Formato del Modelo:** Asegúrate de saber si el modelo incluye el preprocesador o no. Esto afecta cómo preparas los datos.

2. **Orden de Clases:** El orden de las clases en las probabilidades debe coincidir con el orden del modelo.

3. **Manejo de Errores:** Implementa manejo de errores robusto para casos donde el modelo no pueda hacer predicciones.

4. **Performance:** Si el modelo es grande, considera cargarlo una sola vez al inicio en lugar de cargarlo en cada request.

5. **Versionado:** Actualiza `MODEL_VERSION` y `MODEL_ID` en `services.py` cuando cambies de modelo.

## Ejemplo de Request de Prueba

Crea un archivo `test_request.json`:

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

## Soporte

Si encuentras problemas durante la integración:

1. Verifica los logs de la API para mensajes de error
2. Asegúrate de que todas las dependencias estén instaladas
3. Verifica que el formato del modelo sea compatible (joblib, pickle, etc.)
4. Revisa que el preprocesamiento coincida con el entrenamiento

