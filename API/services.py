"""Servicios de predicción del modelo."""

import time
import random
from typing import Dict
from uuid import uuid4
from datetime import datetime

from loguru import logger

from API.schemas import PredictionRequest, PredictionResponse, PredictionProbabilities


# Clases de predicción posibles
# IMPORTANTE: El orden debe coincidir con el orden del label_encoder del modelo
# Orden del modelo: ['Insufficient_Weight', 'Normal_Weight', 'Obesity_Type_I', 
#                    'Obesity_Type_II', 'Obesity_Type_III', 'Overweight_Level_I', 
#                    'Overweight_Level_II']
OBESITY_CLASSES = [
    "Insufficient_Weight",
    "Normal_Weight",
    "Obesity_Type_I",
    "Obesity_Type_II",
    "Obesity_Type_III",
    "Overweight_Level_I",
    "Overweight_Level_II",
]

MODEL_VERSION = "1.0.0"
MODEL_ID = "obesity-classifier-v1"


def dummy_predict(request: PredictionRequest) -> PredictionResponse:
    """
    Función dummy que simula una predicción del modelo.
    
    Esta función genera predicciones aleatorias pero realistas mientras
    el modelo real está en desarrollo. Será reemplazada cuando el modelo
    esté listo.
    
    Args:
        request: Datos de entrada para la predicción
        
    Returns:
        Respuesta con la predicción y probabilidades
    """
    start_time = time.time()
    
    logger.info(f"Procesando predicción para: Age={request.Age}, Weight={request.Weight}")
    
    # Generar probabilidades dummy basadas en algunas características
    # Esto es solo para simulación - el modelo real usará todas las features
    probabilities = _generate_dummy_probabilities(request)
    
    # Obtener la clase con mayor probabilidad
    prediction = max(probabilities.items(), key=lambda x: x[1])[0]
    confidence = probabilities[prediction]
    
    # Calcular tiempo de procesamiento
    processing_time = (time.time() - start_time) * 1000  # en milisegundos
    
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
    
    logger.info(
        f"Predicción completada: {prediction} (confianza: {confidence:.2f})"
    )
    
    return response


def _generate_dummy_probabilities(request: PredictionRequest) -> Dict[str, float]:
    """
    Genera probabilidades dummy basadas en características básicas.
    
    Esta función simula un modelo que considera BMI y algunas características
    para generar probabilidades realistas.
    """
    # Calcular BMI aproximado
    bmi = request.Weight / (request.Height ** 2)
    
    # Inicializar probabilidades base
    probs = {cls: 0.0 for cls in OBESITY_CLASSES}
    
    # Asignar probabilidades basadas en BMI (simplificado)
    if bmi < 18.5:
        probs["Insufficient_Weight"] = 0.7
        probs["Normal_Weight"] = 0.2
        probs["Overweight_Level_I"] = 0.05
        probs["Overweight_Level_II"] = 0.03
        probs["Obesity_Type_I"] = 0.01
        probs["Obesity_Type_II"] = 0.01
        probs["Obesity_Type_III"] = 0.00
    elif bmi < 25:
        probs["Insufficient_Weight"] = 0.05
        probs["Normal_Weight"] = 0.75
        probs["Overweight_Level_I"] = 0.12
        probs["Overweight_Level_II"] = 0.05
        probs["Obesity_Type_I"] = 0.02
        probs["Obesity_Type_II"] = 0.01
        probs["Obesity_Type_III"] = 0.00
    elif bmi < 30:
        probs["Insufficient_Weight"] = 0.02
        probs["Normal_Weight"] = 0.15
        probs["Overweight_Level_I"] = 0.50
        probs["Overweight_Level_II"] = 0.25
        probs["Obesity_Type_I"] = 0.05
        probs["Obesity_Type_II"] = 0.02
        probs["Obesity_Type_III"] = 0.01
    elif bmi < 35:
        probs["Insufficient_Weight"] = 0.00
        probs["Normal_Weight"] = 0.05
        probs["Overweight_Level_I"] = 0.15
        probs["Overweight_Level_II"] = 0.20
        probs["Obesity_Type_I"] = 0.45
        probs["Obesity_Type_II"] = 0.10
        probs["Obesity_Type_III"] = 0.05
    elif bmi < 40:
        probs["Insufficient_Weight"] = 0.00
        probs["Normal_Weight"] = 0.02
        probs["Overweight_Level_I"] = 0.05
        probs["Overweight_Level_II"] = 0.10
        probs["Obesity_Type_I"] = 0.20
        probs["Obesity_Type_II"] = 0.45
        probs["Obesity_Type_III"] = 0.18
    else:
        probs["Insufficient_Weight"] = 0.00
        probs["Normal_Weight"] = 0.00
        probs["Overweight_Level_I"] = 0.02
        probs["Overweight_Level_II"] = 0.05
        probs["Obesity_Type_I"] = 0.10
        probs["Obesity_Type_II"] = 0.20
        probs["Obesity_Type_III"] = 0.63
    
    # Añadir algo de variabilidad aleatoria para simular incertidumbre del modelo
    for cls in probs:
        noise = random.uniform(-0.05, 0.05)
        probs[cls] = max(0.0, min(1.0, probs[cls] + noise))
    
    # Normalizar para que sumen 1.0
    total = sum(probs.values())
    if total > 0:
        probs = {k: v / total for k, v in probs.items()}
    
    return probs


def real_predict(request: PredictionRequest) -> PredictionResponse:
    """
    Función para predicción real con el modelo entrenado.
    
    Args:
        request: Datos de entrada para la predicción
        
    Returns:
        Respuesta con la predicción y probabilidades
        
    Raises:
        RuntimeError: Si el modelo no está cargado
        Exception: Si hay error durante la predicción
    """
    start_time = time.time()
    
    logger.info(f"Procesando predicción real para: Age={request.Age}, Weight={request.Weight}")
    
    try:
        # Importar funciones de inferencia
        from mlops_obesidad.inference import predict_single
        
        # Realizar predicción
        prediction_label, probabilities_array, probabilities_dict = predict_single(request)
        
        # Obtener confianza (probabilidad máxima)
        confidence = max(probabilities_dict.values())
        
        # Asegurar que todas las clases estén en el diccionario
        # (por si el modelo tiene un orden diferente)
        complete_probabilities = {cls: 0.0 for cls in OBESITY_CLASSES}
        complete_probabilities.update(probabilities_dict)
        
        # Calcular tiempo de procesamiento
        processing_time = (time.time() - start_time) * 1000  # en milisegundos
        
        # Crear respuesta
        response = PredictionResponse(
            prediction=prediction_label,
            probabilities=PredictionProbabilities(**complete_probabilities),
            confidence=round(confidence, 4),
            model_version=MODEL_VERSION,
            model_id=MODEL_ID,
            prediction_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat() + "Z",
            processing_time_ms=round(processing_time, 2),
        )
        
        logger.success(
            f"Predicción real completada: {prediction_label} (confianza: {confidence:.4f})"
        )
        
        return response
        
    except RuntimeError as e:
        logger.error(f"Error: Modelo no disponible - {e}")
        logger.warning("Usando función dummy como fallback")
        return dummy_predict(request)
    except Exception as e:
        logger.error(f"Error durante predicción real: {e}")
        logger.warning("Usando función dummy como fallback")
        return dummy_predict(request)

