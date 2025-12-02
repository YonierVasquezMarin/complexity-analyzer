from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from services.analysis_service import analyze_pseudocode
from services.completion_service import CompletionService
from services.llm_analysis_service import LLMAnalysisService
from models.requests import AnalyzeCodeRequest, CompleteCodeRequest, AnalyzeByLLMRequest
from models.responses import (
    RootResponse,
    HealthResponse,
    InfoResponse,
    AnalyzeCodeResponse,
    AnalyzeCodeErrorResponse,
    CompleteCodeResponse,
    ComplexityDetails,
    AnalyzeByLLMResponse
)
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Complexity Analyzer API",
    description="API base con FastAPI",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)


@app.get("/", response_model=RootResponse)
async def root():
    """
    Endpoint raíz de la API
    """
    return RootResponse(message="Bienvenido a la API", status="ok")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    return HealthResponse(status="healthy", service="complexity-analyzer")


@app.get("/api/v1/info", response_model=InfoResponse)
async def get_info():
    """
    Endpoint de información de la API
    """
    return InfoResponse(
        name="Complexity Analyzer API",
        version="1.0.0",
        framework="FastAPI"
    )


@app.post(
    "/analyze-by-system",
    response_model=Union[AnalyzeCodeResponse, AnalyzeCodeErrorResponse]
)
def analyze_endpoint(request: AnalyzeCodeRequest):
    """
    Endpoint para analizar la complejidad de pseudocódigo.
    Recibe un payload con el código en el campo 'pseudocode' y devuelve
    el análisis de complejidad.
    """
    result = analyze_pseudocode(request.pseudocode)
    
    # Verificar si hay un error en la respuesta
    if "error" in result:
        return AnalyzeCodeErrorResponse(
            error=result["error"],
            details=result.get("details", "")
        )
    
    # Construir la respuesta exitosa
    details = ComplexityDetails(
        loops=result.get("details", {}).get("loops", []),
        recursion=result.get("details", {}).get("recursion"),
        combination=result.get("details", {}).get("combination", ""),
        early_exit_detected=result.get("details", {}).get("early_exit_detected", False)
    )
    
    return AnalyzeCodeResponse(
        O=result["O"],
        Omega=result["Omega"],
        Theta=result["Theta"],
        details=details
    )


@app.post("/complete-code", response_model=CompleteCodeResponse)
def complete_code_endpoint(request: CompleteCodeRequest):
    """
    Endpoint para completar pseudocódigo usando IA.
    Recibe un payload con el código en el campo 'pseudocode' y detecta
    comentarios que inician con "completar" o "Completar" para
    generar el código faltante.
    
    Retorna:
    - code: El pseudocódigo completo (original o completado)
    """
    try:
        completion_service = CompletionService()
        completed_code = completion_service.complete_code(request.pseudocode)
        
        return CompleteCodeResponse(code=completed_code)
        
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al completar el código: {str(e)}")


@app.post("/analyze-by-llm", response_model=AnalyzeByLLMResponse)
def analyze_by_llm_endpoint(request: AnalyzeByLLMRequest):
    """
    Endpoint para analizar pseudocódigo usando LLM.
    Recibe un payload con el pseudocódigo y genera un análisis completo
    e independiente de complejidad computacional.
    
    El análisis incluye:
    - Análisis básico de complejidad (O, Ω, Θ)
    - Análisis paso a paso
    - Clasificación de patrones algorítmicos
    - Representación matemática
    - Diagramas de ejecución
    - Análisis de costo por instrucción
    - Recomendaciones de optimización
    
    Retorna:
    - Análisis completo de complejidad generado por LLM
    """
    try:
        analysis_service = LLMAnalysisService()
        analysis_result = analysis_service.analyze_pseudocode(request.pseudocode)
        
        # Convertir el diccionario a la respuesta tipada
        return AnalyzeByLLMResponse(**analysis_result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar el pseudocódigo: {str(e)}")
