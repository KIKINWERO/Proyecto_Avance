"""Script para probar el endpoint de predicción de la API."""

import requests
import json
from typing import Dict, Any


def test_predict_endpoint(base_url: str = "http://localhost:8000") -> None:
    """
    Prueba el endpoint /api/v1/predict con datos dummy.
    
    Args:
        base_url: URL base de la API (por defecto http://localhost:8000)
    """
    endpoint = f"{base_url}/api/v1/predict"
    
    # Datos dummy para la predicción
    dummy_data: Dict[str, Any] = {
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
    
    print("=" * 60)
    print("Prueba del Endpoint de Predicción")
    print("=" * 60)
    print(f"\nURL: {endpoint}")
    print(f"\nDatos enviados:")
    print(json.dumps(dummy_data, indent=2, ensure_ascii=False))
    print("\n" + "-" * 60)
    
    try:
        # Realizar la petición POST
        print("\nEnviando petición...")
        response = requests.post(
            endpoint,
            json=dummy_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Mostrar resultados
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("\n✅ Predicción exitosa!")
            result = response.json()
            print("\nRespuesta:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # Mostrar información clave
            print("\n" + "=" * 60)
            print("Resumen de la Predicción:")
            print("=" * 60)
            print(f"Predicción: {result.get('prediction')}")
            print(f"Confianza: {result.get('confidence')}")
            print(f"Versión del Modelo: {result.get('model_version')}")
            print(f"ID de Predicción: {result.get('prediction_id')}")
            print(f"Tiempo de Procesamiento: {result.get('processing_time_ms')} ms")
            print("\nProbabilidades:")
            if 'probabilities' in result:
                for class_name, prob in result['probabilities'].items():
                    print(f"  - {class_name}: {prob:.4f}")
        else:
            print(f"\n❌ Error en la petición")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar a la API")
        print(f"Asegúrate de que la API esté ejecutándose en {base_url}")
        print("Ejecuta: python run_api.py")
    except requests.exceptions.Timeout:
        print("\n❌ Error: La petición tardó demasiado tiempo")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error en la petición: {str(e)}")
    except json.JSONDecodeError:
        print("\n❌ Error: La respuesta no es un JSON válido")
        print(f"Respuesta: {response.text}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    import sys
    
    # Permitir pasar la URL como argumento
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    test_predict_endpoint(base_url)

