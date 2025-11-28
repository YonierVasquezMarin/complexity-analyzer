# Documentación del Analizador de Complejidad

Este documento explica en detalle el archivo `analyzer/complexity.py`, que contiene el motor principal para calcular la complejidad computacional del pseudocódigo interpretado por el parser.

## Índice

1. [Introducción](#introducción)
2. [Arquitectura General](#arquitectura-general)
3. [Funciones de Utilidad](#funciones-de-utilidad)
4. [Clase ComplexityAnalyzer](#clase-complexityanalyzer)
5. [Métodos de Análisis](#métodos-de-análisis)
6. [Detección de Recursión](#detección-de-recursión)
7. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Introducción

El archivo `complexity.py` es el núcleo del sistema de análisis de complejidad computacional. Su función principal es:

1. **Recibir un AST** generado por el parser (`parser/parser.py`)
2. **Analizar recursivamente** cada nodo del árbol
3. **Calcular la complejidad** según las estructuras de control encontradas
4. **Retornar notaciones** Big O, Omega y Theta junto con detalles del análisis

El analizador soporta:
- Ciclos: `FOR`, `WHILE`, `REPEAT`
- Condicionales: `IF-ELSE`
- Subrutinas y recursión
- Secuencias de sentencias

---

## Arquitectura General

El archivo se estructura en dos componentes principales:

```
complexity.py
├── Funciones de Utilidad (líneas 13-35)
│   ├── BigO() - Selección de complejidad dominante
│   ├── combine_multiplicative() - Multiplicación de complejidades
│   └── combine_additive() - Suma de complejidades
└── Clase ComplexityAnalyzer (líneas 42-213)
    ├── analyze() - Punto de entrada principal
    ├── _analyze_node() - Evaluación recursiva del AST
    ├── Métodos de análisis por tipo de nodo
    └── _detect_recursion() - Heurísticas de recursión
```

### Formato de Datos

**Importante:** El analizador ahora trabaja con **diccionarios** en lugar de objetos de Lark directamente. Los nodos del AST son diccionarios con una clave `"type"` que identifica el tipo de nodo, y otras claves específicas según el tipo (como `"body"`, `"then"`, `"else"`, `"name"`, etc.).

### Flujo de Procesamiento

```
AST → ComplexityAnalyzer.analyze() → _analyze_node() → Cálculo de complejidad → Resultado
```

---

## Funciones de Utilidad

### `BigO(expr_list)`

**Ubicación:** Líneas 13-20

Combina múltiples complejidades y retorna la dominante según el orden de crecimiento.

**Parámetros:**
- `expr_list` (list): Lista de expresiones de complejidad (ej: `["n", "log n", "n^2"]`)

**Retorna:**
- `str`: La complejidad dominante de la lista

**Orden de complejidades reconocidas:**
```python
["1", "log n", "n", "n log n", "n^2", "n^3", "2^n"]
```

**Ejemplo:**
```python
BigO(["n", "log n", "n^2"])  # Retorna "n^2"
BigO([])  # Retorna "1"
```

**Comportamiento:**
- Si la lista está vacía, retorna `"1"` (complejidad constante)
- Si una expresión no está en el orden conocido, se le asigna la máxima prioridad
- Selecciona la expresión con mayor índice en el orden (mayor complejidad)

---

### `combine_multiplicative(a, b)`

**Ubicación:** Líneas 23-30

Aplica reglas de multiplicación de complejidades (usado para ciclos anidados o ciclos con cuerpo complejo).

**Parámetros:**
- `a` (str): Primera expresión de complejidad
- `b` (str): Segunda expresión de complejidad

**Retorna:**
- `str`: Resultado de la multiplicación

**Reglas implementadas:**
- `1 * X = X` y `X * 1 = X`
- `n * log n = n log n`
- `n * n = n^2`
- Para otros casos: retorna `"{a} * {b}"` (expresión literal)

**Ejemplo:**
```python
combine_multiplicative("n", "log n")  # Retorna "n log n"
combine_multiplicative("n", "n")      # Retorna "n^2"
combine_multiplicative("1", "n")      # Retorna "n"
```

---

### `combine_additive(a, b)`

**Ubicación:** Líneas 33-35

Combina complejidades de forma aditiva (usado para secuencias de sentencias).

**Parámetros:**
- `a` (str): Primera expresión de complejidad
- `b` (str): Segunda expresión de complejidad

**Retorna:**
- `str`: La complejidad dominante entre ambas

**Comportamiento:**
- Utiliza `BigO()` para seleccionar la dominante
- Se usa cuando hay sentencias secuenciales (suma de complejidades)

**Ejemplo:**
```python
combine_additive("n", "log n")  # Retorna "n" (dominante)
combine_additive("n^2", "n")    # Retorna "n^2" (dominante)
```

---

## Clase ComplexityAnalyzer

### Inicialización

**Ubicación:** Líneas 43-48

```python
def __init__(self):
    self.details = {
        "loops": [],
        "recursion": None,
        "combination": ""
    }
```

**Atributos:**
- `details` (dict): Diccionario que almacena información detallada del análisis:
  - `loops`: Lista de ciclos detectados con su complejidad
  - `recursion`: Información sobre recursión detectada (si existe)
  - `combination`: Descripción de cómo se combinaron las complejidades

---

### Método Principal: `analyze(ast)`

**Ubicación:** Líneas 54-67

Punto de entrada principal del analizador. Recibe el AST completo y retorna un diccionario con las notaciones de complejidad.

**Parámetros:**
- `ast`: Árbol de sintaxis abstracta generado por el parser

**Retorna:**
```python
{
    "O": "O(complejidad)",      # Notación Big O
    "Omega": "Ω(complejidad)",  # Notación Omega
    "Theta": "Θ(complejidad)",  # Notación Theta
    "details": {                 # Detalles del análisis
        "loops": [...],
        "recursion": ...,
        "combination": "..."
    }
}
```

**Nota:** Actualmente, las tres notaciones (O, Omega, Theta) retornan el mismo valor, ya que el analizador calcula la complejidad exacta en la mayoría de casos simples.

**Ejemplo de uso:**
```python
from analyzer.complexity import ComplexityAnalyzer
from parser.parser import parse

code = """
for i ← 1 to n do
    x ← x + 1
"""
ast = parse(code)
analyzer = ComplexityAnalyzer()
result = analyzer.analyze(ast)

print(result["O"])  # "O(n)"
```

---

## Métodos de Análisis

### `_analyze_node(node)`

**Ubicación:** Líneas 73-101

Método central que evalúa recursivamente cada nodo del AST según su tipo.

**Parámetros:**
- `node`: Nodo del AST a analizar (diccionario o valor primitivo)

**Retorna:**
- `str`: Expresión de complejidad calculada

**Comportamiento:**
- Si el nodo no es un diccionario, retorna `"1"` (complejidad constante)
- Trabaja con diccionarios que tienen una clave `"type"` que identifica el tipo de nodo
- Los nodos ahora son diccionarios en lugar de objetos de Lark directamente

**Tipos de nodos soportados:**
- `program`: Secuencia de sentencias (accede a `node.get("body", [])`)
- `for`: Ciclo FOR
- `while`: Ciclo WHILE
- `repeat`: Ciclo REPEAT
- `if`: Condicional IF-ELSE
- `subroutine_decl`: Declaración de subrutina
- Otros: Retorna `"1"` (complejidad constante)

**Flujo:**
1. Verifica si el nodo es un diccionario
2. Extrae el tipo mediante `node.get("type")`
3. Llama al método específico correspondiente según el tipo
4. Retorna la complejidad calculada

---

### `_sequence(elements)`

**Ubicación:** Líneas 107-113

Analiza una secuencia de sentencias (suma de complejidades).

**Parámetros:**
- `elements`: Lista de nodos hijos (sentencias)

**Retorna:**
- `str`: Complejidad dominante de la secuencia

**Comportamiento:**
- Analiza cada elemento de la secuencia
- Combina las complejidades usando `combine_additive()`
- Actualiza `self.details["combination"]` con una descripción

**Ejemplo:**
```python
# Secuencia: O(n) + O(log n) = O(n)
```

---

### `_for_loop(node)`

**Ubicación:** Líneas 119-126

Analiza un ciclo FOR.

**Estructura esperada del nodo:**
```python
{
    "type": "for",
    "var": "...",
    "start": ...,
    "end": ...,
    "body": {...}  # Cuerpo del ciclo
}
```

**Comportamiento:**
- Extrae el cuerpo del ciclo mediante `node.get("body")`
- Asume complejidad de iteración `O(n)` por defecto
- Analiza recursivamente el cuerpo del ciclo
- Multiplica la complejidad de iteración por la del cuerpo usando `combine_multiplicative()`
- Registra el ciclo en `self.details["loops"]` con el mensaje "Ciclo FOR → O(n)"

**Retorna:**
- `str`: Complejidad del ciclo (típicamente `"n"` o `"n * cuerpo"`)

**Ejemplo:**
```python
# for i ← 1 to n do
#     x ← x + 1
# Complejidad: O(n)
```

---

### `_while_loop(node)`

**Ubicación:** Líneas 128-136

Analiza un ciclo WHILE.

**Estructura esperada del nodo:**
```python
{
    "type": "while",
    "condition": ...,
    "body": {...}  # Cuerpo del ciclo
}
```

**Comportamiento:**
- Extrae el cuerpo del ciclo mediante `node.get("body")`
- Similar a `_for_loop()`
- Por defecto asume `O(n)` iteraciones
- Analiza recursivamente el cuerpo del ciclo
- Multiplica la complejidad de iteración por la del cuerpo
- Registra el ciclo en `self.details["loops"]` con el mensaje "Ciclo WHILE → O(n)"

**Nota:** El analizador no evalúa la condición del WHILE para determinar el número exacto de iteraciones, asume `O(n)` por defecto.

---

### `_repeat_loop(node)`

**Ubicación:** Líneas 138-143

Analiza un ciclo REPEAT-UNTIL.

**Estructura esperada del nodo:**
```python
{
    "type": "repeat",
    "body": {...},  # Cuerpo del ciclo
    "condition": ...
}
```

**Comportamiento:**
- Extrae el cuerpo del ciclo mediante `node.get("body")`
- Similar a los otros ciclos
- Asume `O(n)` iteraciones
- Analiza recursivamente el cuerpo del ciclo
- Multiplica por la complejidad del cuerpo usando `combine_multiplicative("n", body_c)`
- Registra el ciclo en `self.details["loops"]` con el mensaje "Ciclo REPEAT → O(n)"

---

### `_if_statement(node)`

**Ubicación:** Líneas 149-158

Analiza una sentencia condicional IF-ELSE.

**Estructura esperada del nodo:**
```python
{
    "type": "if",
    "condition": ...,
    "then": {...},  # Bloque then (opcional)
    "else": {...}   # Bloque else (opcional)
}
```

**Comportamiento:**
- Extrae los bloques `then` y `else` mediante `node.get("then")` y `node.get("else")`
- Analiza todos los bloques presentes (then y else si existe)
- Retorna la complejidad dominante entre los bloques usando `BigO()`
- Usa `BigO()` para seleccionar la mayor complejidad

**Ejemplo:**
```python
# if condition then
#     O(n^2)  # bloque then
# else
#     O(n)    # bloque else
# Complejidad: O(n^2)
```

---

### `_subroutine(node)`

**Ubicación:** Líneas 164-179

Analiza una declaración de subrutina (función/procedimiento).

**Estructura esperada del nodo:**
```python
{
    "type": "subroutine_decl",
    "name": "...",
    "body": {...}  # Cuerpo de la subrutina
}
```

**Comportamiento:**
1. Extrae el bloque de la subrutina mediante `node.get("body")`
2. Detecta si hay recursión usando `_detect_recursion()`
3. Si hay recursión:
   - **Recursión simple** (`T(n-1)`): Retorna `"n"` y actualiza `self.details["recursion"]` con "T(n) = T(n-1) + cost"
   - **Recursión divide y vencerás** (`T(n/2)`): Retorna `"n log n"` y actualiza `self.details["recursion"]` con "T(n) = 2T(n/2) + cost"
4. Si no hay recursión: Retorna la complejidad del cuerpo

**Retorna:**
- `str`: Complejidad de la subrutina

**Ejemplo:**
```python
# subroutine factorial(n)
#     if n <= 1 then return 1
#     return n * factorial(n-1)
# Complejidad: O(n) (recursión simple)
```

---

## Detección de Recursión

### `_detect_recursion(node)`

**Ubicación:** Líneas 185-213

Heurística básica para detectar si una subrutina se llama a sí misma.

**Parámetros:**
- `node`: Nodo de declaración de subrutina (diccionario)

**Retorna:**
- `None`: No hay recursión
- `"simple"`: Recursión tipo `T(n-1)` (lineal)
- `"divide"`: Recursión tipo `T(n/2)` (divide y vencerás)

**Algoritmo:**
1. Extrae el nombre de la función mediante `node.get("name")`
2. Extrae el bloque de la subrutina mediante `node.get("body")`
3. Busca recursivamente en el bloque si hay un nodo con:
   - `type == "call"` y `name == nombre_de_la_función`
4. La búsqueda se realiza recursivamente en todos los valores del diccionario y elementos de listas
5. Si encuentra recursión:
   - Convierte el bloque a texto usando `str(block)`
   - Busca indicadores de división (`"/2"` o `"div 2"`) en el texto
   - Si encuentra: retorna `"divide"`
   - Si no: retorna `"simple"`

**Limitaciones:**
- Es una heurística simple basada en texto
- No analiza la estructura real de la recursión
- Puede tener falsos positivos o negativos en casos complejos
- La búsqueda de división se hace sobre la representación en texto del bloque, no sobre la estructura del AST

**Ejemplo de detección:**
```python
# Detecta recursión simple:
# factorial(n-1) → "simple"

# Detecta recursión divide y vencerás:
# merge_sort(n/2) → "divide"
```

---

## Ejemplos de Uso

### Ejemplo 1: Ciclo Simple

```python
from analyzer.complexity import ComplexityAnalyzer
from parser.parser import parse

code = """
for i ← 1 to n do
    x ← x + 1
"""

ast = parse(code)
analyzer = ComplexityAnalyzer()
result = analyzer.analyze(ast)

print(result["O"])  # "O(n)"
print(result["details"]["loops"])  # ["Ciclo FOR → O(n)"]
```

---

### Ejemplo 2: Ciclos Anidados

```python
code = """
for i ← 1 to n do
    for j ← 1 to n do
        x ← x + 1
"""

ast = parse(code)
analyzer = ComplexityAnalyzer()
result = analyzer.analyze(ast)

print(result["O"])  # "O(n^2)"
```

---

### Ejemplo 3: Secuencia de Sentencias

```python
code = """
x ← 1
for i ← 1 to n do
    x ← x + 1
y ← log(n)
"""

ast = parse(code)
analyzer = ComplexityAnalyzer()
result = analyzer.analyze(ast)

print(result["O"])  # "O(n)" (dominante)
```

---

### Ejemplo 4: Condicional

```python
code = """
if x > 0 then
    for i ← 1 to n do
        x ← x + 1
else
    x ← 1
"""

ast = parse(code)
analyzer = ComplexityAnalyzer()
result = analyzer.analyze(ast)

print(result["O"])  # "O(n)" (dominante entre then y else)
```

---

### Ejemplo 5: Subrutina con Recursión

```python
code = """
subroutine factorial(n)
    if n <= 1 then
        return 1
    else
        return n * factorial(n - 1)
"""

ast = parse(code)
analyzer = ComplexityAnalyzer()
result = analyzer.analyze(ast)

print(result["O"])  # "O(n)"
print(result["details"]["recursion"])  # "T(n) = T(n-1) + cost"
```

---

## Notas de Implementación

### Cambios Importantes

1. **Formato de AST:** El analizador ahora trabaja con diccionarios en lugar de objetos de Lark. Los nodos tienen una estructura como `{"type": "for", "body": {...}, ...}` en lugar de objetos con atributos.
2. **Tipos de nodos:** Los tipos de nodos han cambiado:
   - `for_loop` → `for`
   - `while_loop` → `while`
   - `repeat_loop` → `repeat`
   - `if_statement` → `if`
3. **Acceso a datos:** Se usa `node.get("clave")` en lugar de acceder directamente a atributos o hijos del nodo.

### Limitaciones Actuales

1. **Ciclos:** No analiza el rango real de iteraciones, asume `O(n)` por defecto
2. **Recursión:** Heurística simple basada en texto, no análisis estructural profundo
3. **Operaciones:** No considera la complejidad de operaciones individuales (solo estructuras de control)
4. **Notaciones:** O, Omega y Theta retornan el mismo valor (no distingue casos)

### Mejoras Futuras Posibles

- Análisis estático de rangos de ciclos
- Detección más sofisticada de patrones de recursión
- Consideración de complejidad de operaciones (búsquedas, ordenamientos, etc.)
- Distinción real entre O, Omega y Theta cuando sea posible

---

## Referencias

- **Parser relacionado:** `parser/parser.py` - Genera el AST que consume este módulo
- **Gramática:** `parser/grammar.lark` - Define la estructura del pseudocódigo

---

## Autor

Documentación generada para el proyecto Complexity Analyzer.

