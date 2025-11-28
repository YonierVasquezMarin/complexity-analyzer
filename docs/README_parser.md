# Documentación del Analizador y Transformador

Este documento explica en detalle el archivo `syntax/parser.py`, que contiene el analizador sintáctico (parser) y el transformador que convierte el árbol de parseo en un Árbol de Sintaxis Abstracta (AST).

## Índice

1. [Introducción](#introducción)
2. [Arquitectura General](#arquitectura-general)
3. [La Clase PseudocodeParser](#la-clase-pseudocodeparser)
4. [El Transformador (PseudocodeTransformer)](#el-transformador-pseudocodetransformer)
5. [Estructura del AST](#estructura-del-ast)
6. [Métodos del Transformador por Categoría](#métodos-del-transformador-por-categoría)
7. [Método de Parseo](#método-de-parseo)
8. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Introducción

El archivo `syntax/parser.py` es el núcleo del sistema de análisis sintáctico. Su función principal es:

1. **Cargar la gramática** definida en `grammar.lark` ubicado en el mismo directorio
2. **Crear un parser** usando Lark con el algoritmo LALR
3. **Transformar el árbol de parseo** en un AST estructurado mediante un Transformer personalizado
4. **Proporcionar una interfaz simple** mediante la clase `PseudocodeParser` con el método `parse()`

---

## Arquitectura General

El archivo se estructura en dos componentes principales:

```
syntax/parser.py
├── Clase PseudocodeParser (líneas 4-15)
│   ├── __init__(): Carga la gramática y crea el parser Lark
│   └── parse(): Método público para parsear código
└── Clase PseudocodeTransformer (líneas 18-225)
    └── Métodos de transformación organizados por categoría
```

### Flujo de Procesamiento

```
Código Fuente → PseudocodeParser.parse() → Parser Lark → Árbol de Parseo → PseudocodeTransformer → AST
```

---

## La Clase PseudocodeParser

### Inicialización

```4:10:syntax/parser.py
class PseudocodeParser:
    def __init__(self):
        # Construir la ruta absoluta al archivo grammar.lark
        current_dir = os.path.dirname(os.path.abspath(__file__))
        grammar_path = os.path.join(current_dir, "grammar.lark")
        
        self.lark = Lark.open(grammar_path, start="program", parser="lalr")
```

La clase `PseudocodeParser` se encarga de:
- **Construir la ruta absoluta** al archivo `grammar.lark` ubicado en el mismo directorio que `parser.py`
- **Cargar la gramática** usando `Lark.open()` que lee el archivo directamente
- **Crear el parser Lark** con:
  - **`start="program"`**: Define la regla inicial de la gramática
  - **`parser="lalr"`**: Utiliza el algoritmo LALR (Look-Ahead Left-to-Right) para el análisis sintáctico

El parser LALR es eficiente y adecuado para gramáticas de contexto libre, permitiendo un análisis rápido del código fuente.

---

## El Transformador (PseudocodeTransformer)

La clase `PseudocodeTransformer` hereda de `Transformer` de Lark y se encarga de convertir el árbol de parseo (parse tree) en un AST (Abstract Syntax Tree) estructurado.

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
- **`class`**: Declaraciones de clases
- **`object`**: Declaraciones de objetos
- **`subroutine`**: Declaraciones de subrutinas
- **`binop`**: Operaciones binarias (suma, resta, multiplicación, división, etc.)
- **`comparison`**: Comparaciones
- **`or`**, **`and`**, **`not`**: Operadores lógicos
- **`var`**: Variables (simples, con acceso a campo o array)
- **`number`**: Números literales
- **`name`**: Nombres (identificadores)

---

## Métodos del Transformador por Categoría

### 1. Programa y Sentencias

#### `program(items)`
Convierte el nodo raíz en un objeto programa.

```23:24:syntax/parser.py
    def program(self, items):
        return {"type": "program", "body": items}
```

**Retorna:**
```python
{
    "type": "program",
    "body": items  # Lista de sentencias
}
```

#### `statement(items)`
Extrae la primera sentencia de la lista. Normalmente `statement` solo tiene un hijo, por lo que devuelve ese hijo directamente.

```26:28:syntax/parser.py
    def statement(self, items):
        # statement solo tiene un hijo, devolvemos ese hijo directamente
        return items[0] if items else None
```

---

### 2. Asignaciones

#### `assignment(items)`
Transforma una asignación en un nodo estructurado. Maneja diferentes casos según la cantidad de elementos recibidos.

```30:40:syntax/parser.py
    def assignment(self, items):
        # variable ASSIGN expr
        # items[0] = variable
        # items[1] = ASSIGN (🡨) - lo ignoramos
        # items[2] = expr
        if len(items) >= 3:
            return {"type": "assignment", "var": items[0], "expr": items[2]}
        elif len(items) == 2:
            return {"type": "assignment", "var": items[0], "expr": items[1]}
        else:
            return {"type": "assignment", "var": items[0], "expr": {"type": "number", "value": "0"}}
```

**Retorna:**
```python
{
    "type": "assignment",
    "var": {...},    # Variable destino (puede ser var simple, con campo o array)
    "expr": {...}    # Expresión a asignar
}
```

#### `variable(items)`
Maneja variables simples y variables con acceso (campo de objeto o índice de array).

```119:127:syntax/parser.py
    def variable(self, items):
        if not items:
            return {"type": "var", "name": "unknown"}
        
        if len(items) == 1:
            return {"type": "var", "name": self._extract_value(items[0])}
        else:
            # obj.field o arr[index]
            return {"type": "var", "name": self._extract_value(items[0]), "access": items[1]}
```

**Ejemplos:**

1. **Variable simple** (`x`):
   ```python
   {"type": "var", "name": "x"}
   ```

2. **Acceso a campo** (`casa.area`):
   ```python
   {
       "type": "var",
       "name": "casa",
       "access": {"type": "name", "value": "area"}
   }
   ```

3. **Acceso a arreglo** (`arr[5]`):
   ```python
   {
       "type": "var",
       "name": "arr",
       "access": {"type": "array_index", "range": [...]}
   }
   ```

#### `array_index(items)` y `index_range(items)`
Manejan índices de arreglos.

```129:133:syntax/parser.py
    def array_index(self, items):
        return {"type": "array_index", "range": items[0] if items else None}

    def index_range(self, items):
        return items
```

Soportan:
- Índices simples: `arr[5]`
- Rangos: `arr[1..10]`

---

### 3. Estructuras de Control

#### `for_loop(items)`
Transforma un ciclo FOR. Ignora el token ASSIGN (🡨) que aparece entre la variable y el valor inicial.

```42:56:syntax/parser.py
    def for_loop(self, items):
        # for NAME ASSIGN expr to expr do block
        # Lark filtra keywords, pero mantiene ASSIGN
        # items[0] = NAME
        # items[1] = ASSIGN (🡨) - lo ignoramos
        # items[2] = expr (start)
        # items[3] = expr (end)
        # items[4] = block
        return {
            "type": "for",
            "var": self._extract_value(items[0]),
            "start": items[2],  # Saltamos ASSIGN
            "end": items[3],
            "body": items[4],
        }
```

**Retorna:**
```python
{
    "type": "for",
    "var": "i",           # Variable contadora (string)
    "start": {...},       # Valor inicial (expresión)
    "end": {...},         # Valor final (expresión)
    "body": {...}         # Bloque del ciclo
}
```

#### `while_loop(items)`
Transforma un ciclo WHILE.

```58:63:syntax/parser.py
    def while_loop(self, items):
        return {
            "type": "while",
            "condition": items[0],
            "body": items[1],
        }
```

**Retorna:**
```python
{
    "type": "while",
    "condition": {...},   # Condición
    "body": {...}         # Bloque del ciclo
}
```

#### `repeat_loop(items)`
Transforma un ciclo REPEAT UNTIL.

```65:70:syntax/parser.py
    def repeat_loop(self, items):
        return {
            "type": "repeat",
            "body": items[0],
            "condition": items[1],
        }
```

**Retorna:**
```python
{
    "type": "repeat",
    "body": {...},        # Bloque del ciclo
    "condition": {...}    # Condición (evaluada al final)
}
```

#### `if_statement(items)`
Transforma una sentencia IF, con soporte opcional para ELSE.

```72:75:syntax/parser.py
    def if_statement(self, items):
        if len(items) == 2:
            return {"type": "if", "condition": items[0], "then": items[1], "else": None}
        return {"type": "if", "condition": items[0], "then": items[1], "else": items[2]}
```

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

```77:78:syntax/parser.py
    def block(self, items):
        return {"type": "block", "body": items}
```

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

```80:83:syntax/parser.py
    def call(self, items):
        name = self._extract_value(items[0])
        args = items[1] if len(items) > 1 else []
        return {"type": "call", "name": name, "args": args}
```

**Retorna:**
```python
{
    "type": "call",
    "name": "nombre_funcion",  # String con el nombre
    "args": [...]              # Lista de argumentos (puede estar vacía)
}
```

#### `arg_list(items)`
Retorna directamente la lista de argumentos.

```85:86:syntax/parser.py
    def arg_list(self, items):
        return items
```

---

### 5. Programación Orientada a Objetos

#### `class_decl(items)`
Transforma una declaración de clase.

```88:89:syntax/parser.py
    def class_decl(self, items):
        return {"type": "class", "name": self._extract_value(items[0]), "attrs": items[1:]}
```

**Ejemplo:** `Casa {area color propietario}`

**Retorna:**
```python
{
    "type": "class",
    "name": "Casa",  # String
    "attrs": ["area", "color", "propietario"]  # Lista de strings
}
```

#### `class_attr(items)`
Extrae el valor del atributo de clase.

```91:92:syntax/parser.py
    def class_attr(self, items):
        return self._extract_value(items[0])
```

#### `object_decl(items)`
Transforma una declaración de objeto.

```94:99:syntax/parser.py
    def object_decl(self, items):
        return {
            "type": "object",
            "class": self._extract_value(items[0]),
            "name": self._extract_value(items[1])
        }
```

**Ejemplo:** `Casa miCasa`

**Retorna:**
```python
{
    "type": "object",
    "class": "Casa",    # String
    "name": "miCasa"    # String
}
```

---

### 6. Subrutinas

#### `subroutine_decl(items)`
Transforma una declaración de subrutina. Maneja casos con y sin parámetros.

```101:106:syntax/parser.py
    def subroutine_decl(self, items):
        name = self._extract_value(items[0])
        if len(items) == 2:
            return {"type": "subroutine", "name": name, "params": [], "body": items[1]}
        else:
            return {"type": "subroutine", "name": name, "params": items[1], "body": items[2]}
```

**Retorna:**
```python
{
    "type": "subroutine",
    "name": "nombre",     # String
    "params": [...],      # Lista de parámetros (puede estar vacía)
    "body": {...}         # Bloque de la subrutina
}
```

#### `param_list(items)`
Retorna directamente la lista de parámetros.

```108:109:syntax/parser.py
    def param_list(self, items):
        return items
```

#### `param(items)`
Extrae el primer elemento de la lista de parámetros.

```111:112:syntax/parser.py
    def param(self, items):
        return items[0] if items else None
```

#### `array_dims(items)`
Retorna directamente las dimensiones del arreglo.

```114:115:syntax/parser.py
    def array_dims(self, items):
        return items
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

**`condition(items)`:**
```137:138:syntax/parser.py
    def condition(self, items):
        return items[0] if items else None
```

**`or_expr(items)`:**
```140:145:syntax/parser.py
    def or_expr(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "or", "left": items[0], "right": items[2]}
        return items[0] if items else None
```

**`and_expr(items)`:**
```147:152:syntax/parser.py
    def and_expr(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "and", "left": items[0], "right": items[2]}
        return items[0] if items else None
```

**`not_expr(items)`:**
```154:159:syntax/parser.py
    def not_expr(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return {"type": "not", "expr": items[1]}
        return items[0] if items else None
```

**`comparison(items)`:**
```161:166:syntax/parser.py
    def comparison(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "comparison", "left": items[0], "op": str(items[1]), "right": items[2]}
        return items[0] if items else None
```

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

**`expr(items)`:**
```170:178:syntax/parser.py
    def expr(self, items):
        if not items:
            return {"type": "number", "value": "0"}
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "binop", "left": items[0], "op": str(items[1]), "right": items[2]}
        # Si hay más o menos elementos, devolver el primero
        return items[0]
```

**`term(items)`:**
```180:187:syntax/parser.py
    def term(self, items):
        if not items:
            return {"type": "number", "value": "1"}
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "binop", "left": items[0], "op": str(items[1]), "right": items[2]}
        return items[0]
```

**`factor(items)`:**
```189:191:syntax/parser.py
    def factor(self, items):
        # factor siempre devuelve un solo elemento
        return items[0] if items else {"type": "number", "value": "0"}
```

**Ejemplo de operación binaria:**
```python
{
    "type": "binop",
    "left": {...},
    "op": "+",  # Operador como string
    "right": {...}
}
```

---

### 8. Tokens

#### `NAME(token)`
Convierte un token NAME en un nodo de tipo `name`.

```198:199:syntax/parser.py
    def NAME(self, token):
        return {"type": "name", "value": str(token)}
```

**Retorna:**
```python
{"type": "name", "value": "nombre_variable"}
```

#### `NUMBER(token)`
Convierte un token NUMBER en un nodo de tipo `number`. El valor se mantiene como string.

```195:196:syntax/parser.py
    def NUMBER(self, token):
        return {"type": "number", "value": str(token)}
```

**Retorna:**
```python
{"type": "number", "value": "123"}
```

#### `REL_OP(token)`, `ADD_OP(token)`, `MUL_OP(token)`
Retornan los tokens de operadores como strings.

```201:208:syntax/parser.py
    def REL_OP(self, token):
        return str(token)
    
    def ADD_OP(self, token):
        return str(token)
    
    def MUL_OP(self, token):
        return str(token)
```

### 9. Utilidades

#### `_extract_value(item)`
Método auxiliar privado que extrae el valor string de diferentes tipos de elementos (Token, string, dict, etc.).

```212:225:syntax/parser.py
    def _extract_value(self, item):
        """Extrae el valor string de diferentes tipos de elementos."""
        if item is None:
            return "unknown"
        if isinstance(item, Token):
            return str(item)
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            if "value" in item:
                return item["value"]
            if "name" in item:
                return item["name"]
        return str(item)
```

Este método es utilizado internamente para normalizar la extracción de valores de nombres y tokens en diferentes contextos.

---

## Método de Parseo

### `PseudocodeParser.parse(text: str)`

Método principal que proporciona la interfaz pública para parsear código.

```12:15:syntax/parser.py
    def parse(self, text):
        tree = self.lark.parse(text)
        transformed = PseudocodeTransformer().transform(tree)
        return transformed
```

**Parámetros:**
- `text` (str): Código fuente en pseudocódigo a analizar

**Retorna:**
- Diccionario con el AST del programa

**Proceso:**
1. Parsea el código usando el parser Lark → genera un árbol de parseo
2. Transforma el árbol usando `PseudocodeTransformer` → genera el AST
3. Retorna el AST

**Ejemplo de uso:**
```python
from syntax.parser import PseudocodeParser

parser = PseudocodeParser()

codigo = """
x 🡨 5
for i 🡨 1 to 10 do begin
    x 🡨 x + i
end
"""

ast = parser.parse(codigo)
# Retorna:
# {
#     "type": "program",
#     "body": [
#         {
#             "type": "assignment",
#             "var": {"type": "var", "name": "x"},
#             "expr": {"type": "number", "value": "5"}
#         },
#         {
#             "type": "for",
#             "var": "i",
#             "start": {"type": "number", "value": "1"},
#             "end": {"type": "number", "value": "10"},
#             "body": {
#                 "type": "block",
#                 "body": [
#                     {
#                         "type": "assignment",
#                         "var": {"type": "var", "name": "x"},
#                         "expr": {
#                             "type": "binop",
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
            "var": {"type": "var", "name": "x"},
            "expr": {"type": "number", "value": "10"}
        },
        {
            "type": "assignment",
            "var": {"type": "var", "name": "y"},
            "expr": {
                "type": "binop",
                "left": {"type": "var", "name": "x"},
                "op": "+",
                "right": {"type": "number", "value": "5"}
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
            "start": {"type": "number", "value": "1"},
            "end": {"type": "number", "value": "10"},
            "body": {
                "type": "block",
                "body": [
                    {
                        "type": "if",
                        "condition": {
                            "type": "comparison",
                            "left": {"type": "var", "name": "i"},
                            "op": ">",
                            "right": {"type": "number", "value": "5"}
                        },
                        "then": {
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
            "type": "class",
            "name": "Casa",
            "attrs": ["area", "color", "propietario"]
        },
        {
            "type": "object",
            "class": "Casa",
            "name": "miCasa"
        },
        {
            "type": "assignment",
            "var": {
                "type": "var",
                "name": "miCasa",
                "access": {"type": "name", "value": "area"}
            },
            "expr": {"type": "number", "value": "100"}
        }
    ]
}
```

---

## Notas Importantes

1. **Ruta del archivo grammar.lark**: El código construye la ruta absoluta al archivo `grammar.lark` usando `os.path.dirname(os.path.abspath(__file__))`, por lo que siempre busca el archivo en el mismo directorio que `parser.py`, independientemente del directorio de trabajo actual.

2. **Manejo de errores**: El parser Lark lanzará excepciones si el código no es válido sintácticamente. Es recomendable envolver las llamadas a `parse()` en bloques try-except.

3. **Tipos de datos**: Los números se mantienen como strings en el AST (no se convierten a enteros). Esto permite preservar el formato original y manejar números grandes sin pérdida de precisión.

4. **Estructura del AST**: 
   - Las asignaciones usan `var` y `expr` (no `target` y `value`)
   - Las operaciones binarias usan el tipo `binop` (no `binary_op`)
   - Las variables con acceso a campos o arrays incluyen un campo `access`
   - Las clases usan el tipo `class` y el campo `attrs` (no `class_decl` y `attributes`)
   - Los objetos usan el tipo `object` (no `object_decl`)

5. **Extensibilidad**: Para agregar nuevos tipos de nodos o modificar la estructura del AST, se deben:
   - Actualizar la gramática en `grammar.lark` (si es necesario)
   - Agregar o modificar métodos en `PseudocodeTransformer`

---

## Referencias

- **Gramática**: Ver `docs/README_gramatica.md` para detalles sobre la gramática Lark
- **Lark Documentation**: https://lark-parser.readthedocs.io/
- **AST**: Abstract Syntax Tree (Árbol de Sintaxis Abstracta)

