from fastapi import FastAPI
from fastapi.responses import JSONResponse

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

