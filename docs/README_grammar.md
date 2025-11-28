# Documentación de la Gramática Lark

Este documento explica en detalle la gramática definida en `syntax/grammar.lark`, que describe el pseudocódigo soportado por el analizador de complejidad.

## Índice

1. [Introducción](#introducción)
2. [Estructura General](#estructura-general)
3. [Sentencias Principales](#sentencias-principales)
4. [Asignaciones](#asignaciones)
5. [Estructuras de Control](#estructuras-de-control)
6. [Expresiones](#expresiones)
7. [Programación Orientada a Objetos](#programación-orientada-a-objetos)
8. [Subrutinas](#subrutinas)
9. [Tokens y Reglas Especiales](#tokens-y-reglas-especiales)

---

## Introducción

La gramática está diseñada para analizar pseudocódigo que incluye:
- Estructuras de control (FOR, WHILE, REPEAT, IF)
- Asignaciones con símbolo especial
- Objetos y clases
- Arreglos
- Subrutinas y llamadas a funciones
- Expresiones matemáticas y lógicas

---

## Estructura General

### Programa

Un programa está compuesto por una o más sentencias:

```
program: statement+
```

**Ejemplo:**
```
x 🡨 5
for i 🡨 1 to 10 do begin
    x 🡨 x + i
end
```

---

## Sentencias Principales

Las sentencias que puede contener un programa son:

```
statement: assignment
         | for_loop
         | while_loop
         | repeat_loop
         | if_statement
         | call
         | class_decl
         | object_decl
         | subroutine_decl
         | COMMENT
```

Cada tipo de sentencia se detalla a continuación.

---

## Asignaciones

### Sintaxis

```
assignment: variable ASSIGN expr
```

### Operador de Asignación

El operador de asignación es el símbolo especial **🡨** (flecha hacia la izquierda):

```
ASSIGN: "🡨"
```

**Ejemplos:**
```
x 🡨 10
contador 🡨 contador + 1
miObjeto.campo 🡨 valor
arreglo[5] 🡨 100
```

### Variables

Las variables pueden ser:
- Nombres simples: `x`, `contador`, `miVariable`
- Campos de objetos: `objeto.campo`
- Elementos de arreglos: `arreglo[indice]` o `arreglo[inicio..fin]`

```
variable: NAME
        | NAME "." NAME
        | NAME array_index
```

**Ejemplos:**
```
x                    // Variable simple
casa.area            // Campo de objeto
vector[5]            // Elemento de arreglo
matriz[1..10]        // Rango de elementos
```

### Índices de Arreglos

Los arreglos soportan índices simples o rangos:

```
array_index: "[" index_range "]"
index_range: expr (".." expr)?
```

**Ejemplos:**
```
arr[5]           // Índice simple
arr[1..10]       // Rango de índices
arr[i]           // Índice con variable
arr[inicio..fin] // Rango con variables
```

---

## Estructuras de Control

### Ciclo FOR

Sintaxis:
```
for_loop: "for" NAME ASSIGN expr "to" expr "do" block
```

Donde `ASSIGN` es el símbolo `🡨` (el mismo que se usa para asignaciones).

**Ejemplo:**
```
for i 🡨 1 to 10 do begin
    x 🡨 x + i
end
```

### Ciclo WHILE

Sintaxis:
```
while_loop: "while" "(" condition ")" "do" block
```

**Ejemplo:**
```
while (x < 100) do begin
    x 🡨 x * 2
end
```

### Ciclo REPEAT UNTIL

Sintaxis:
```
repeat_loop: "repeat" block "until" "(" condition ")"
```

**Ejemplo:**
```
repeat begin
    x 🡨 x + 1
end until (x >= 100)
```

### Sentencia IF

Sintaxis:
```
if_statement: "if" "(" condition ")" "then" block ("else" block)?
```

El bloque `else` es opcional.

**Ejemplos:**
```
if (x > 0) then begin
    resultado 🡨 positivo
end

if (x > 0) then begin
    resultado 🡨 positivo
end else begin
    resultado 🡨 negativo
end
```

### Bloques

Los bloques se definen con `begin` y `end`:

```
block: "begin" statement* "end"
```

Pueden contener cero o más sentencias.

---

## Expresiones

### Expresiones Lógicas

Las condiciones lógicas soportan operadores `and`, `or`, y `not`:

```
condition: or_expr

or_expr: and_expr
       | or_expr "or" and_expr

and_expr: not_expr
        | and_expr "and" not_expr

not_expr: comparison
         | "not" not_expr

comparison: expr (REL_OP expr)?
```

**Operadores de Comparación:**
```
REL_OP: "<" | ">" | "<=" | ">=" | "=" | "≠"
```

**Ejemplos:**
```
x > 5
x <= 10
x = y
x ≠ 0
(x > 5) and (x < 10)
(x < 0) or (x > 100)
not (x = 0)
```

### Expresiones Matemáticas

Las expresiones matemáticas siguen la precedencia estándar:

```
expr: term
    | expr ADD_OP term

term: factor
    | term MUL_OP factor

factor: NUMBER
      | variable
      | "(" expr ")"
```

Los operadores están definidos como tokens:

```
ADD_OP: "+" | "-"
MUL_OP: "*" | "/" | "mod" | "div"
```

**Operadores:**
- Suma: `+`
- Resta: `-`
- Multiplicación: `*`
- División: `/`
- Módulo: `mod`
- División entera: `div`

**Ejemplos:**
```
5
x
x + 5
x * y + z
(x + y) * z
x mod 2
x div 3
```

---

## Programación Orientada a Objetos

### Declaración de Clases

Sintaxis:
```
class_decl: NAME "{" class_attr* "}"
class_attr: NAME
```

**Ejemplo:**
```
Casa {area color propietario}
Persona {nombre edad direccion}
```

### Declaración de Objetos

Sintaxis:
```
object_decl: NAME NAME
```

El primer `NAME` es el tipo (clase) y el segundo es el nombre del objeto.

**Ejemplo:**
```
Casa miCasa
Persona juan
```

**Uso:**
```
miCasa.area 🡨 100
miCasa.color 🡨 "azul"
```

---

## Subrutinas

### Declaración de Subrutinas

Sintaxis:
```
subroutine_decl: NAME "(" param_list? ")" block

param_list: param ("," param)*

param: NAME
     | NAME array_dims
     | NAME NAME      // Clase objeto

array_dims: ("[" expr? "]")+
```

**Ejemplos:**
```
calcularSuma(a, b) begin
    resultado 🡨 a + b
end

procesarArreglo(arr[]) begin
    // procesar arreglo
end

manejarObjeto(p Persona) begin
    // usar objeto p
end
```

### Llamadas a Subrutinas

Sintaxis:
```
call: "CALL" NAME "(" arg_list? ")"

arg_list: expr ("," expr)*
```

**Ejemplos:**
```
CALL calcularSuma(5, 10)
CALL procesarArreglo(vector)
CALL imprimirResultado(x, y, z)
```

---

## Tokens y Reglas Especiales

### Tokens Básicos

#### NAME (Identificadores)

```
NAME: /[A-Za-z][A-Za-z0-9_]*/
```

- Debe comenzar con una letra
- Puede contener letras, dígitos y guiones bajos
- Ejemplos: `x`, `contador`, `mi_variable`, `Clase1`

#### NUMBER (Números)

```
NUMBER: /\d+/
```

- Solo enteros positivos
- Ejemplos: `0`, `5`, `100`, `12345`

#### COMMENT (Comentarios)

```
COMMENT: "►" /[^\n]*/
```

- Los comentarios comienzan con `►`
- Todo hasta el final de la línea se ignora
- Los comentarios se ignoran mediante `%ignore COMMENT`
- Ejemplo: `► Este es un comentario`

### Reglas de Espaciado

```
%import common.WS
%ignore WS
%ignore COMMENT
```

- Los espacios en blanco se ignoran automáticamente
- Los comentarios también se ignoran
- Importado de la biblioteca común de Lark

---

## Ejemplos Completos

### Ejemplo 1: Programa Simple

```
x 🡨 0
for i 🡨 1 to 10 do begin
    x 🡨 x + i
end
► Fin del programa
```

### Ejemplo 2: Con Condicionales

```
x 🡨 5
if (x > 0) then begin
    resultado 🡨 positivo
end else begin
    resultado 🡨 negativo
end
```

### Ejemplo 3: Con Objetos

```
Casa {area color}
Casa miCasa
miCasa.area 🡨 100
miCasa.color 🡨 "azul"
```

### Ejemplo 4: Con Subrutinas

```
sumar(a, b) begin
    resultado 🡨 a + b
end

x 🡨 5
y 🡨 10
CALL sumar(x, y)
```

---

## Notas Importantes

1. **Símbolo de Asignación**: El símbolo `🡨` se usa tanto para asignaciones como para el ciclo FOR. Si tu editor no lo soporta, considera usar una alternativa como `<-` o `:=`.

3. **Símbolo de Desigualdad**: El símbolo `≠` puede requerir codificación UTF-8 adecuada.

4. **Comentarios**: Los comentarios usan el símbolo `►` y se ignoran completamente durante el análisis.

5. **Precedencia de Operadores**: Las expresiones matemáticas respetan la precedencia estándar (multiplicación/división antes que suma/resta).

6. **Bloques Vacíos**: Los bloques `begin end` pueden estar vacíos (sin sentencias).

---

## Referencias

- [Documentación de Lark](https://lark-parser.readthedocs.io/)
- Archivo fuente: `syntax/grammar.lark`

