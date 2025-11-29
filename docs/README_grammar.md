# Documentación de la Gramática

Este documento describe la gramática definida en `syntax/grammar.lark`, que define el pseudocódigo soportado por el analizador.

## Introducción

La gramática soporta pseudocódigo con estructuras de control, asignaciones, objetos, arreglos, subrutinas y expresiones matemáticas y lógicas.

## Estructuras Principales

### Asignaciones

Sintaxis: `variable 🡨 expresión`

El operador de asignación es el símbolo **🡨** (flecha hacia la izquierda).

**Ejemplos:**
```
x 🡨 10
contador 🡨 contador + 1
arreglo[5] 🡨 100
```

### Variables

- Variables simples: `x`, `contador`
- Campos de objetos: `objeto.campo`
- Elementos de arreglos: `arreglo[indice]` o `arreglo[inicio..fin]`

### Declaración de Arreglos

Sintaxis: `array nombreArray[tamaño]`

**Ejemplo:**
```
array miArreglo[10]
array matriz[5][5]
```

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

**Ejemplo:**
```
if (x > 0) then begin
    resultado 🡨 positivo
end else begin
    resultado 🡨 negativo
end
```

### Control de Flujo

- `return expresión` - Retorna un valor
- `break` - Sale de un ciclo
- `continue` - Salta a la siguiente iteración

## Expresiones

### Operadores de Comparación

`<`, `>`, `<=`, `>=`, `=`, `≠`

### Operadores Lógicos

`and`, `or`, `not`

### Operadores Matemáticos

- Suma: `+`
- Resta: `-`
- Multiplicación: `*`
- División: `/`
- Módulo: `mod`
- División entera: `div`

### Funciones Especiales

- `length(expresión)` - Longitud de un arreglo o cadena
- `ceiling(expresión)` o `┌expresión┐` - Techo
- `floor(expresión)` o `└expresión┘` - Piso

## Programación Orientada a Objetos

### Declaración de Clases

Sintaxis: `NombreClase {atributo1 atributo2 ...}`

**Ejemplo:**
```
Casa {area color propietario}
```

### Declaración de Objetos

Sintaxis: `Clase nombreObjeto`

**Ejemplo:**
```
Casa miCasa
miCasa.area 🡨 100
```

## Grafos

### Declaración de Grafos

Sintaxis: `Graph NombreGrafo {atributo1 atributo2 ...}`

**Ejemplo:**
```
Graph GrafoCiudad {nodos aristas}
Graph miGrafo
```

## Subrutinas

### Declaración de Subrutinas

Sintaxis: `nombreSubrutina(parámetros) bloque`

**Ejemplo:**
```
calcularSuma(a, b) begin
    resultado 🡨 a + b
    return resultado
end
```

### Llamadas a Subrutinas

Sintaxis: `CALL nombreSubrutina(argumentos)`

**Ejemplo:**
```
CALL calcularSuma(5, 10)
```

## Tokens y Valores

- **Identificadores**: Letras, dígitos y guiones bajos (ej: `x`, `contador`, `mi_variable`)
- **Números**: Enteros positivos (ej: `0`, `5`, `100`)
- **Cadenas**: Texto entre comillas dobles (ej: `"Hola"`)
- **Booleanos**: `T` (verdadero), `F` (falso)
- **NULL**: Valor nulo
- **Comentarios**: Comienzan con `►` y todo hasta el final de la línea se ignora

## Notas Importantes

1. **Símbolo de Asignación**: Se usa `🡨` para asignaciones y en el ciclo FOR.
2. **Bloques**: Se definen con `begin` y `end` y pueden contener cero o más sentencias.
3. **Precedencia**: Las expresiones respetan la precedencia estándar (multiplicación/división antes que suma/resta).

## Referencias

- Archivo fuente: `syntax/grammar.lark`
- [Documentación de Lark](https://lark-parser.readthedocs.io/)
