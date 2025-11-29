# Documentación de la Gramática

Este documento describe la gramática definida en `syntax/grammar.lark`, que define el pseudocódigo soportado por el analizador de complejidad.

## Índice

1. [Introducción](#introducción)
2. [Estructura General](#estructura-general)
3. [Sentencias Principales](#sentencias-principales)
4. [Asignaciones y Variables](#asignaciones-y-variables)
5. [Estructuras de Control](#estructuras-de-control)
6. [Expresiones](#expresiones)
7. [Programación Orientada a Objetos](#programación-orientada-a-objetos)
8. [Grafos](#grafos)
9. [Subrutinas](#subrutinas)
10. [Tokens y Valores](#tokens-y-valores)

---

## Introducción

La gramática soporta pseudocódigo con:
- Estructuras de control (FOR, WHILE, REPEAT, IF)
- Asignaciones con símbolo especial 🡨
- Objetos, clases y grafos
- Arreglos y matrices
- Subrutinas y llamadas a funciones
- Expresiones matemáticas y lógicas
- Control de flujo (return, break, continue)

---

## Estructura General

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

Las sentencias soportadas son:

- `assignment` - Asignaciones
- `array_decl` - Declaración de arreglos locales
- `for_loop`, `while_loop`, `repeat_loop` - Ciclos
- `if_statement` - Condicionales
- `call_stmt` - Llamadas a subrutinas
- `return_stmt`, `break_stmt`, `continue_stmt` - Control de flujo
- `class_decl`, `object_decl` - Clases y objetos
- `graph_decl`, `graph_obj` - Grafos
- `subroutine_decl` - Declaración de subrutinas

---

## Asignaciones y Variables

### Asignaciones

Sintaxis: `variable 🡨 expresión`

El operador de asignación es el símbolo **🡨** (flecha hacia la izquierda).

**Ejemplos:**
```
x 🡨 10
contador 🡨 contador + 1
miObjeto.campo 🡨 valor
arreglo[5] 🡨 100
```

### Variables

Las variables pueden ser:
- Nombres simples: `x`, `contador`
- Campos de objetos: `objeto.campo`
- Elementos de arreglos: `arreglo[indice]` o `arreglo[inicio..fin]`

**Ejemplos:**
```
x                    // Variable simple
casa.area            // Campo de objeto
vector[5]            // Elemento de arreglo
matriz[1..10]        // Rango de elementos
```

### Declaración de Arreglos Locales

Sintaxis: `array nombreArray[tamaño]`

**Ejemplo:**
```
array miArreglo[10]
array matriz[5][5]
```

---

## Estructuras de Control

### Ciclo FOR

Sintaxis: `for variable 🡨 inicio to fin do bloque`

**Ejemplo:**
```
for i 🡨 1 to 10 do begin
    x 🡨 x + i
end
```

### Ciclo WHILE

Sintaxis: `while (condición) do bloque`

**Ejemplo:**
```
while (x < 100) do begin
    x 🡨 x * 2
end
```

### Ciclo REPEAT UNTIL

Sintaxis: `repeat bloque until (condición)`

**Ejemplo:**
```
repeat begin
    x 🡨 x + 1
end until (x >= 100)
```

### Sentencia IF

Sintaxis: `if (condición) then bloque [else bloque]`

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

### Control de Flujo

- `return expresión` - Retorna un valor (la expresión es opcional)
- `break` - Sale de un ciclo
- `continue` - Salta a la siguiente iteración

### Bloques

Los bloques se definen con `begin` y `end` y pueden contener cero o más sentencias.

---

## Expresiones

### Expresiones Lógicas

Soportan operadores `and`, `or`, y `not` con precedencia estándar.

**Operadores de Comparación:**
- `<`, `>`, `<=`, `>=`, `=`, `≠`

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

Siguen la precedencia estándar (multiplicación/división antes que suma/resta).

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

### Funciones Especiales

- `length(expresión)` - Longitud de un arreglo o cadena
- `ceiling(expresión)` o `┌expresión┐` - Techo (redondeo hacia arriba)
- `floor(expresión)` o `└expresión┘` - Piso (redondeo hacia abajo)

**Ejemplos:**
```
length(arreglo)
ceiling(x / 2)
┌x / 2┐
floor(x / 2)
└x / 2┘
```

---

## Programación Orientada a Objetos

### Declaración de Clases

Sintaxis: `NombreClase {atributo1 atributo2 ...}`

**Ejemplo:**
```
Casa {area color propietario}
Persona {nombre edad direccion}
```

### Declaración de Objetos

Sintaxis: `Clase nombreObjeto`

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

## Grafos

### Declaración de Grafos

Sintaxis: `Graph NombreGrafo {atributo1 atributo2 ...}`

**Ejemplo:**
```
Graph GrafoCiudad {nodos aristas}
```

### Instancias de Grafos

Sintaxis: `Graph nombreInstancia`

**Ejemplo:**
```
Graph miGrafo
```

---

## Subrutinas

### Declaración de Subrutinas

Sintaxis: `nombreSubrutina(parámetros) bloque`

Los parámetros pueden ser:
- Variables simples: `a`
- Arreglos: `arr[]` o `matriz[][]`
- Objetos: `objeto Clase`

**Ejemplos:**
```
calcularSuma(a, b) begin
    resultado 🡨 a + b
    return resultado
end

procesarArreglo(arr[]) begin
    ► procesar arreglo
end

manejarObjeto(p Persona) begin
    ► usar objeto p
end
```

### Llamadas a Subrutinas

Sintaxis: `CALL nombreSubrutina(argumentos)`

**Ejemplos:**
```
CALL calcularSuma(5, 10)
CALL procesarArreglo(vector)
CALL imprimirResultado(x, y, z)
```

---

## Tokens y Valores

### Identificadores (NAME)

Deben comenzar con una letra y pueden contener letras, dígitos y guiones bajos.

**Ejemplos:** `x`, `contador`, `mi_variable`, `Clase1`

### Números (NUMBER)

Solo enteros positivos.

**Ejemplos:** `0`, `5`, `100`, `12345`

### Cadenas (STRING)

Cadenas de texto entre comillas dobles.

**Ejemplos:** `"Hola"`, `"texto con espacios"`

### Valores Booleanos

- `T` - Verdadero
- `F` - Falso

### Valor NULL

- `NULL` - Valor nulo

### Comentarios

Los comentarios comienzan con `►` y todo hasta el final de la línea se ignora.

**Ejemplo:** `► Este es un comentario`

---

## Notas Importantes

1. **Símbolo de Asignación**: El símbolo `🡨` se usa para asignaciones y en el ciclo FOR.
2. **Símbolo de Desigualdad**: El símbolo `≠` requiere codificación UTF-8.
3. **Comentarios**: Los comentarios usan el símbolo `►` y se ignoran durante el análisis.
4. **Precedencia**: Las expresiones respetan la precedencia estándar (multiplicación/división antes que suma/resta).
5. **Bloques Vacíos**: Los bloques `begin end` pueden estar vacíos.

---

## Referencias

- [Documentación de Lark](https://lark-parser.readthedocs.io/)
- Archivo fuente: `syntax/grammar.lark`

