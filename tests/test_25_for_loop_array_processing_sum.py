"""
Test para verificar el análisis de complejidad de un ciclo FOR
con procesamiento de array y suma acumulativa.

Pseudocódigo evaluado:
procesarDatos(n) begin array temp[n] suma 🡨 0 for i 🡨 1 to n do begin temp[i] 🡨 i * 2 suma 🡨 suma + temp[i] end return suma end
"""

from services.analysis_service import analyze_pseudocode


def test_for_loop_array_processing_sum():
    """
    PRUEBA: Ciclo FOR con procesamiento de array y suma acumulativa
    
    Verifica que un ciclo FOR que procesa un array y acumula una suma
    genere la complejidad O(n), Ω(n) y Θ(n).
    """
    # Pseudocódigo a evaluar
    pseudocode = "procesarDatos(n) begin array temp[n] suma 🡨 0 for i 🡨 1 to n do begin temp[i] 🡨 i * 2 suma 🡨 suma + temp[i] end return suma end"
    
    # Ejecutar el análisis
    result = analyze_pseudocode(pseudocode)
    
    # Resultado esperado
    expected_result = {
        "O": "O(n)",
        "Omega": "Ω(n)",
        "Theta": "Θ(n)",
        "details": {
            "loops": [
                "Ciclo FOR → O(n)"
            ],
            "recursion": None,
            "combination": "Suma de complejidades secuenciales",
            "early_exit_detected": False
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

