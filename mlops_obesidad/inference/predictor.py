"""
Módulo para realizar predicciones con el modelo entrenado.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple

from loguru import logger

from API.schemas import PredictionRequest
from mlops_obesidad.inference.model_loader import get_model


def request_to_dataframe(request: PredictionRequest) -> pd.DataFrame:
    """
    Convierte un PredictionRequest a un DataFrame para el modelo.
    
    El modelo espera datos en formato crudo (raw) ya que incluye un pipeline
    completo de limpieza y preprocesamiento.
    
    Args:
        request: Request de predicción con los datos del individuo
        
    Returns:
        DataFrame con una sola fila y las columnas esperadas por el modelo
    """
    # Crear diccionario con los datos del request
    # Convertir enums a sus valores string
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
    logger.debug(f"DataFrame creado con shape: {df.shape}")
    
    return df


def predict_single(request: PredictionRequest) -> Tuple[str, np.ndarray, Dict[str, float]]:
    """
    Realiza una predicción individual con el modelo entrenado.
    
    Args:
        request: Request de predicción con los datos del individuo
        
    Returns:
        Tupla con:
        - prediction_label: Etiqueta predicha (string)
        - probabilities_array: Array de probabilidades (numpy array)
        - probabilities_dict: Diccionario con probabilidades por clase
        
    Raises:
        RuntimeError: Si el modelo no está cargado
        Exception: Si hay error durante la predicción
    """
    # Obtener modelo y label encoder
    artifacts = get_model()
    model = artifacts['model']
    label_encoder = artifacts['label_encoder']
    
    # Convertir request a DataFrame
    df_input = request_to_dataframe(request)
    
    logger.debug(f"Realizando predicción con modelo...")
    
    try:
        # El modelo tiene un pipeline completo que hace limpieza y preprocesamiento
        # Por lo tanto, podemos pasarle los datos crudos directamente
        pred_numeric = model.predict(df_input)
        pred_proba = model.predict_proba(df_input)
        
        # Decodificar etiqueta
        pred_label = label_encoder.inverse_transform(pred_numeric)[0]
        
        # Convertir probabilidades a diccionario
        # El orden de las clases debe coincidir con label_encoder.classes_
        class_names = label_encoder.classes_
        probabilities_dict = {
            class_name: float(prob)
            for class_name, prob in zip(class_names, pred_proba[0])
        }
        
        logger.debug(f"Predicción: {pred_label}, Confianza: {max(pred_proba[0]):.4f}")
        
        return pred_label, pred_proba[0], probabilities_dict
        
    except Exception as e:
        logger.error(f"Error durante la predicción: {e}")
        raise Exception(f"Error durante la predicción: {e}")

