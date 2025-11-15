"""Routers para los endpoints de la API."""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from loguru import logger

from API.schemas import PredictionRequest, PredictionResponse, ErrorResponse, ErrorDetail
from API.services import real_predict

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Realizar predicción de nivel de obesidad",
    description="Recibe las características de un individuo y retorna la predicción del nivel de obesidad junto con las probabilidades asociadas a cada clase.",
    responses={
        200: {"description": "Predicción exitosa"},
        400: {"model": ErrorResponse, "description": "Error de validación"},
        422: {"model": ErrorResponse, "description": "Datos inválidos"},
        503: {"model": ErrorResponse, "description": "Modelo no disponible"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
    },
)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Endpoint para realizar predicciones de niveles de obesidad.
    
    Args:
        request: Datos del individuo para la predicción
        
    Returns:
        Respuesta con la predicción y probabilidades
        
    Raises:
        HTTPException: Si hay errores en la validación o procesamiento
    """
    try:
        logger.info("Recibida solicitud de predicción")
        
        # Realizar predicción
        response = real_predict(request)
        
        logger.success(
            f"Predicción completada exitosamente: {response.prediction}"
        )
        
        return response
        
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": {"issue": str(e)},
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        )
    except Exception as e:
        logger.error(f"Error inesperado durante la predicción: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred during prediction",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        )

