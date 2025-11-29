"""
Test para verificar el análisis de complejidad de una búsqueda compleja en matriz
con bucles FOR anidados y salida temprana.

Pseudocódigo evaluado:
busquedaCompleja(matriz, n, objetivo) begin encontrado 🡨 F for i 🡨 1 to n do begin for j 🡨 1 to n do begin if (matriz[i][j] = objetivo) then begin encontrado 🡨 T return i end if (matriz[i][j] > objetivo * 2) then begin break end end if (encontrado = T) then begin break end end if (encontrado = F) then begin return 0 end end
"""

from services.analysis_service import analyze_pseudocode


def test_busqueda_compleja_matriz():
    """
    PRUEBA: Búsqueda compleja en matriz con bucles FOR anidados y salida temprana
    
    Verifica que una búsqueda en matriz con bucles anidados y condiciones de salida
    temprana genere la complejidad O(n^2), Ω(1) y Theta N/A.
    """
    # Pseudocódigo a evaluar
    pseudocode = "busquedaCompleja(matriz, n, objetivo) begin encontrado 🡨 F for i 🡨 1 to n do begin for j 🡨 1 to n do begin if (matriz[i][j] = objetivo) then begin encontrado 🡨 T return i end if (matriz[i][j] > objetivo * 2) then begin break end end if (encontrado = T) then begin break end end if (encontrado = F) then begin return 0 end end"
    
    # Ejecutar el análisis
    result = analyze_pseudocode(pseudocode)
    
    # Resultado esperado
    expected_result = {
        "O": "O(n^2)",
        "Omega": "Ω(1)",
        "Theta": "N/A",
        "details": {
            "loops": [
                "Ciclo FOR con salida temprana → Ω(1), O(n)",
                "Ciclo FOR con salida temprana → Ω(1), O(n)"
            ],
            "recursion": None,
            "combination": "Suma de complejidades secuenciales",
            "early_exit_detected": True
        }
    }
    
    # Verificar que no haya errores
    assert "error" not in result, f"Error en el análisis: {result.get('error', 'Desconocido')}"
    
    # Verificar la estructura del resultado
    assert "O" in result, "El resultado debe contener 'O'"
    assert "Omega" in result, "El resultado debe contener 'Omega'"
    assert "Theta" in result, "El resultado debe contener 'Theta'"
    assert "details" in result, "El resultado debe contener 'details'"
    
    # Verificar los valores de complejidad
    assert result["O"] == expected_result["O"], f"O esperado: {expected_result['O']}, obtenido: {result['O']}"
    assert result["Omega"] == expected_result["Omega"], f"Omega esperado: {expected_result['Omega']}, obtenido: {result['Omega']}"
    assert result["Theta"] == expected_result["Theta"], f"Theta esperado: {expected_result['Theta']}, obtenido: {result['Theta']}"
    
    # Verificar los detalles
    assert "loops" in result["details"], "El resultado debe contener 'loops' en details"
    assert result["details"]["loops"] == expected_result["details"]["loops"], \
        f"Loops esperado: {expected_result['details']['loops']}, obtenido: {result['details']['loops']}"
    
    assert result["details"]["recursion"] == expected_result["details"]["recursion"], \
        f"Recursion esperado: {expected_result['details']['recursion']}, obtenido: {result['details']['recursion']}"
    
    assert result["details"]["combination"] == expected_result["details"]["combination"], \
        f"Combination esperado: {expected_result['details']['combination']}, obtenido: {result['details']['combination']}"
    
    assert result["details"]["early_exit_detected"] == expected_result["details"]["early_exit_detected"], \
        f"Early exit detected esperado: {expected_result['details']['early_exit_detected']}, obtenido: {result['details']['early_exit_detected']}"
    
    # Verificación final: comparar el resultado completo
    assert result == expected_result, f"Resultado completo no coincide.\nEsperado: {expected_result}\nObtenido: {result}"

