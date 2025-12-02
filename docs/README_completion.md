# Documentación del Servicio de Completado de Código

Este documento explica el funcionamiento del servicio de completado de código (`services/completion_service.py`).

## Introducción

El servicio de completado de código utiliza inteligencia artificial (IA) para completar automáticamente pseudocódigo que contiene comentarios especiales marcados con "completar" o "Completar". El servicio detecta estos comentarios, genera el código faltante usando un modelo de lenguaje (Claude de Anthropic) y reemplaza los comentarios con el código generado, manteniendo el resto del código intacto.

## Componentes Principales

### Clase CompletionService

Servicio principal que gestiona el proceso de completado de código.

#### Dependencias

- **LLMService**: Servicio para interactuar con la API de Claude (`services/llm_service.py`)
- **Template de prompt**: Archivo `prompts/complete_pseudocode.txt` que contiene las instrucciones para el LLM
- **Gramática**: Archivo `syntax/grammar.lark` que define la sintaxis válida del pseudocódigo

#### Métodos Principales

##### `__init__()`

Inicializa el servicio cargando:
- El servicio LLM (`LLMService`)
- La ruta al template de prompt (`prompts/complete_pseudocode.txt`)

##### `_has_completion_comments(code: str) -> bool`

Verifica si el código contiene comentarios de completado. Busca el patrón `►\s*[Cc]ompletar` (case-insensitive).

**Ejemplo de comentarios detectados:**
```
► Completar la condición del if
► completar el cuerpo del ciclo
```

##### `_load_prompt_template() -> str`

Carga el template del prompt desde el archivo `prompts/complete_pseudocode.txt`.

##### `_load_grammar() -> str`

Carga la gramática del pseudocódigo desde `syntax/grammar.lark` para asegurar que el código generado sea válido.

##### `_build_prompt(code: str, grammar: str, template: str) -> str`

Construye el prompt final combinando:
- El template con las instrucciones
- La gramática del pseudocódigo
- El código a completar

##### `_clean_markdown_blocks(code: str) -> str`

Limpia bloques de código markdown que el LLM pueda haber generado. Remueve triple comillas invertidas (```) al inicio y final del código para asegurar que solo se retorne código plano.

##### `complete_code(code: str) -> str`

Método principal que ejecuta el proceso de completado:

1. Verifica si hay comentarios de completado
2. Si no hay comentarios, retorna el código original sin modificar
3. Si hay comentarios:
   - Carga el template y la gramática
   - Construye el prompt
   - Genera el código completado usando el LLM
   - Limpia bloques de markdown
   - Preserva el formato original (saltos de línea, espacios)
   - Retorna el código completado

## Flujo de Funcionamiento

```
1. Código con comentarios de completado
   ↓
2. Detección de comentarios (► Completar...)
   ↓
3. Construcción del prompt (template + gramática + código)
   ↓
4. Generación con LLM (Claude)
   ↓
5. Limpieza de markdown
   ↓
6. Preservación de formato
   ↓
7. Código completado
```

## Uso del Endpoint

### Endpoint: `/complete-code`

**Método:** `POST`

**Descripción:** Completa pseudocódigo usando IA cuando detecta comentarios de completado.

**Request Body:**
```json
{
  "pseudocode": "código en pseudocódigo con comentarios ► Completar..."
}
```

**Response (éxito):**
```json
{
  "pseudocode": "código completado sin comentarios"
}
```

**Response (error):**
```json
{
  "detail": "mensaje de error"
}
```

**Códigos de estado:**
- `200`: Completado exitoso
- `400`: Campo 'pseudocode' faltante o vacío
- `500`: Error interno (API key no configurada, error de comunicación con LLM, etc.)

## Ejemplos de Uso

### Ejemplo 1: Completado simple

**Código de entrada:**
```
if (x > 0) then begin
    ► Completar la operación de suma
end
```

**Código de salida:**
```
if (x > 0) then begin
    resultado 🡨 x + 1
end
```

### Ejemplo 2: Múltiples comentarios

**Código de entrada:**
```
for i 🡨 1 to n do begin
    if (► Completar la condición) then begin
        ► Completar el cuerpo del if
    end
end
```

**Código de salida:**
```
for i 🡨 1 to n do begin
    if (i mod 2 = 0) then begin
        suma 🡨 suma + i
    end
end
```

### Ejemplo 3: Sin comentarios de completado

**Código de entrada:**
```
for i 🡨 1 to n do begin
    x 🡨 x + 1
end
```

**Código de salida:** (sin cambios)
```
for i 🡨 1 to n do begin
    x 🡨 x + 1
end
```

### Ejemplo usando Python

```python
from services.completion_service import CompletionService

code = """
for i 🡨 1 to n do begin
    ► Completar el cuerpo del ciclo
end
"""

service = CompletionService()
completed = service.complete_code(code)
print(completed)
```

### Ejemplo usando la API

```python
import requests

url = "http://localhost:8000/complete-code"
payload = {
    "pseudocode": """
    for i 🡨 1 to n do begin
        ► Completar el cuerpo del ciclo
    end
    """
}

response = requests.post(url, json=payload)
result = response.json()
print(result["pseudocode"])
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

El servicio necesita que existan los siguientes archivos:

1. **`prompts/complete_pseudocode.txt`**: Template con las instrucciones para el LLM
2. **`syntax/grammar.lark`**: Gramática del pseudocódigo para validar el código generado

## Características Importantes

### Preservación de Formato

El servicio preserva cuidadosamente:
- Saltos de línea originales
- Indentación
- Espacios en blanco
- Estructura del código

### Validación de Gramática

El código generado debe cumplir con la gramática definida en `syntax/grammar.lark`. El prompt incluye la gramática completa para guiar al LLM.

### Detección de Comentarios

Los comentarios de completado deben seguir el formato:
- Iniciar con el símbolo `►`
- Seguido de espacios opcionales
- Seguido de "completar" o "Completar" (case-insensitive)

**Patrón regex:** `►\s*[Cc]ompletar`

### Limpieza de Markdown

El servicio automáticamente remueve bloques de código markdown (triple comillas invertidas) que el LLM pueda generar, asegurando que solo se retorne código plano.

## Manejo de Errores

El servicio maneja los siguientes errores:

1. **Sin comentarios de completado**: Retorna el código original sin modificar
2. **API key no configurada**: Lanza `ValueError` con mensaje descriptivo
3. **Archivos faltantes**: Lanza `FileNotFoundError` con la ruta del archivo
4. **Error de comunicación con LLM**: Lanza `Exception` con el mensaje de error
5. **Código vacío**: El endpoint retorna error 400

## Limitaciones

1. **Dependencia de API externa**: Requiere conexión a internet y API key válida
2. **Calidad del código generado**: Depende de la calidad del modelo LLM y del prompt
3. **Validación**: El código generado no se valida sintácticamente antes de retornarse (solo se guía al LLM con la gramática)
4. **Múltiples comentarios**: Todos los comentarios se completan en una sola llamada al LLM

## Referencias

- **LLM Service**: `services/llm_service.py` - Servicio para interactuar con Claude
- **Parser**: `syntax/parser.py` - Parser del pseudocódigo
- **Gramática**: `syntax/grammar.lark` - Definición de la sintaxis
- **Template de prompt**: `prompts/complete_pseudocode.txt` - Instrucciones para el LLM
- **Endpoint**: `main.py` - Endpoint `/complete-code` de la API

