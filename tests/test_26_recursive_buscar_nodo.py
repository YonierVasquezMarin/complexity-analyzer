"""
Test para verificar el análisis de complejidad de una función recursiva
que busca y suma valores en una lista enlazada.

Pseudocódigo evaluado:
buscarNodo(nodo) begin if (nodo = NULL) then begin return 0 end valor 🡨 nodo.dato siguiente 🡨 nodo.siguiente if (siguiente = NULL) then begin return valor end return valor + CALL buscarNodo(siguiente) end
"""

from services.analysis_service import analyze_pseudocode


def test_recursive_buscar_nodo():
    """
    PRUEBA: Función recursiva buscarNodo
    
    Verifica que una función recursiva que recorre una lista enlazada
    genere la complejidad O(n), Ω(n) y Θ(n) con recursión T(n) = T(n-1) + cost.
    """
    # Pseudocódigo a evaluar
    pseudocode = "buscarNodo(nodo) begin if (nodo = NULL) then begin return 0 end valor 🡨 nodo.dato siguiente 🡨 nodo.siguiente if (siguiente = NULL) then begin return valor end return valor + CALL buscarNodo(siguiente) end"
    
    # Ejecutar el análisis
    result = analyze_pseudocode(pseudocode)
    
    # Resultado esperado
    expected_result = {
        "O": "O(n)",
        "Omega": "Ω(n)",
        "Theta": "Θ(n)",
        "details": {
            "loops": [],
            "recursion": "T(n) = T(n-1) + cost",
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

