"""
Modelos de entrada (requests) para los endpoints de la API
"""

from pydantic import BaseModel, Field


class AnalyzeCodeRequest(BaseModel):
    """
    Modelo de entrada para el endpoint /analyze-by-system
    """
    code: str = Field(
        ...,
        description="Código en pseudocódigo a analizar",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "code": "for i 🡨 1 to n do begin\n    x 🡨 x + i\nend"
            }
        }


class CompleteCodeRequest(BaseModel):
    """
    Modelo de entrada para el endpoint /complete-code
    """
    code: str = Field(
        ...,
        description="Código en pseudocódigo a completar",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "code": "for i 🡨 1 to n do begin\n    ► Completar la operación de suma\nend"
            }
        }

