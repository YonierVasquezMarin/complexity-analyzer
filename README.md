# Complexity Analyzer API

API base desarrollada con FastAPI para el proyecto Complexity Analyzer.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar o descargar el proyecto

2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

El flag `--reload` permite que el servidor se recargue automáticamente cuando detecte cambios en el código.

## Acceso a la API

Una vez iniciado el servidor, la API estará disponible en:

- **API Base**: http://localhost:8000
- **Documentación interactiva (Swagger UI)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc

## Endpoints disponibles

- `GET /` - Endpoint raíz
- `GET /health` - Verificación del estado de la API
- `GET /api/v1/info` - Información de la API

## Estructura del proyecto

```
complexity-analyzer/
├── main.py              # Aplicación principal FastAPI
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Este archivo
```

