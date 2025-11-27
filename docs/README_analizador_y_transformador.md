# Documentación del Analizador y Transformador

Este documento explica en detalle el archivo `parser/parser.py`, que contiene el analizador sintáctico (parser) y el transformador que convierte el árbol de parseo en un Árbol de Sintaxis Abstracta (AST).

## Índice

1. [Introducción](#introducción)
2. [Arquitectura General](#arquitectura-general)
3. [El Parser (Lark)](#el-parser-lark)
4. [El Transformador (PseudoCodeTransformer)](#el-transformador-pseudocodetransformer)
5. [Estructura del AST](#estructura-del-ast)
6. [Métodos del Transformador por Categoría](#métodos-del-transformador-por-categoría)
7. [Función de Parseo](#función-de-parseo)
8. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Introducción

El archivo `parser.py` es el núcleo del sistema de análisis sintáctico. Su función principal es:

1. **Cargar la gramática** definida en `grammar.lark`
2. **Crear un parser** usando Lark con el algoritmo LALR
3. **Transformar el árbol de parseo** en un AST estructurado mediante un Transformer personalizado
4. **Proporcionar una interfaz simple** (`parse()`) para convertir código fuente en AST

---

## Arquitectura General

El archivo se estructura en tres componentes principales:

```
parser.py
├── Carga de gramática (líneas 3-6)
├── Creación del parser Lark (línea 7)
├── Clase PseudoCodeTransformer (líneas 13-257)
│   └── Métodos de transformación organizados por categoría
└── Función parse() (líneas 262-264)
```

### Flujo de Procesamiento

```
Código Fuente → Parser Lark → Árbol de Parseo → Transformer → AST
```

---

## El Parser (Lark)

### Carga de la Gramática

```python
with open("grammar.lark", "r", encoding="utf-8") as f:
    GRAMMAR = f.read()
```

La gramática se carga desde el archivo `grammar.lark` ubicado en el mismo directorio. Esta gramática define todas las reglas sintácticas del pseudocódigo soportado.

### Creación del Parser

```python
parser = Lark(GRAMMAR, start="start", parser="lalr")
```

- **`GRAMMAR`**: La gramática cargada desde el archivo
- **`start="start"`**: Define la regla inicial de la gramática
- **`parser="lalr"`**: Utiliza el algoritmo LALR (Look-Ahead Left-to-Right) para el análisis sintáctico

El parser LALR es eficiente y adecuado para gramáticas de contexto libre, permitiendo un análisis rápido del código fuente.

---

## El Transformador (PseudoCodeTransformer)

La clase `PseudoCodeTransformer` hereda de `Transformer` de Lark y se encarga de convertir el árbol de parseo (parse tree) en un AST (Abstract Syntax Tree) estructurado.

### ¿Por qué un Transformador?

El árbol de parseo generado por Lark contiene información detallada sobre la estructura sintáctica, pero puede incluir:
- Tokens en bruto
- Nodos intermedios innecesarios
- Estructura específica de Lark

El transformador simplifica y normaliza esta estructura en un AST más limpio y fácil de procesar.

---

## Estructura del AST

El AST generado es un diccionario anidado de Python con la siguiente estructura general:

```python
{
    "type": "tipo_de_nodo",
    # ... campos específicos según el tipo
}
```

### Tipos de Nodos Principales

- **`program`**: Nodo raíz que contiene el cuerpo del programa
- **`assignment`**: Asignaciones de variables
- **`for`**, **`while`**, **`repeat`**: Estructuras de control
- **`if`**: Condicionales
- **`block`**: Bloques de código (begin...end)
- **`call`**: Llamadas a subrutinas
- **`class_decl`**: Declaraciones de clases
- **`object_decl`**: Declaraciones de objetos
- **`subroutine`**: Declaraciones de subrutinas
- **`binary_op`**: Operaciones binarias
- **`comparison`**: Comparaciones
- **`or`**, **`and`**, **`not`**: Operadores lógicos

---

## Métodos del Transformador por Categoría

### 1. Programa y Sentencias

#### `start(items)`
Convierte el nodo raíz en un objeto programa.

**Retorna:**
```python
{
    "type": "program",
    "body": items  # Lista de sentencias
}
```

#### `program(items)`
Retorna directamente la lista de sentencias.

#### `statement(items)`
Extrae la primera sentencia de la lista (normalmente hay una sola).

---

### 2. Asignaciones

#### `assignment(items)`
Transforma una asignación en un nodo estructurado.

**Retorna:**
```python
{
    "type": "assignment",
    "target": items[0],  # Variable destino
    "value": items[1]     # Expresión a asignar
}
```

#### `variable(items)`
Maneja tres tipos de variables:

1. **Variable simple** (`NAME`):
   ```python
   {"type": "var", "name": "x"}
   ```

2. **Acceso a campo** (`NAME.NAME`):
   ```python
   {
       "type": "field_access",
       "object": "casa",
       "field": "area"
   }
   ```

3. **Acceso a arreglo** (`NAME[index]`):
   ```python
   {
       "type": "array_access",
       "array": "arr",
       "index": {...}  # Expresión del índice
   }
   ```

#### `array_index(items)` y `index_range(items)`
Manejan índices de arreglos, soportando:
- Índices simples: `arr[5]`
- Rangos: `arr[1..10]`

---

### 3. Estructuras de Control

#### `for_loop(items)`
Transforma un ciclo FOR.

**Retorna:**
```python
{
    "type": "for",
    "var": "i",           # Variable contadora
    "start": {...},        # Valor inicial
    "end": {...},          # Valor final
    "body": {...}          # Bloque del ciclo
}
```

#### `while_loop(items)`
Transforma un ciclo WHILE.

**Retorna:**
```python
{
    "type": "while",
    "condition": {...},    # Condición
    "body": {...}          # Bloque del ciclo
}
```

#### `repeat_loop(items)`
Transforma un ciclo REPEAT UNTIL.

**Retorna:**
```python
{
    "type": "repeat",
    "body": {...},         # Bloque del ciclo
    "condition": {...}     # Condición (evaluada al final)
}
```

#### `if_statement(items)`
Transforma una sentencia IF, con soporte opcional para ELSE.

**Sin ELSE:**
```python
{
    "type": "if",
    "condition": {...},
    "then": {...},
    "else": None
}
```

**Con ELSE:**
```python
{
    "type": "if",
    "condition": {...},
    "then": {...},
    "else": {...}
}
```

#### `block(items)`
Transforma un bloque BEGIN...END.

**Retorna:**
```python
{
    "type": "block",
    "body": items  # Lista de sentencias
}
```

---

### 4. Llamadas a Subrutinas

#### `call(items)`
Transforma una llamada CALL.

**Retorna:**
```python
{
    "type": "call",
    "name": "nombre_funcion",
    "args": [...]  # Lista de argumentos (puede estar vacía)
}
```

#### `arg_list(items)`
Retorna directamente la lista de argumentos.

---

### 5. Programación Orientada a Objetos

#### `class_decl(items)`
Transforma una declaración de clase.

**Ejemplo:** `Casa {area color propietario}`

**Retorna:**
```python
{
    "type": "class_decl",
    "name": "Casa",
    "attributes": ["area", "color", "propietario"]
}
```

#### `object_decl(items)`
Transforma una declaración de objeto.

**Ejemplo:** `Casa miCasa`

**Retorna:**
```python
{
    "type": "object_decl",
    "class": "Casa",
    "name": "miCasa"
}
```

---

### 6. Subrutinas

#### `subroutine_decl(items)`
Transforma una declaración de subrutina.

**Retorna:**
```python
{
    "type": "subroutine",
    "name": "nombre",
    "params": [...],  # Lista de parámetros
    "body": {...}     # Bloque de la subrutina
}
```

#### `param(items)`
Maneja tres tipos de parámetros:

1. **Parámetro simple:**
   ```python
   {"type": "param", "name": "x"}
   ```

2. **Parámetro arreglo:**
   ```python
   {
       "type": "param_array",
       "name": "arr",
       "dims": [{"dim": ...}, ...]
   }
   ```

3. **Parámetro objeto:**
   ```python
   {
       "type": "param_object",
       "class": "Casa",
       "name": "casa"
   }
   ```

---

### 7. Expresiones y Condiciones

#### Jerarquía de Expresiones Lógicas

El transformador procesa las expresiones lógicas siguiendo la precedencia:

1. **`condition(items)`** → `or_expr`
2. **`or_expr(items)`** → Maneja operadores OR
3. **`and_expr(items)`** → Maneja operadores AND
4. **`not_expr(items)`** → Maneja operadores NOT
5. **`comparison(items)`** → Comparaciones (>, <, =, etc.)

**Ejemplo de OR:**
```python
{
    "type": "or",
    "left": {...},
    "right": {...}
}
```

#### Expresiones Matemáticas

1. **`expr(items)`** → Suma y resta (`+`, `-`)
2. **`term(items)`** → Multiplicación, división, mod, div (`*`, `/`, `mod`, `div`)
3. **`factor(items)`** → Factores básicos (números, variables, paréntesis)

**Ejemplo de operación binaria:**
```python
{
    "type": "binary_op",
    "left": {...},
    "op": "+",  # Operador como string
    "right": {...}
}
```

---

### 8. Tokens

#### `NAME(token)`
Convierte un token NAME en string.

#### `NUMBER(token)`
Convierte un token NUMBER en entero.

#### `REL_OP(token)`
Retorna el token de operador relacional tal cual.

---

## Función de Parseo

### `parse(code: str)`

Función principal que proporciona la interfaz pública para parsear código.

**Parámetros:**
- `code` (str): Código fuente en pseudocódigo a analizar

**Retorna:**
- Diccionario con el AST del programa

**Proceso:**
1. Parsea el código usando el parser Lark → genera un árbol de parseo
2. Transforma el árbol usando `PseudoCodeTransformer` → genera el AST
3. Retorna el AST

**Ejemplo de uso:**
```python
from parser.parser import parse

codigo = """
x 🡨 5
for i 🡨 1 to 10 do begin
    x 🡨 x + i
end
"""

ast = parse(codigo)
# Retorna:
# {
#     "type": "program",
#     "body": [
#         {
#             "type": "assignment",
#             "target": {"type": "var", "name": "x"},
#             "value": 5
#         },
#         {
#             "type": "for",
#             "var": "i",
#             "start": 1,
#             "end": 10,
#             "body": {
#                 "type": "block",
#                 "body": [
#                     {
#                         "type": "assignment",
#                         "target": {"type": "var", "name": "x"},
#                         "value": {
#                             "type": "binary_op",
#                             "left": {"type": "var", "name": "x"},
#                             "op": "+",
#                             "right": {"type": "var", "name": "i"}
#                         }
#                     }
#                 ]
#             }
#         }
#     ]
# }
```

---

## Ejemplos de Uso

### Ejemplo 1: Programa Simple con Asignación

**Código:**
```
x 🡨 10
y 🡨 x + 5
```

**AST generado:**
```python
{
    "type": "program",
    "body": [
        {
            "type": "assignment",
            "target": {"type": "var", "name": "x"},
            "value": 10
        },
        {
            "type": "assignment",
            "target": {"type": "var", "name": "y"},
            "value": {
                "type": "binary_op",
                "left": {"type": "var", "name": "x"},
                "op": "+",
                "right": 5
            }
        }
    ]
}
```

### Ejemplo 2: Ciclo FOR con Condicional

**Código:**
```
for i 🡨 1 to 10 do begin
    if (i > 5) then begin
        x 🡨 x + i
    end
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
            "start": 1,
            "end": 10,
            "body": {
                "type": "block",
                "body": [
                    {
                        "type": "if",
                        "condition": {
                            "type": "comparison",
                            "left": {"type": "var", "name": "i"},
                            "op": ">",
                            "right": 5
                        },
                        "then": {
                            "type": "block",
                            "body": [
                                {
                                    "type": "assignment",
                                    "target": {"type": "var", "name": "x"},
                                    "value": {
                                        "type": "binary_op",
                                        "left": {"type": "var", "name": "x"},
                                        "op": "+",
                                        "right": {"type": "var", "name": "i"}
                                    }
                                }
                            ]
                        },
                        "else": None
                    }
                ]
            }
        }
    ]
}
```

### Ejemplo 3: Clase y Objeto

**Código:**
```
Casa {area color propietario}
Casa miCasa
miCasa.area 🡨 100
```

**AST generado:**
```python
{
    "type": "program",
    "body": [
        {
            "type": "class_decl",
            "name": "Casa",
            "attributes": ["area", "color", "propietario"]
        },
        {
            "type": "object_decl",
            "class": "Casa",
            "name": "miCasa"
        },
        {
            "type": "assignment",
            "target": {
                "type": "field_access",
                "object": "miCasa",
                "field": "area"
            },
            "value": 100
        }
    ]
}
```

---

## Notas Importantes

1. **Ruta del archivo grammar.lark**: El código asume que `grammar.lark` está en el mismo directorio que `parser.py`. Si se ejecuta desde otro directorio, puede ser necesario ajustar la ruta.

2. **Manejo de errores**: El parser Lark lanzará excepciones si el código no es válido sintácticamente. Es recomendable envolver las llamadas a `parse()` en bloques try-except.

3. **Tipos de datos**: Los números se convierten automáticamente a enteros. Para soportar números decimales, sería necesario modificar el método `NUMBER()`.

4. **Extensibilidad**: Para agregar nuevos tipos de nodos o modificar la estructura del AST, se deben:
   - Actualizar la gramática en `grammar.lark` (si es necesario)
   - Agregar o modificar métodos en `PseudoCodeTransformer`

---

## Referencias

- **Gramática**: Ver `docs/README_gramatica.md` para detalles sobre la gramática Lark
- **Lark Documentation**: https://lark-parser.readthedocs.io/
- **AST**: Abstract Syntax Tree (Árbol de Sintaxis Abstracta)

