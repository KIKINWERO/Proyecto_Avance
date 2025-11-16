"""
Tests unitarios para el módulo de preprocesamiento.
"""

import pytest
import pandas as pd
import numpy as np

from mlops_obesidad.preprocessing.transformers import DataCleanerTransformer


class TestDataCleanerTransformer:
    """Tests para DataCleanerTransformer."""
    
    def test_fit_learns_object_columns(self):
        """Test que fit aprende qué columnas son de tipo object."""
        transformer = DataCleanerTransformer()
        df = pd.DataFrame({
            'numeric_col': [1, 2, 3],
            'text_col': ['a', 'b', 'c'],
            'another_text': ['x', 'y', 'z']
        })
        
        transformer.fit(df)
        
        assert 'text_col' in transformer.obj_cols
        assert 'another_text' in transformer.obj_cols
        assert 'numeric_col' not in transformer.obj_cols
    
    def test_transform_standardizes_nulls(self):
        """Test que transform estandariza valores nulos."""
        transformer = DataCleanerTransformer()
        df_train = pd.DataFrame({
            'col1': ['NA', 'N/A', 'na', 'value', np.nan]
        })
        
        transformer.fit(df_train)
        df_test = pd.DataFrame({
            'col1': ['NA', 'N/A', 'na', 'NaN', 'value']
        })
        
        result = transformer.transform(df_test)
        
        # Verificar que los valores nulos estén estandarizados
        assert result['col1'].isna().sum() == 4  # NA, N/A, na, NaN deben ser NaN
        assert result['col1'].notna().sum() == 1  # Solo 'value' debe quedar
    
    def test_transform_trims_strings(self):
        """Test que transform recorta espacios en strings."""
        transformer = DataCleanerTransformer()
        df_train = pd.DataFrame({
            'text_col': ['  a  ', '  b  ', '  c  ']
        })
        
        transformer.fit(df_train)
        df_test = pd.DataFrame({
            'text_col': ['  hello  ', '  world  ']
        })
        
        result = transformer.transform(df_test)
        
        assert result['text_col'].iloc[0] == 'hello'
        assert result['text_col'].iloc[1] == 'world'
    
    def test_transform_drops_all_null_columns(self):
        """Test que transform elimina columnas 100% nulas."""
        transformer = DataCleanerTransformer()
        df_train = pd.DataFrame({
            'col1': [1, 2, 3],
            'null_col': [np.nan, np.nan, np.nan],
            'col2': ['a', 'b', 'c']
        })
        
        transformer.fit(df_train)
        df_test = pd.DataFrame({
            'col1': [4, 5],
            'null_col': [np.nan, np.nan],
            'col2': ['d', 'e']
        })
        
        result = transformer.transform(df_test)
        
        # La columna null_col debe ser eliminada
        assert 'null_col' not in result.columns
        assert 'col1' in result.columns
        assert 'col2' in result.columns
    
    def test_fit_transform_workflow(self):
        """Test del flujo completo fit + transform."""
        transformer = DataCleanerTransformer()
        df = pd.DataFrame({
            'numeric': [1, 2, 3],
            'text': ['  a  ', '  b  ', '  c  '],
            'null_col': [np.nan, np.nan, np.nan]
        })
        
        transformer.fit(df)
        result = transformer.transform(df)
        
        # Verificar que el resultado tiene el formato correcto
        assert isinstance(result, pd.DataFrame)
        assert 'null_col' not in result.columns
        assert result['text'].iloc[0] == 'a'

