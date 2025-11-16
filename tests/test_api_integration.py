"""
Tests de integración para la API completa.
"""

import pytest
import requests
import time
from API.schemas import Gender, YesNo, CAEC, CALC, MTRANS


# URL base de la API
API_BASE_URL = "http://localhost:8000"


class TestAPIIntegration:
    """Tests de integración end-to-end de la API."""
    
    @pytest.fixture(scope="class")
    def api_running(self):
        """Verifica que la API esté corriendo."""
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=2)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("API no está corriendo. Inicia la API con: python run_api.py")
    
    def test_root_endpoint(self, api_running):
        """Test que el endpoint raíz responde."""
        response = requests.get(f"{API_BASE_URL}/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_docs_endpoint(self, api_running):
        """Test que la documentación Swagger está disponible."""
        response = requests.get(f"{API_BASE_URL}/docs")
        
        assert response.status_code == 200
    
    def test_predict_endpoint_valid_request(self, api_running):
        """Test que el endpoint de predicción funciona con un request válido."""
        request_data = {
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
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/predict",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert "prediction" in data
        assert "probabilities" in data
        assert "confidence" in data
        assert "model_version" in data
        assert "model_id" in data
        assert "prediction_id" in data
        assert "timestamp" in data
        assert "processing_time_ms" in data
        
        # Verificar que la predicción es una clase válida
        valid_classes = [
            "Insufficient_Weight",
            "Normal_Weight",
            "Overweight_Level_I",
            "Overweight_Level_II",
            "Obesity_Type_I",
            "Obesity_Type_II",
            "Obesity_Type_III"
        ]
        assert data["prediction"] in valid_classes
        
        # Verificar que las probabilidades suman aproximadamente 1.0
        probs = data["probabilities"]
        total = sum(probs.values())
        assert abs(total - 1.0) < 0.01
    
    def test_predict_endpoint_invalid_gender(self, api_running):
        """Test que el endpoint valida el género correctamente."""
        request_data = {
            "Gender": "Invalid",  # Valor inválido
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
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/predict",
            json=request_data
        )
        
        # Debe retornar un error de validación (422)
        assert response.status_code == 422
    
    def test_predict_endpoint_missing_field(self, api_running):
        """Test que el endpoint valida campos requeridos."""
        request_data = {
            # Falta el campo "Gender"
            "Age": 21.0,
            "Height": 1.62,
            "Weight": 64.0,
            # ... otros campos
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/predict",
            json=request_data
        )
        
        # Debe retornar un error de validación (422)
        assert response.status_code == 422
    
    def test_predict_endpoint_invalid_age_range(self, api_running):
        """Test que el endpoint valida rangos de edad."""
        request_data = {
            "Gender": "Female",
            "Age": 200.0,  # Edad inválida (debe estar entre 0 y 120)
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
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/predict",
            json=request_data
        )
        
        # Debe retornar un error de validación (422)
        assert response.status_code == 422

