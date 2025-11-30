"""
Modelos de salida (responses) para los endpoints de la API
"""

from typing import List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


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


# Modelos para /analyze-by-llm
class BasicComplexity(BaseModel):
    """Análisis básico de complejidad"""
    O: str = Field(..., description="Notación Big O (peor caso)")
    Omega: str = Field(..., description="Notación Omega (mejor caso)")
    Theta: str = Field(..., description="Notación Theta (caso promedio) o 'N/A'")
    tight_bound: bool = Field(..., description="Indica si hay cota fuerte")
    summary: str = Field(..., description="Explicación breve de la complejidad")


class StepByStepItem(BaseModel):
    """Item del análisis paso a paso"""
    step: int = Field(..., description="Número de paso")
    code_line: str = Field(..., description="Línea de código analizada")
    explanation: str = Field(..., description="Explicación de qué hace")
    executions: str = Field(..., description="Número de ejecuciones")
    complexity_contribution: str = Field(..., description="Contribución a la complejidad")
    detailed_reasoning: str = Field(..., description="Razonamiento detallado")


class PatternClassification(BaseModel):
    """Clasificación de patrones algorítmicos"""
    primary_pattern: str = Field(..., description="Patrón primario identificado")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza (0-1)")
    characteristics: List[str] = Field(..., description="Características que lo identifican")
    similar_algorithms: List[str] = Field(..., description="Algoritmos similares conocidos")
    alternative_approaches: Optional[str] = Field(None, description="Enfoques alternativos")


class MathematicalRepresentation(BaseModel):
    """Representación matemática de la complejidad"""
    type: str = Field(..., description="Tipo: 'recurrence' o 'summation'")
    recurrence_relation: Optional[str] = Field(None, description="Relación de recurrencia T(n)")
    base_case: Optional[str] = Field(None, description="Caso base")
    solution_method: Optional[str] = Field(None, description="Método de solución (Teorema Maestro, etc.)")
    solution_steps: Optional[List[str]] = Field(None, description="Pasos de la resolución matemática")
    summation: Optional[str] = Field(None, description="Sumatoria para ciclos")
    expansion: Optional[str] = Field(None, description="Expansión de la sumatoria")
    final_result: str = Field(..., description="Resultado final")
    latex_notation: Optional[str] = Field(None, description="Notación LaTeX")


class RecursionTree(BaseModel):
    """Árbol de recursión"""
    format: str = Field(..., description="Formato del diagrama (ej: 'mermaid')")
    diagram: str = Field(..., description="Código del diagrama")
    depth: Optional[str] = Field(None, description="Profundidad del árbol")
    nodes_per_level: Optional[List[int]] = Field(None, description="Nodos por nivel")
    work_per_level: Optional[List[str]] = Field(None, description="Trabajo por nivel")
    total_work: Optional[str] = Field(None, description="Trabajo total")


class TraceTableItem(BaseModel):
    """Item de la tabla de traza"""
    model_config = ConfigDict(extra='allow')  # Permitir campos adicionales
    
    i: Optional[int] = Field(None, description="Valor de i")
    j: Optional[int] = Field(None, description="Valor de j")
    operation: Optional[str] = Field(None, description="Operación realizada")
    cost: Optional[str] = Field(None, description="Costo de la operación")


class TraceTable(BaseModel):
    """Tabla de traza para n pequeño"""
    input_size: int = Field(..., description="Tamaño de entrada usado")
    iterations: List[TraceTableItem] = Field(..., description="Iteraciones de la traza")
    total_operations: int = Field(..., description="Total de operaciones")


class Flowchart(BaseModel):
    """Diagrama de flujo"""
    format: str = Field(..., description="Formato del diagrama (ej: 'mermaid')")
    diagram: str = Field(..., description="Código del diagrama")


class ExecutionDiagram(BaseModel):
    """Diagramas de ejecución"""
    recursion_tree: Optional[RecursionTree] = Field(None, description="Árbol de recursión")
    trace_table: Optional[TraceTable] = Field(None, description="Tabla de traza")
    flowchart: Optional[Flowchart] = Field(None, description="Diagrama de flujo")


class InstructionBreakdown(BaseModel):
    """Desglose de costo por instrucción"""
    line: int = Field(..., description="Número de línea")
    code: str = Field(..., description="Código de la línea")
    operation_type: str = Field(..., description="Tipo de operación")
    executions_count: str = Field(..., description="Número de ejecuciones")
    time_per_execution_us: float = Field(..., description="Tiempo por ejecución en microsegundos")
    total_time_formula: str = Field(..., description="Fórmula del tiempo total")
    total_time_n_1000: str = Field(..., description="Tiempo total para n=1000")


class CostSummary(BaseModel):
    """Resumen de costos"""
    total_time_formula: str = Field(..., description="Fórmula del tiempo total")
    for_n_10: str = Field(..., description="Tiempo para n=10")
    for_n_100: str = Field(..., description="Tiempo para n=100")
    for_n_1000: str = Field(..., description="Tiempo para n=1000")
    for_n_10000: str = Field(..., description="Tiempo para n=10000")


class CostAnalysis(BaseModel):
    """Análisis de costo por instrucción"""
    instruction_breakdown: List[InstructionBreakdown] = Field(..., description="Desglose por instrucción")
    summary: CostSummary = Field(..., description="Resumen de costos")


class TokenUsage(BaseModel):
    """Uso de tokens"""
    input: int = Field(default=0, description="Tokens de entrada")
    output: int = Field(default=0, description="Tokens de salida")
    total: int = Field(default=0, description="Total de tokens")


class LLMMetadata(BaseModel):
    """Metadatos del LLM"""
    model_config = ConfigDict(protected_namespaces=())
    
    model_used: str = Field(..., description="Modelo utilizado")
    tokens: TokenUsage = Field(..., description="Tokens usados (input, output, total)")
    estimated_cost_usd: Optional[float] = Field(None, description="Costo estimado en USD")
    processing_time_ms: Optional[float] = Field(None, description="Tiempo de procesamiento en ms")


class Recommendations(BaseModel):
    """Recomendaciones de optimización"""
    optimization_suggestions: List[str] = Field(..., description="Sugerencias de optimización")
    complexity_class: str = Field(..., description="Clase de complejidad")
    scalability: str = Field(..., description="Información sobre escalabilidad")


class AnalyzeByLLMResponse(BaseModel):
    """
    Modelo de salida para el endpoint POST /analyze-by-llm
    Análisis completo de complejidad generado por LLM
    """
    pseudocode: str = Field(..., description="Pseudocódigo analizado")
    basic_complexity: BasicComplexity = Field(..., description="Análisis básico de complejidad")
    step_by_step_analysis: List[StepByStepItem] = Field(..., description="Análisis paso a paso")
    pattern_classification: PatternClassification = Field(..., description="Clasificación de patrones")
    mathematical_representation: MathematicalRepresentation = Field(..., description="Representación matemática")
    execution_diagram: Optional[ExecutionDiagram] = Field(None, description="Diagramas de ejecución")
    cost_analysis: Optional[CostAnalysis] = Field(None, description="Análisis de costo")
    llm_metadata: LLMMetadata = Field(..., description="Metadatos del LLM")
    recommendations: Recommendations = Field(..., description="Recomendaciones")