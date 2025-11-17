"""
Transformadores personalizados para el pipeline de machine learning.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class DataCleanerTransformer(BaseEstimator, TransformerMixin):
    """
    Transformador personalizado que realiza la limpieza de datos crudos.
    
    Este transformador:
    - Estandariza valores nulos (NA, N/A, na, NaN, strings vacíos)
    - Recorta espacios en columnas de tipo object
    - Elimina columnas que están 100% nulas (aprendidas durante fit)
    
    No elimina filas duplicadas, ya que eso se hace antes del pipeline.
    """
    
    def __init__(self):
        """Inicializa el transformador."""
        self.obj_cols = []
        self.all_null_cols = []

    def fit(self, X, y=None):
        """
        Aprende qué columnas son 'object' y cuáles están 100% nulas.
        
        Args:
            X: DataFrame con datos de entrenamiento
            y: Variable objetivo (no usada, solo para compatibilidad con sklearn)
            
        Returns:
            self: El transformador ajustado
        """
        X = pd.DataFrame(X).copy()

        # Aprender qué columnas son de tipo 'object' para limpiarlas en transform
        self.obj_cols = X.select_dtypes(include=["object"]).columns.tolist()

        # Detectar columnas 100% nulas en el set de entrenamiento
        # (considerando también strings vacíos como nulos)
        df_temp = X.replace(r"^\s*$", np.nan, regex=True).replace(
            {"NA": np.nan, "N/A": np.nan, "na": np.nan, "NaN": np.nan}
        )
        self.all_null_cols = [c for c in df_temp.columns if df_temp[c].isna().all()]

        return self

    def transform(self, X):
        """
        Aplica la limpieza a cualquier dato (train o test/new).
        
        Args:
            X: DataFrame con datos a limpiar
            
        Returns:
            DataFrame limpio
        """
        df = pd.DataFrame(X).copy()

        # 1) Recortar strings SOLO en columnas de texto aprendidas en fit,
        #    sin convertir NaN a 'nan' (evitar astype(str))
        for c in self.obj_cols:
            if c in df.columns:
                df[c] = df[c].apply(lambda v: v.strip() if isinstance(v, str) else v)

        # 2) Estandarizar nulos:
        #    - strings vacíos -> NaN
        #    - alias de nulos (case-insensitive) -> NaN
        df = df.replace(r"^\s*$", np.nan, regex=True)
        null_aliases = {"na", "n/a", "nan"}
        for c in self.obj_cols:
            if c in df.columns:
                df[c] = df[c].apply(
                    lambda v: np.nan
                    if isinstance(v, str) and v.strip().lower() in null_aliases
                    else v
                )

        # 3) Eliminar columnas 100% nulas aprendidas en fit
        if self.all_null_cols:
            df = df.drop(columns=self.all_null_cols, errors="ignore")

        return df
