# Documentación del Servicio de Análisis por LLM

Este documento explica el funcionamiento del servicio de análisis de complejidad computacional usando inteligencia artificial (`services/llm_analysis_service.py`).

## Introducción

El servicio de análisis por LLM utiliza inteligencia artificial para analizar pseudocódigo y generar un análisis completo de complejidad computacional. A diferencia del análisis tradicional, este servicio utiliza un modelo de lenguaje (Claude de Anthropic) para proporcionar un análisis detallado y explicativo que incluye múltiples aspectos del algoritmo.

## ¿Qué hace el servicio?

El servicio recibe pseudocódigo y genera automáticamente:

- **Análisis básico de complejidad**: Notación Big O (peor caso), Omega (mejor caso) y Theta (caso promedio)
- **Análisis paso a paso**: Explicación línea por línea de cómo funciona el código
- **Clasificación de patrones**: Identifica técnicas algorítmicas (Divide y Conquista, Programación Dinámica, etc.)
- **Representación matemática**: Ecuaciones y relaciones de recurrencia cuando aplica
- **Diagramas de ejecución**: Visualizaciones del flujo del algoritmo
- **Análisis de costo**: Estimación de tiempo de ejecución por instrucción
- **Recomendaciones**: Sugerencias de optimización cuando es posible

## Componentes Principales

### Clase LLMAnalysisService

Servicio principal que gestiona el análisis de pseudocódigo usando IA.

#### Dependencias

- **LLMService**: Servicio para interactuar con la API de Claude (`services/llm_service.py`)
- **Template de prompt**: Archivo `prompts/analyze_by_llm.txt` que contiene las instrucciones detalladas para el LLM

#### Método Principal

##### `analyze_pseudocode(pseudocode: str) -> Dict[str, Any]`

Método principal que ejecuta el análisis:

1. Carga el template de prompt con las instrucciones
2. Construye el prompt combinando el template con el pseudocódigo
3. Envía la solicitud al LLM para generar el análisis
4. Procesa y estructura la respuesta
5. Retorna un diccionario con todo el análisis completo

## Flujo de Funcionamiento

```
1. Pseudocódigo de entrada
   ↓
2. Carga del template de prompt
   ↓
3. Construcción del prompt (template + pseudocódigo)
   ↓
4. Generación con LLM (Claude)
   ↓
5. Procesamiento de la respuesta JSON
   ↓
6. Análisis completo estructurado
```

## Uso del Endpoint

### Endpoint: `/analyze-by-llm`

**Método:** `POST`

**Descripción:** Analiza pseudocódigo usando IA para generar un análisis completo de complejidad computacional.

**Request Body:**
```json
{
  "pseudocode": "for i ← 1 to n do begin\n    x ← x + i\nend"
}
```

**Response (éxito):**
```json
{
  "pseudocode": "...",
  "basic_complexity": {
    "big_o": "O(n)",
    "omega": "Ω(n)",
    "theta": "Θ(n)",
    "tight_bound": true
  },
  "step_by_step_analysis": [...],
  "pattern_classification": {...},
  "mathematical_representation": {...},
  "execution_diagram": {...},
  "cost_analysis": {...},
  "llm_metadata": {...}
}
```

**Códigos de estado:**
- `200`: Análisis exitoso
- `400`: Campo 'pseudocode' faltante o vacío
- `500`: Error interno (API key no configurada, error de comunicación con LLM, etc.)

## Ejemplos de Uso

### Ejemplo usando Python

```python
from services.llm_analysis_service import LLMAnalysisService

pseudocode = """
for i ← 1 to n do begin
    for j ← 1 to n do begin
        resultado ← resultado + A[i][j]
    end
end
"""

service = LLMAnalysisService()
analysis = service.analyze_pseudocode(pseudocode)
print(analysis["basic_complexity"]["big_o"])  # O(n²)
```

### Ejemplo usando la API

```python
import requests

url = "http://localhost:8000/analyze-by-llm"
payload = {
    "pseudocode": """
    for i ← 1 to n do begin
        x ← x + i
    end
    """
}

response = requests.post(url, json=payload)
result = response.json()
print(result["basic_complexity"])
```

## Configuración Requerida

### Variables de Entorno

El servicio requiere las siguientes variables de entorno:

- **`ANTHROPIC_API_KEY`**: API key de Anthropic para acceder a Claude (requerida)
- **`CLAUDE_MODEL`**: Modelo de Claude a usar (opcional, por defecto: `claude-3-5-sonnet-20240620`)

**Ejemplo de archivo `.env`:**
```
ANTHROPIC_API_KEY=tu_api_key_aqui
CLAUDE_MODEL=claude-3-5-sonnet-20240620
```

### Archivos Requeridos

El servicio necesita que exista el siguiente archivo:

1. **`prompts/analyze_by_llm.txt`**: Template con las instrucciones detalladas para el LLM que define qué tipo de análisis debe generar

## Características Importantes

### Análisis Completo

El servicio genera un análisis exhaustivo que va más allá de solo calcular la complejidad, incluyendo explicaciones, diagramas y recomendaciones.

### Respuesta Estructurada

La respuesta del LLM se estructura en formato JSON con campos bien definidos para facilitar su uso y procesamiento.

### Metadatos

Cada análisis incluye metadatos como el tiempo de procesamiento y el modelo utilizado, útiles para monitoreo y depuración.

## Manejo de Errores

El servicio maneja los siguientes errores:

1. **Pseudocódigo vacío**: El endpoint retorna error 400
2. **API key no configurada**: Lanza `ValueError` con mensaje descriptivo
3. **Archivo de prompt faltante**: Lanza `FileNotFoundError` con la ruta del archivo
4. **Error de comunicación con LLM**: Lanza `Exception` con el mensaje de error

## Limitaciones

1. **Dependencia de API externa**: Requiere conexión a internet y API key válida
2. **Tiempo de respuesta**: El análisis puede tardar varios segundos dependiendo de la complejidad del código
3. **Calidad del análisis**: Depende de la calidad del modelo LLM y de cómo interprete el pseudocódigo
4. **Costo**: Cada análisis consume tokens de la API de Anthropic

## Referencias

- **LLM Service**: `services/llm_service.py` - Servicio para interactuar con Claude
- **Template de prompt**: `prompts/analyze_by_llm.txt` - Instrucciones detalladas para el LLM
- **Endpoint**: `main.py` - Endpoint `/analyze-by-llm` de la API
- **Modelos de respuesta**: `models/responses.py` - Estructura de la respuesta `AnalyzeByLLMResponse`

