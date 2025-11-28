# complexity.py
# ----------------------------------------------------------
# Motor principal para calcular la complejidad computacional
# del pseudocódigo interpretado por parser/parser.py
# ----------------------------------------------------------

from math import log2

# ----------------------------------------------------------
# Utilidades básicas
# ----------------------------------------------------------

def BigO(expr_list):
    """Combina múltiples complejidades y retorna la dominante."""
    if not expr_list:
        return "1"

    order = ["1", "log n", "n", "n log n", "n^2", "n^3", "2^n"]
    scored = [(order.index(e) if e in order else len(order), e) for e in expr_list]
    return max(scored)[1]


def combine_multiplicative(a, b):
    """Reglas simples de multiplicación de complejidad."""
    if a == "1": return b
    if b == "1": return a
    if a == "n" and b == "log n": return "n log n"
    if a == "log n" and b == "n": return "n log n"
    if a == "n" and b == "n": return "n^2"
    return f"{a} * {b}"


def combine_additive(a, b):
    """Reglas simples de suma de complejidad."""
    return BigO([a, b])


# ----------------------------------------------------------
# Análisis principal
# ----------------------------------------------------------

class ComplexityAnalyzer:
    def __init__(self):
        self.details = {
            "loops": [],
            "recursion": None,
            "combination": ""
        }

    # ------------------------------------------------------
    # Entrada principal
    # ------------------------------------------------------

    def analyze(self, ast):
        """Punto de entrada: recibe el árbol completo."""
        complexity = self._analyze_node(ast)

        O = f"O({complexity})"
        Omega = f"Ω({complexity})"
        Theta = f"Θ({complexity})"

        return {
            "O": O,
            "Omega": Omega,
            "Theta": Theta,
            "details": self.details
        }

    # ------------------------------------------------------
    # Evaluación recursiva del árbol
    # ------------------------------------------------------

    def _analyze_node(self, node):
        """Evalúa nodos del AST generados por Lark (ahora como diccionarios)."""
        
        # Ahora trabajamos con diccionarios, no con nodos de Lark
        if not isinstance(node, dict):
            return "1"
        
        nodetype = node.get("type")

        if nodetype == "program":
            return self._sequence(node.get("body", []))

        if nodetype == "block":
            return self._sequence(node.get("body", []))

        if nodetype == "for":  # ← CAMBIO: "for" en lugar de "for_loop"
            return self._for_loop(node)

        if nodetype == "while":  # ← CAMBIO: "while" en lugar de "while_loop"
            return self._while_loop(node)

        if nodetype == "repeat":  # ← CAMBIO: "repeat" en lugar de "repeat_loop"
            return self._repeat_loop(node)

        if nodetype == "if":  # ← CAMBIO: "if" en lugar de "if_statement"
            return self._if_statement(node)

        if nodetype == "subroutine_decl":
            return self._subroutine(node)

        # Otros nodos → complejidad constante
        return "1"

    # ------------------------------------------------------
    # Secuencia de sentencias
    # ------------------------------------------------------

    def _sequence(self, elements):
        total = "1"
        for el in elements:
            c = self._analyze_node(el)
            total = combine_additive(total, c)
        self.details["combination"] = "Suma de complejidades secuenciales"
        return total

    # ------------------------------------------------------
    # CICLOS
    # ------------------------------------------------------

    def _for_loop(self, node):
        # node es ahora un diccionario: {"type": "for", "var": ..., "start": ..., "end": ..., "body": ...}
        body = node.get("body")
        body_c = self._analyze_node(body)
        iter_c = "n"

        self.details["loops"].append("Ciclo FOR → O(n)")
        
        # Combinar la complejidad del ciclo con la del cuerpo
        return combine_multiplicative(iter_c, body_c)

    def _while_loop(self, node):
        body = node.get("body")

        # Por defecto asumimos O(n)
        iter_c = "n"
        body_c = self._analyze_node(body)

        self.details["loops"].append("Ciclo WHILE → O(n)")
        return combine_multiplicative(iter_c, body_c)

    def _repeat_loop(self, node):
        body = node.get("body")
        body_c = self._analyze_node(body)

        self.details["loops"].append("Ciclo REPEAT → O(n)")
        return combine_multiplicative("n", body_c)

    # ------------------------------------------------------
    # IF
    # ------------------------------------------------------

    def _if_statement(self, node):
        # node: {"type": "if", "condition": ..., "then": ..., "else": ...}
        blocks = []
        if node.get("then"):
            blocks.append(node["then"])
        if node.get("else"):
            blocks.append(node["else"])
        
        comps = [self._analyze_node(b) for b in blocks]
        return BigO(comps)

    # ------------------------------------------------------
    # SUBRUTINAS (posible recursión)
    # ------------------------------------------------------

    def _subroutine(self, node):
        block = node.get("body")
        # Detectar recursión (simple heurística)
        recursive = self._detect_recursion(node)

        body_c = self._analyze_node(block)

        if recursive == "simple":
            self.details["recursion"] = "T(n) = T(n-1) + cost"
            return "n"

        if recursive == "divide":
            self.details["recursion"] = "T(n) = 2T(n/2) + cost"
            return "n log n"

        return body_c

    # ------------------------------------------------------
    # Heurísticas básicas para detectar recursión
    # ------------------------------------------------------

    def _detect_recursion(self, node):
        """Revisa si dentro del bloque se llama a sí misma la función."""
        name = node.get("name")
        block = node.get("body")

        def search(n):
            if isinstance(n, dict):
                if n.get("type") == "call" and n.get("name") == name:
                    return True
                # Buscar recursivamente en todos los valores
                for value in n.values():
                    if isinstance(value, (dict, list)):
                        if search(value):
                            return True
            elif isinstance(n, list):
                for item in n:
                    if search(item):
                        return True
            return False

        if search(block):
            # Detectar si es T(n-1) o T(n/2)
            text = str(block)

            if "/2" in text or "div 2" in text:
                return "divide"

            return "simple"

        return None