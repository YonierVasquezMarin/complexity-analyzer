# -------------------------------------------------------------
# Servicio central que integra parser.py y complexity.py
# -------------------------------------------------------------

from syntax.parser import PseudocodeParser
from analyzer.complexity import ComplexityAnalyzer


def analyze_pseudocode(text: str):
    """
    Recibe pseudocódigo en texto plano, lo convierte a un AST,
    lo analiza y devuelve el JSON con complejidades.
    """

    # 1. Parsear texto → AST
    parser = PseudocodeParser()
    try:
        ast = parser.parse(text)
    except Exception as e:
        return {
            "error": "Error de sintaxis en el pseudocódigo.",
            "details": str(e)
        }

    # 2. Analizar complejidad
    analyzer = ComplexityAnalyzer()
    try:
        result = analyzer.analyze(ast)
    except Exception as e:
        return {
            "error": "Error al analizar complejidad.",
            "details": str(e)
        }

    return result