"""
Script de deployment para hacer predicciones con el modelo entrenado.
El modelo espera datos en formato crudo (raw) ya que incluye un pipeline completo
de limpieza y preprocesamiento.
"""

import pickle
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Agregar el directorio raíz al path para poder importar mlops_obesidad
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Importar el transformador personalizado necesario para cargar el modelo pickle
from mlops_obesidad.preprocessing.transformers import DataCleanerTransformer

# =============================================================================
# CONFIGURACIÓN DE RUTAS
# =============================================================================

# SCRIPT_DIR y PROJECT_ROOT ya están definidos arriba

# Rutas de archivos (relativas al directorio del script)
SRC_PATH = PROJECT_ROOT / 'data' / 'raw' / 'obesity_estimation_original.csv'
MODEL_PATH = SCRIPT_DIR / 'xgboost_model_artifacts.pkl'

def main():
    """Función principal para cargar modelo y hacer predicciones."""
    
    # 1. Cargar el modelo y artefactos
    print("=" * 80)
    print("Cargando modelo y artefactos...")
    print("=" * 80)
    
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"El archivo del modelo no existe: {MODEL_PATH}")
    
    try:
        with open(MODEL_PATH, 'rb') as f:
            artifacts = pickle.load(f)
        print(f"[OK] Modelo cargado desde: {MODEL_PATH}")
    except Exception as e:
        raise Exception(f"Error al cargar el modelo: {e}")
    
    model = artifacts['model']
    label_encoder = artifacts['label_encoder']
    print(f"[OK] Label encoder cargado con {len(label_encoder.classes_)} clases")
    print(f"  Clases: {label_encoder.classes_}")
    
    # 2. Cargar datos de prueba
    print("\n" + "=" * 80)
    print("Cargando datos de prueba...")
    print("=" * 80)
    
    if not SRC_PATH.exists():
        raise FileNotFoundError(f"El archivo de datos no existe: {SRC_PATH}")
    
    try:
        df_raw = pd.read_csv(SRC_PATH, sep=None, engine="python", encoding="utf-8")
        print(f"[OK] Datos cargados: {df_raw.shape[0]} filas, {df_raw.shape[1]} columnas")
    except Exception as e:
        raise Exception(f"Error al cargar los datos: {e}")
    
    # 3. Preparar datos para predicción (eliminar columna objetivo si existe)
    print("\n" + "=" * 80)
    print("Preparando datos para predicción...")
    print("=" * 80)
    
    TARGET = 'NObeyesdad'
    if TARGET in df_raw.columns:
        df_for_prediction = df_raw.drop(columns=[TARGET])
        print(f"[OK] Columna objetivo '{TARGET}' eliminada")
        print(f"  Datos para predicción: {df_for_prediction.shape[0]} filas, {df_for_prediction.shape[1]} columnas")
    else:
        df_for_prediction = df_raw.copy()
        print(f"[OK] No se encontró columna objetivo, usando todos los datos")
        print(f"  Datos para predicción: {df_for_prediction.shape[0]} filas, {df_for_prediction.shape[1]} columnas")
    
    # 4. Realizar predicciones
    print("\n" + "=" * 80)
    print("Realizando predicciones...")
    print("=" * 80)
    
    try:
        # El modelo tiene un pipeline completo que hace limpieza y preprocesamiento
        # Por lo tanto, podemos pasarle los datos crudos directamente
        pred_numeric = model.predict(df_for_prediction)
        print(f"[OK] Predicciones numéricas generadas: {len(pred_numeric)} predicciones")
    except Exception as e:
        raise Exception(f"Error al hacer predicciones: {e}")
    
    try:
        pred_proba = model.predict_proba(df_for_prediction)
        print(f"[OK] Probabilidades generadas: shape {pred_proba.shape}")
    except Exception as e:
        print(f"[WARNING] No se pudieron generar probabilidades: {e}")
        pred_proba = None
    
    # 5. Decodificar etiquetas
    print("\n" + "=" * 80)
    print("Decodificando etiquetas...")
    print("=" * 80)
    
    try:
        pred_labels = label_encoder.inverse_transform(pred_numeric)
        print(f"[OK] Etiquetas decodificadas: {len(pred_labels)} etiquetas")
    except Exception as e:
        raise Exception(f"Error al decodificar etiquetas: {e}")
    
    # 6. Mostrar resultados
    print("\n" + "=" * 80)
    print("RESULTADOS")
    print("=" * 80)
    
    # Mostrar distribución de predicciones
    unique, counts = np.unique(pred_labels, return_counts=True)
    print("\nDistribución de predicciones:")
    for label, count in zip(unique, counts):
        percentage = (count / len(pred_labels)) * 100
        print(f"  {label}: {count} ({percentage:.2f}%)")
    
    # Mostrar primeras 10 predicciones
    print("\nPrimeras 10 predicciones:")
    for i in range(min(10, len(pred_labels))):
        if pred_proba is not None:
            max_prob = np.max(pred_proba[i])
            print(f"  Fila {i+1}: {pred_labels[i]} (confianza: {max_prob:.4f})")
        else:
            print(f"  Fila {i+1}: {pred_labels[i]}")
    
    print("\n" + "=" * 80)
    print("Proceso completado exitosamente")
    print("=" * 80)
    
    return pred_labels, pred_proba, pred_numeric


if __name__ == "__main__":
    try:
        pred_labels, pred_proba, pred_numeric = main()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
