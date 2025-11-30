"""
Modelos de salida (responses) para los endpoints de la API
"""

from typing import List, Optional, Union
from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    """
    Modelo de salida para el endpoint GET /
    """
    message: str = Field(..., description="Mensaje de bienvenida")
    status: str = Field(..., description="Estado de la API")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Bienvenido a la API",
                "status": "ok"
            }
        }


class HealthResponse(BaseModel):
    """
    Modelo de salida para el endpoint GET /health
    """
    status: str = Field(..., description="Estado de salud del servicio")
    service: str = Field(..., description="Nombre del servicio")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "complexity-analyzer"
            }
        }


class InfoResponse(BaseModel):
    """
    Modelo de salida para el endpoint GET /api/v1/info
    """
    name: str = Field(..., description="Nombre de la API")
    version: str = Field(..., description="Versión de la API")
    framework: str = Field(..., description="Framework utilizado")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Complexity Analyzer API",
                "version": "1.0.0",
                "framework": "FastAPI"
            }
        }


class ComplexityDetails(BaseModel):
    """
    Modelo para los detalles de complejidad en la respuesta de análisis
    """
    loops: List[str] = Field(
        default_factory=list,
        description="Lista de ciclos detectados en el código"
    )
    recursion: Optional[str] = Field(
        None,
        description="Información sobre recursión detectada"
    )
    combination: str = Field(
        default="",
        description="Descripción de cómo se combinaron las complejidades"
    )
    early_exit_detected: bool = Field(
        default=False,
        description="Indica si se detectó una salida temprana en el código"
    )


class AnalyzeCodeResponse(BaseModel):
    """
    Modelo de salida exitosa para el endpoint POST /analyze-by-system
    """
    O: str = Field(..., description="Notación Big O (peor caso)")
    Omega: str = Field(..., description="Notación Omega (mejor caso)")
    Theta: str = Field(..., description="Notación Theta (caso promedio) o 'N/A' si no existe")
    details: ComplexityDetails = Field(..., description="Detalles del análisis de complejidad")

    class Config:
        json_schema_extra = {
            "example": {
                "O": "O(n)",
                "Omega": "Ω(n)",
                "Theta": "Θ(n)",
                "details": {
                    "loops": ["Ciclo FOR → O(n)"],
                    "recursion": None,
                    "combination": "",
                    "early_exit_detected": False
                }
            }
        }


class AnalyzeCodeErrorResponse(BaseModel):
    """
    Modelo de salida con error para el endpoint POST /analyze-by-system
    """
    error: str = Field(..., description="Mensaje de error")
    details: str = Field(..., description="Detalles del error")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Error de sintaxis en el pseudocódigo.",
                "details": "Unexpected token at line 3"
            }
        }


class CompleteCodeResponse(BaseModel):
    """
    Modelo de salida para el endpoint POST /complete-code
    """
    code: str = Field(..., description="Código completado (o original si no había comentarios de completado)")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "for i 🡨 1 to n do begin\n    x 🡨 x + i\nend"
            }
        }

