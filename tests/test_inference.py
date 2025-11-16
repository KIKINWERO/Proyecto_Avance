"""
Tests unitarios para el módulo de inferencia.
"""

import pytest
import pandas as pd
from pathlib import Path

from mlops_obesidad.inference.model_loader import load_model, get_model
from mlops_obesidad.inference.predictor import request_to_dataframe
from API.schemas import PredictionRequest, Gender, YesNo, CAEC, CALC, MTRANS


class TestModelLoader:
    """Tests para el cargador de modelos."""
    
    def test_load_model_exists(self):
        """Test que el modelo se puede cargar si existe."""
        model_path = Path("models/xgboost_model_artifacts.pkl")
        
        if not model_path.exists():
            pytest.skip("Modelo no encontrado, saltando test")
        
        artifacts = load_model()
        
        assert artifacts is not None
        assert 'model' in artifacts
        assert 'label_encoder' in artifacts
        assert len(artifacts['label_encoder'].classes_) == 7
    
    def test_get_model_returns_loaded_model(self):
        """Test que get_model retorna el modelo cargado."""
        model_path = Path("models/xgboost_model_artifacts.pkl")
        
        if not model_path.exists():
            pytest.skip("Modelo no encontrado, saltando test")
        
        artifacts = get_model()
        
        assert artifacts is not None
        assert 'model' in artifacts
        assert 'label_encoder' in artifacts


class TestPredictor:
    """Tests para las funciones de predicción."""
    
    def test_request_to_dataframe_converts_correctly(self):
        """Test que request_to_dataframe convierte correctamente."""
        request = PredictionRequest(
            Gender=Gender.FEMALE,
            Age=21.0,
            Height=1.62,
            Weight=64.0,
            family_history_with_overweight=YesNo.YES,
            FAVC=YesNo.NO,
            FCVC=2.0,
            NCP=3.0,
            CAEC=CAEC.SOMETIMES,
            SMOKE=YesNo.NO,
            CH2O=2.0,
            SCC=YesNo.NO,
            FAF=0.0,
            TUE=1.0,
            CALC=CALC.NO,
            MTRANS=MTRANS.PUBLIC_TRANSPORTATION
        )
        
        df = request_to_dataframe(request)
        
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] == 1  # Una fila
        assert df.shape[1] == 16  # 16 columnas
        assert df['Gender'].iloc[0] == 'Female'
        assert df['Age'].iloc[0] == 21.0
        assert df['Height'].iloc[0] == 1.62
    
    def test_request_to_dataframe_has_all_columns(self):
        """Test que el DataFrame tiene todas las columnas necesarias."""
        request = PredictionRequest(
            Gender=Gender.MALE,
            Age=25.0,
            Height=1.75,
            Weight=80.0,
            family_history_with_overweight=YesNo.NO,
            FAVC=YesNo.YES,
            FCVC=3.0,
            NCP=2.0,
            CAEC=CAEC.FREQUENTLY,
            SMOKE=YesNo.NO,
            CH2O=1.0,
            SCC=YesNo.YES,
            FAF=2.0,
            TUE=0.0,
            CALC=CALC.SOMETIMES,
            MTRANS=MTRANS.WALKING
        )
        
        df = request_to_dataframe(request)
        
        expected_columns = [
            'Gender', 'Age', 'Height', 'Weight',
            'family_history_with_overweight', 'FAVC', 'FCVC', 'NCP',
            'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'MTRANS'
        ]
        
        for col in expected_columns:
            assert col in df.columns, f"Columna {col} no encontrada"

