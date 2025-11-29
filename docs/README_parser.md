# Documentación del Analizador y Transformador

Este documento explica el funcionamiento del parser (`syntax/parser.py`), que convierte código en pseudocódigo a un AST (Árbol de Sintaxis Abstracta).

## Introducción

El parser realiza dos funciones principales:

1. **Análisis sintáctico**: Usa Lark para parsear el código según la gramática definida.
2. **Transformación**: Convierte el árbol de parseo en un AST estructurado (diccionarios de Python).

## Componentes

### Clase PseudocodeParser

Clase principal que proporciona la interfaz pública para parsear código.

#### Método: `parse(text: str)`

Parsea código en pseudocódigo y retorna el AST.

**Ejemplo:**
```python
from syntax.parser import PseudocodeParser

parser = PseudocodeParser()
ast = parser.parse("x 🡨 5")
```

### Clase PseudocodeTransformer

Transforma el árbol de parseo de Lark en un AST estructurado. Cada tipo de nodo tiene un método de transformación correspondiente.

## Estructura del AST

El AST es un diccionario anidado de Python con la siguiente estructura:

```python
{
    "type": "tipo_de_nodo",
    # ... campos específicos según el tipo
}
```

### Tipos de Nodos Principales

- **`program`**: Nodo raíz con el cuerpo del programa
- **`assignment`**: Asignaciones (`var`, `expr`)
- **`for`**, **`while`**, **`repeat`**: Ciclos (`var`, `start`, `end`, `body` o `condition`, `body`)
- **`if`**: Condicionales (`condition`, `then`, `else`)
- **`block`**: Bloques de código (`body`)
- **`subroutine`**: Subrutinas (`name`, `params`, `body`)
- **`call`**: Llamadas a subrutinas (`name`, `args`)
- **`var`**: Variables (`name`, `access` opcional)
- **`binop`**: Operaciones binarias (`left`, `op`, `right`)
- **`comparison`**: Comparaciones (`left`, `op`, `right`)
- **`number`**: Números literales (`value`)
- **`name`**: Identificadores (`value`)

## Ejemplo de Transformación

**Código:**
```
for i 🡨 1 to 10 do begin
    x 🡨 x + i
end
```

**AST generado:**
```python
{
    "type": "program",
    "body": [
        {
            "type": "for",
            "var": "i",
            "start": {"type": "number", "value": "1"},
            "end": {"type": "number", "value": "10"},
            "body": {
                "type": "block",
                "body": [
                    {
                        "type": "assignment",
                        "var": {"type": "var", "name": "x"},
                        "expr": {
                            "type": "binop",
                            "left": {"type": "var", "name": "x"},
                            "op": "+",
                            "right": {"type": "var", "name": "i"}
                        }
                    }
                ]
            }
        }
    ]
}
```

## Flujo de Procesamiento

```
Código Fuente → PseudocodeParser.parse() → Parser Lark → Árbol de Parseo → PseudocodeTransformer → AST
```

## Notas Importantes

1. **Ruta de gramática**: El parser busca `grammar.lark` en el mismo directorio que `parser.py`.
2. **Manejo de errores**: El parser Lark lanzará excepciones si el código no es válido sintácticamente.
3. **Tipos de datos**: Los números se mantienen como strings en el AST.
4. **Estructura**: El AST usa diccionarios de Python, no objetos de Lark.

## Referencias

- **Gramática**: `syntax/grammar.lark`
- **Analizador de complejidad**: `analyzer/complexity.py` - Consume el AST generado por este módulo
- [Documentación de Lark](https://lark-parser.readthedocs.io/)
