from fastapi import FastAPI
from fastapi.responses import JSONResponse
from services.analysis_service import analyze_pseudocode

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
