"""
Módulo para cargar y gestionar el modelo entrenado.
"""

import pickle
import sys
from pathlib import Path
from typing import Dict, Optional, Any
from loguru import logger

from mlops_obesidad.config import MODELS_DIR

# Importar DataCleanerTransformer para que pickle pueda cargar el modelo
# Esta importación debe estar aquí antes de cargar el modelo
from mlops_obesidad.preprocessing.transformers import DataCleanerTransformer

# Registrar la clase en sys.modules para que pickle la encuentre
# Esto es necesario porque el modelo fue guardado desde un notebook donde
# la clase estaba en __main__
if '__main__' not in sys.modules:
    import types
    sys.modules['__main__'] = types.ModuleType('__main__')
sys.modules['__main__'].DataCleanerTransformer = DataCleanerTransformer

# Variable global para almacenar el modelo cargado
_model_artifacts: Optional[Dict[str, Any]] = None


def load_model(model_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Carga el modelo y sus artefactos desde un archivo pickle.
    
    Args:
        model_path: Ruta al archivo del modelo. Si es None, usa el path por defecto.
        
    Returns:
        Diccionario con 'model' y 'label_encoder'
        
    Raises:
        FileNotFoundError: Si el archivo del modelo no existe
        Exception: Si hay error al cargar el modelo
    """
    global _model_artifacts
    
    if _model_artifacts is not None:
        logger.info("Modelo ya está cargado en memoria")
        return _model_artifacts
    
    if model_path is None:
        model_path = MODELS_DIR / "xgboost_model_artifacts.pkl"
    
    if not model_path.exists():
        raise FileNotFoundError(f"El archivo del modelo no existe: {model_path}")
    
    logger.info(f"Cargando modelo desde: {model_path}")
    
    try:
        with open(model_path, 'rb') as f:
            _model_artifacts = pickle.load(f)
        
        logger.success("Modelo cargado exitosamente")
        logger.info(f"Label encoder con {len(_model_artifacts['label_encoder'].classes_)} clases")
        logger.debug(f"Clases: {_model_artifacts['label_encoder'].classes_}")
        
        return _model_artifacts
        
    except Exception as e:
        logger.error(f"Error al cargar el modelo: {e}")
        raise Exception(f"Error al cargar el modelo: {e}")


def get_model() -> Dict[str, Any]:
    """
    Obtiene el modelo cargado. Si no está cargado, lo carga primero.
    
    Returns:
        Diccionario con 'model' y 'label_encoder'
        
    Raises:
        RuntimeError: Si el modelo no está cargado y no se puede cargar
    """
    global _model_artifacts
    
    if _model_artifacts is None:
        logger.warning("Modelo no está cargado, cargando ahora...")
        load_model()
    
    if _model_artifacts is None:
        raise RuntimeError("No se pudo cargar el modelo")
    
    return _model_artifacts

