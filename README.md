# Complexity Analyzer

**Complexity Analyzer** es una herramienta desarrollada con FastAPI que analiza la complejidad computacional de código escrito en pseudocódigo. El sistema parsea el código, genera un Árbol de Sintaxis Abstracta (AST) y calcula automáticamente las notaciones de complejidad Big O (O), Omega (Ω) y Theta (Θ).

## Introducción

Este proyecto proporciona una API REST que permite analizar la complejidad algorítmica de pseudocódigo. El sistema está compuesto por tres componentes principales:

1. **Parser**: Convierte código en pseudocódigo a un AST estructurado
2. **Analizador de Complejidad**: Evalúa el AST y calcula las complejidades computacionales
3. **API REST**: Expone la funcionalidad mediante endpoints HTTP

El analizador soporta múltiples estructuras de control (ciclos FOR, WHILE, REPEAT-UNTIL), condicionales (IF-THEN-ELSE), recursión, y operaciones con arreglos y strings, detectando automáticamente patrones de complejidad como ciclos anidados, salidas tempranas y diferentes tipos de recursión.

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

- `GET /` - Endpoint raíz que devuelve un mensaje de bienvenida
- `GET /health` - Verificación del estado de la API
- `GET /api/v1/info` - Información de la API (nombre, versión, framework)
- `POST /analyze-by-system` - Analiza la complejidad de código en pseudocódigo

### Ejemplo de uso del endpoint de análisis

```bash
curl -X POST "http://localhost:8000/analyze-by-system" \
  -H "Content-Type: application/json" \
  -d '{"code": "for i ← 1 to n do begin\n    x ← x + 1\nend"}'
```

## Funciones Principales

### `analyze_pseudocode(text: str)`
**Ubicación**: `services/analysis_service.py`

Función principal que integra el parser y el analizador de complejidad. Recibe código en pseudocódigo como texto plano, lo parsea a un AST, analiza su complejidad y devuelve un JSON con los resultados.

**Parámetros**:
- `text`: Código en pseudocódigo a analizar

**Retorna**: Diccionario con las notaciones de complejidad (O, Omega, Theta) y detalles del análisis, o un diccionario con error si hay problemas de sintaxis o análisis.

### `PseudocodeParser.parse(text: str)`
**Ubicación**: `syntax/parser.py`

Parsea código en pseudocódigo y lo convierte en un AST (Árbol de Sintaxis Abstracta) estructurado. Utiliza la gramática definida en `grammar.lark` para validar y transformar el código.

**Parámetros**:
- `text`: Código en pseudocódigo a parsear

**Retorna**: AST en formato de diccionario de Python

### `ComplexityAnalyzer.analyze(ast)`
**Ubicación**: `analyzer/complexity.py`

Analiza un AST y calcula la complejidad computacional del código. Evalúa recursivamente todos los nodos del árbol, detecta ciclos, recursión, condicionales y operaciones especiales, y retorna las notaciones Big O, Omega y Theta.

**Parámetros**:
- `ast`: Árbol de sintaxis abstracta generado por el parser

**Retorna**: Diccionario con:
  - `O`: Notación Big O (peor caso)
  - `Omega`: Notación Omega (mejor caso)
  - `Theta`: Notación Theta (caso promedio, o "N/A" si no existe)
  - `details`: Detalles del análisis (ciclos detectados, recursión, etc.)

## Estructura del proyecto

```
complexity-analyzer/
├── main.py                    # Aplicación principal FastAPI
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Este archivo
├── analyzer/
│   └── complexity.py         # Analizador de complejidad computacional
├── services/
│   └── analysis_service.py   # Servicio que integra parser y analizador
├── syntax/
│   ├── grammar.lark          # Gramática del pseudocódigo (Lark)
│   └── parser.py             # Parser y transformador de código
├── docs/
│   ├── README_complexity.md  # Documentación del analizador de complejidad
│   ├── README_grammar.md     # Documentación de la gramática
│   └── README_parser.md      # Documentación del parser
└── tests/
    └── test_*.py             # Tests unitarios del proyecto
```

## Documentación Adicional

Para información más detallada sobre los componentes del sistema, consulta los siguientes documentos:

- **[Documentación del Analizador de Complejidad](docs/README_complexity.md)**: Explica cómo funciona el cálculo de complejidad, los tipos de recursión detectados, y cómo se manejan ciclos anidados y salidas tempranas.

- **[Documentación de la Gramática](docs/README_grammar.md)**: Describe la sintaxis del pseudocódigo soportado, incluyendo estructuras de control, operadores, y tipos de datos.

- **[Documentación del Parser](docs/README_parser.md)**: Detalla cómo el parser convierte código en pseudocódigo a un AST estructurado y la transformación de nodos.

## Características

- ✅ Análisis de complejidad Big O, Omega y Theta
- ✅ Soporte para ciclos FOR, WHILE y REPEAT-UNTIL
- ✅ Detección de ciclos anidados
- ✅ Análisis de condicionales IF-THEN-ELSE
- ✅ Detección de recursión (simple, divide y vencerás, exponencial)
- ✅ Detección de salidas tempranas (return/break)
- ✅ Análisis de operaciones con arreglos y strings
- ✅ API REST con documentación interactiva
- ✅ Manejo de errores de sintaxis

## Ejemplo de Uso

```python
from services.analysis_service import analyze_pseudocode

code = """
for i ← 1 to n do begin
    for j ← 1 to n do begin
        x ← x + 1
    end
end
"""

result = analyze_pseudocode(code)
print(result["O"])      # "O(n^2)"
print(result["Omega"])  # "Ω(n^2)"
print(result["Theta"])  # "Θ(n^2)"
```

