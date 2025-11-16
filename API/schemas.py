"""Schemas Pydantic para validación de request y response."""

from enum import Enum
from datetime import datetime
from typing import Dict, Optional, Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


# Enums para valores categóricos
class Gender(str, Enum):
    """Género del individuo."""

    FEMALE = "Female"
    MALE = "Male"


class YesNo(str, Enum):
    """Valores binarios yes/no."""

    YES = "yes"
    NO = "no"


class CAEC(str, Enum):
    """Consumo de alimentos entre comidas."""

    NO = "no"
    SOMETIMES = "Sometimes"
    FREQUENTLY = "Frequently"
    ALWAYS = "Always"


class CALC(str, Enum):
    """Consumo de alcohol."""

    NO = "no"
    SOMETIMES = "Sometimes"
    FREQUENTLY = "Frequently"
    ALWAYS = "Always"


class MTRANS(str, Enum):
    """Medio de transporte."""

    PUBLIC_TRANSPORTATION = "Public_Transportation"
    WALKING = "Walking"
    AUTOMOBILE = "Automobile"
    MOTORBIKE = "Motorbike"
    BIKE = "Bike"


# Request Schema
class PredictionRequest(BaseModel):
    """Schema para el request de predicción."""

    Gender: Annotated[Gender, Field(..., description="Género del individuo")]
    Age: float = Field(..., ge=0, le=120, description="Edad en años")
    Height: float = Field(..., gt=0, le=3.0, description="Altura en metros")
    Weight: float = Field(..., gt=0, le=300, description="Peso en kilogramos")
    family_history_with_overweight: Annotated[YesNo, Field(
        ..., description="Historial familiar de sobrepeso"
    )]
    FAVC: Annotated[YesNo, Field(
        ..., description="Frecuencia de consumo de alimentos altos en calorías"
    )]
    FCVC: float = Field(
        ..., ge=1.0, le=3.0, description="Frecuencia de consumo de vegetales (1-3)"
    )
    NCP: float = Field(
        ..., ge=1.0, le=4.0, description="Número de comidas principales al día"
    )
    CAEC: Annotated[CAEC, Field(..., description="Consumo de alimentos entre comidas")]
    SMOKE: Annotated[YesNo, Field(..., description="¿Fuma?")]
    CH2O: float = Field(
        ..., ge=1.0, le=3.0, description="Consumo diario de agua (1-3)"
    )
    SCC: Annotated[YesNo, Field(..., description="Monitoreo de calorías consumidas")]
    FAF: float = Field(
        ..., ge=0.0, le=3.0, description="Actividad física (0-3)"
    )
    TUE: float = Field(
        ..., ge=0.0, le=2.0, description="Tiempo usando dispositivos electrónicos (0-2)"
    )
    CALC: Annotated[CALC, Field(..., description="Consumo de alcohol")]
    MTRANS: Annotated[MTRANS, Field(..., description="Medio de transporte utilizado")]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
                "MTRANS": "Public_Transportation",
            }
        }
    )


# Response Schemas
class PredictionProbabilities(BaseModel):
    """Probabilidades para cada clase de predicción."""

    Insufficient_Weight: float = Field(..., ge=0.0, le=1.0)
    Normal_Weight: float = Field(..., ge=0.0, le=1.0)
    Overweight_Level_I: float = Field(..., ge=0.0, le=1.0)
    Overweight_Level_II: float = Field(..., ge=0.0, le=1.0)
    Obesity_Type_I: float = Field(..., ge=0.0, le=1.0)
    Obesity_Type_II: float = Field(..., ge=0.0, le=1.0)
    Obesity_Type_III: float = Field(..., ge=0.0, le=1.0)


class PredictionResponse(BaseModel):
    """Schema para la respuesta de predicción."""

    prediction: str = Field(..., description="Clase predicha (la más probable)")
    probabilities: PredictionProbabilities = Field(
        ..., description="Probabilidades para cada clase"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confianza de la predicción"
    )
    model_version: str = Field(..., description="Versión del modelo utilizado")
    model_id: str = Field(..., description="Identificador del modelo")
    prediction_id: str = Field(..., description="UUID único para esta predicción")
    timestamp: str = Field(..., description="Timestamp ISO 8601")
    processing_time_ms: float = Field(..., ge=0.0, description="Tiempo de procesamiento")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prediction": "Normal_Weight",
                "probabilities": {
                    "Insufficient_Weight": 0.05,
                    "Normal_Weight": 0.75,
                    "Overweight_Level_I": 0.12,
                    "Overweight_Level_II": 0.05,
                    "Obesity_Type_I": 0.02,
                    "Obesity_Type_II": 0.01,
                    "Obesity_Type_III": 0.00,
                },
                "confidence": 0.75,
                "model_version": "1.0.0",
                "model_id": "obesity-classifier-v1",
                "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2024-01-15T10:30:00Z",
                "processing_time_ms": 45.2,
            }
        }
    )


# Error Schemas
class ErrorDetail(BaseModel):
    """Detalle de error."""

    field: Optional[str] = None
    issue: Optional[str] = None


class ErrorResponse(BaseModel):
    """Schema para respuestas de error."""

    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje de error")
    details: Optional[ErrorDetail] = None
    timestamp: str = Field(..., description="Timestamp del error")

