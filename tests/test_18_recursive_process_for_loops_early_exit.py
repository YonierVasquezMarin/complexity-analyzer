"""
Test para verificar el análisis de complejidad de un proceso recursivo
combinado con bucles FOR que contienen salida temprana mediante break.

Pseudocódigo evaluado:
proceso(n) begin if (n = 1) then begin return 1 end mitad 🡨 n div 2 CALL proceso(mitad) end for i 🡨 1 to n do begin if (i mod 2 = 0) then begin for j 🡨 1 to n do begin if (arr = target) then begin break end end end else begin CALL proceso(n) end end
"""

from services.analysis_service import analyze_pseudocode


def test_recursive_process_for_loops_early_exit():
    """
    PRUEBA: Proceso recursivo con bucles FOR y salida temprana
    
    Verifica que un proceso recursivo que divide n por la mitad, combinado
    con bucles FOR que tienen salida temprana mediante break, genere la
    complejidad O(n^2), Ω(n log n) y Theta N/A.
    """
    # Pseudocódigo a evaluar
    pseudocode = "proceso(n) begin if (n = 1) then begin return 1 end mitad 🡨 n div 2 CALL proceso(mitad) end for i 🡨 1 to n do begin if (i mod 2 = 0) then begin for j 🡨 1 to n do begin if (arr = target) then begin break end end end else begin CALL proceso(n) end end"
    
    # Ejecutar el análisis
    result = analyze_pseudocode(pseudocode)
    
    # Resultado esperado
    expected_result = {
        "O": "O(n^2)",
        "Omega": "Ω(log n)",
        "Theta": "N/A",
        "details": {
            "loops": [
                "Ciclo FOR con salida temprana → Ω(1), O(n)",
                "Ciclo FOR con salida temprana → Ω(1), O(n)"
            ],
            "recursion": "T(n) = T(n/2) + cost",
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

