# Documentación del Analizador de Complejidad

Este documento explica el funcionamiento del analizador de complejidad computacional (`analyzer/complexity.py`).

## Introducción

El analizador de complejidad recibe un AST (Árbol de Sintaxis Abstracta) generado por el parser y calcula la complejidad computacional del código, retornando las notaciones Big O, Omega y Theta.

## Componentes Principales

### Funciones de Utilidad

- **`BigO(expr_list)`**: Selecciona la complejidad dominante de una lista de complejidades.
- **`combine_multiplicative(a, b)`**: Multiplica dos complejidades (usado para ciclos anidados).
- **`combine_additive(a, b)`**: Suma dos complejidades (usado para secuencias de sentencias).

### Clase ComplexityResult

Representa el resultado del análisis con tres casos:
- `best`: Mejor caso (Omega - Ω)
- `worst`: Peor caso (Big O - O)
- `avg`: Caso promedio (Theta - Θ)
- `has_early_exit`: Indica si hay salida temprana (return/break)

### Clase ComplexityAnalyzer

Analizador principal que procesa el AST recursivamente.

#### Método Principal: `analyze(ast)`

Punto de entrada que recibe el AST y retorna un diccionario con:
```python
{
    "O": "O(complejidad)",      # Notación Big O
    "Omega": "Ω(complejidad)",  # Notación Omega
    "Theta": "Θ(complejidad)",  # Notación Theta (o "N/A" si no existe)
    "details": {                 # Detalles del análisis
        "loops": [...],
        "recursion": ...,
        "combination": "...",
        "early_exit_detected": False
    }
}
```

## Análisis por Tipo de Estructura

### Ciclos

- **FOR**: Analiza el cuerpo y multiplica por `O(n)` iteraciones.
- **WHILE**: Similar a FOR, asume `O(n)` iteraciones.
- **REPEAT**: Similar a FOR, asume `O(n)` iteraciones.

**Ciclos anidados**: La complejidad se multiplica (ej: `n * n = n^2`).

**Salida temprana**: Si el cuerpo contiene `return` o `break` dentro de un `if`, se detecta salida temprana:
- Mejor caso: `Ω(1)` (sale en primera iteración)
- Peor caso: `O(n * cuerpo)` (recorre todo)

### Condicionales (IF)

- Analiza ambas ramas (`then` y `else` si existe).
- Mejor caso: mínimo entre ambas ramas.
- Peor caso: máximo entre ambas ramas.

### Secuencias

- Combina complejidades de forma aditiva.
- Retorna la complejidad dominante.

### Subrutinas y Recursión

El analizador detecta tres tipos de recursión:

1. **Recursión simple** (`T(n-1)`): Complejidad `O(n)`
2. **Divide y vencerás** (`T(n/2)`): Complejidad `O(n log n)`
3. **Recursión exponencial** (múltiples llamadas): Complejidad `O(2^n)`

La detección se basa en:
- Búsqueda de llamadas recursivas en el cuerpo.
- Patrones de división (operaciones `/2` o `div 2`).
- Número de llamadas recursivas.

### Operaciones Especiales

- **Concatenación de strings** (`+`): `O(n)` donde n es la longitud de los strings.
- **Declaración de arreglos**: `O(n)` donde n es el tamaño del arreglo.
- **Acceso a rangos de arreglos** (`A[1..j]`): `O(n)` para operaciones sobre el subarreglo.

## Ejemplos de Uso

```python
from analyzer.complexity import ComplexityAnalyzer
from syntax.parser import PseudocodeParser

code = """
for i ← 1 to n do begin
    x ← x + 1
end
"""

parser = PseudocodeParser()
ast = parser.parse(code)
analyzer = ComplexityAnalyzer()
result = analyzer.analyze(ast)

print(result["O"])      # "O(n)"
print(result["Omega"])  # "Ω(n)"
print(result["Theta"])  # "Θ(n)"
```

## Limitaciones

1. **Ciclos**: Asume `O(n)` iteraciones por defecto, no analiza rangos reales.
2. **Recursión**: Heurística simple basada en patrones, no análisis estructural profundo.
3. **Operaciones**: No considera la complejidad de todas las operaciones individuales.

## Referencias

- **Parser**: `syntax/parser.py` - Genera el AST que consume este módulo
- **Gramática**: `syntax/grammar.lark` - Define la estructura del pseudocódigo
