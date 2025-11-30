from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from services.analysis_service import analyze_pseudocode
from services.completion_service import CompletionService
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Complexity Analyzer API",
    description="API base con FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root():
    """
    Endpoint raíz de la API
    """
    return {"message": "Bienvenido a la API", "status": "ok"}


@app.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "complexity-analyzer"}
    )


@app.get("/api/v1/info")
async def get_info():
    """
    Endpoint de información de la API
    """
    return {
        "name": "Complexity Analyzer API",
        "version": "1.0.0",
        "framework": "FastAPI"
    }


@app.post("/analyze-by-system")
def analyze_endpoint(payload: dict):
    """
    Endpoint para analizar la complejidad de pseudocódigo.
    Recibe un payload con el código en el campo 'code' y devuelve
    el análisis de complejidad.
    """
    pseudocode = payload.get("code", "")
    result = analyze_pseudocode(pseudocode)
    return result


@app.post("/complete-code")
def complete_code_endpoint(payload: dict):
    """
    Endpoint para completar pseudocódigo usando IA.
    Recibe un payload con el código en el campo 'code' y detecta
    comentarios que inician con "completar" o "Completar" para
    generar el código faltante.
    
    Retorna:
    - code: El pseudocódigo completo (original o completado)
    """
    try:
        pseudocode = payload.get("code", "")
        
        if not pseudocode:
            raise HTTPException(
                status_code=400,
                detail="El campo 'code' es requerido y no puede estar vacío"
            )
        
        completion_service = CompletionService()
        completed_code = completion_service.complete_code(pseudocode)
        
        return {
            "code": completed_code
        }
        
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al completar el código: {str(e)}")
