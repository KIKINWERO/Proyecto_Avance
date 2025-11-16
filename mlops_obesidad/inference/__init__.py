"""Módulo de inferencia para hacer predicciones con el modelo entrenado."""

from mlops_obesidad.inference.model_loader import load_model, get_model
from mlops_obesidad.inference.predictor import predict_single, request_to_dataframe

__all__ = ["load_model", "get_model", "predict_single", "request_to_dataframe"]

