"""
Modelos de entrada (requests) para los endpoints de la API
"""

from pydantic import BaseModel, Field


class AnalyzeCodeRequest(BaseModel):
    """
    Modelo de entrada para el endpoint /analyze-by-system
    """
    pseudocode: str = Field(
        ...,
        description="Código en pseudocódigo a analizar",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "pseudocode": "for i 🡨 1 to n do begin\n    x 🡨 x + i\nend"
            }
        }


class CompleteCodeRequest(BaseModel):
    """
    Modelo de entrada para el endpoint /complete-code
    """
    pseudocode: str = Field(
        ...,
        description="Código en pseudocódigo a completar",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "pseudocode": "for i 🡨 1 to n do begin\n    ► Completar la operación de suma\nend"
            }
        }


class AnalyzeByLLMRequest(BaseModel):
    """
    Modelo de entrada para el endpoint /analyze-by-llm
    """
    pseudocode: str = Field(
        ...,
        description="Pseudocódigo a analizar",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "pseudocode": "for i ← 1 to n do begin\n    for j ← 1 to n do begin\n        if (A[i][j] > max) then\n            max ← A[i][j]\n        end\n    end\nend"
            }
        }
