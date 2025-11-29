# ----------------------------------------------------------
# Motor avanzado para calcular complejidad computacional
# Detecta mejor caso (Omega), peor caso (O) y caso promedio (Theta)
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
    if a == "n^2" and b == "n": return "n^3"
    if a == "n" and b == "n^2": return "n^3"
    return f"{a} * {b}"


def combine_additive(a, b):
    """Reglas simples de suma de complejidad."""
    return BigO([a, b])


# ----------------------------------------------------------
# Clase que representa un resultado de complejidad
# ----------------------------------------------------------

class ComplexityResult:
    def __init__(self, best="1", worst="1", avg=None, has_early_exit=False):
        self.best = best  # Omega
        self.worst = worst  # O
        self.avg = avg if avg else worst  # Theta (por defecto = worst)
        self.has_early_exit = has_early_exit
    
    def __repr__(self):
        return f"ComplexityResult(best={self.best}, worst={self.worst}, avg={self.avg})"


# ----------------------------------------------------------
# Análisis principal
# ----------------------------------------------------------

class ComplexityAnalyzer:
    def __init__(self):
        self.details = {
            "loops": [],
            "recursion": None,
            "combination": "",
            "early_exit_detected": False
        }

    # ------------------------------------------------------
    # Entrada principal
    # ------------------------------------------------------

    def analyze(self, ast):
        """Punto de entrada: recibe el árbol completo."""
        result = self._analyze_node(ast)

        O = f"O({result.worst})"
        Omega = f"Ω({result.best})"
        
        # Si best == worst, entonces existe Theta
        if result.best == result.worst:
            Theta = f"Θ({result.avg})"
        else:
            Theta = "N/A"  # No hay Theta cuando los casos difieren

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
        """Evalúa nodos del AST y retorna ComplexityResult."""

        if not isinstance(node, dict):
            return ComplexityResult()

        nodetype = node.get("type")

        if nodetype == "program":
            return self._sequence(node.get("body", []))

        if nodetype == "block":
            return self._sequence(node.get("body", []))

        if nodetype == "for":
            return self._for_loop(node)

        if nodetype == "while":
            return self._while_loop(node)

        if nodetype == "repeat":
            return self._repeat_loop(node)

        if nodetype == "if":
            return self._if_statement(node)

        if nodetype == "return":
            return ComplexityResult(best="1", worst="1", has_early_exit=True)

        if nodetype == "break":
            return ComplexityResult(best="1", worst="1", has_early_exit=True)

        if nodetype == "continue":
            return ComplexityResult()

        if nodetype == "subroutine_decl":
            return self._subroutine(node)

        # Otros nodos → complejidad constante
        return ComplexityResult()

    # ------------------------------------------------------
    # Secuencia de sentencias
    # ------------------------------------------------------

    def _sequence(self, elements):
        best_total = "1"
        worst_total = "1"
        has_early_exit = False

        for el in elements:
            result = self._analyze_node(el)
            
            best_total = combine_additive(best_total, result.best)
            worst_total = combine_additive(worst_total, result.worst)
            
            if result.has_early_exit:
                has_early_exit = True

        self.details["combination"] = "Suma de complejidades secuenciales"
        return ComplexityResult(best=best_total, worst=worst_total, has_early_exit=has_early_exit)

    # ------------------------------------------------------
    # CICLOS
    # ------------------------------------------------------

    def _for_loop(self, node):
        body = node.get("body")
        body_result = self._analyze_node(body)
        
        iter_c = "n"
        
        # Si el cuerpo tiene salida temprana (return/break dentro de un if)
        if body_result.has_early_exit:
            self.details["loops"].append("Ciclo FOR con salida temprana → Ω(1), O(n)")
            self.details["early_exit_detected"] = True
            return ComplexityResult(
                best="1",  # Mejor caso: sale en primera iteración
                worst=combine_multiplicative(iter_c, body_result.worst),  # Peor caso: recorre todo
                has_early_exit=True
            )
        else:
            self.details["loops"].append("Ciclo FOR → O(n)")
            complexity = combine_multiplicative(iter_c, body_result.worst)
            return ComplexityResult(best=complexity, worst=complexity)

    def _while_loop(self, node):
        body = node.get("body")
        body_result = self._analyze_node(body)
        
        iter_c = "n"
        
        if body_result.has_early_exit:
            self.details["loops"].append("Ciclo WHILE con salida temprana → Ω(1), O(n)")
            self.details["early_exit_detected"] = True
            return ComplexityResult(
                best="1",
                worst=combine_multiplicative(iter_c, body_result.worst),
                has_early_exit=True
            )
        else:
            self.details["loops"].append("Ciclo WHILE → O(n)")
            complexity = combine_multiplicative(iter_c, body_result.worst)
            return ComplexityResult(best=complexity, worst=complexity)

    def _repeat_loop(self, node):
        body = node.get("body")
        body_result = self._analyze_node(body)

        iter_c = "n"
        
        if body_result.has_early_exit:
            self.details["loops"].append("Ciclo REPEAT con salida temprana → Ω(1), O(n)")
            self.details["early_exit_detected"] = True
            return ComplexityResult(
                best="1",
                worst=combine_multiplicative(iter_c, body_result.worst),
                has_early_exit=True
            )
        else:
            self.details["loops"].append("Ciclo REPEAT → O(n)")
            complexity = combine_multiplicative(iter_c, body_result.worst)
            return ComplexityResult(best=complexity, worst=complexity)

    # ------------------------------------------------------
    # IF
    # ------------------------------------------------------

    def _if_statement(self, node):
        then_block = node.get("then")
        else_block = node.get("else")
        
        then_result = self._analyze_node(then_block) if then_block else ComplexityResult()
        else_result = self._analyze_node(else_block) if else_block else ComplexityResult()
        
        # El mejor caso es el mínimo entre ambas ramas
        # El peor caso es el máximo entre ambas ramas
        best_case = BigO([then_result.best, else_result.best]) if else_block else then_result.best
        worst_case = BigO([then_result.worst, else_result.worst])
        
        has_early_exit = then_result.has_early_exit or else_result.has_early_exit
        
        return ComplexityResult(best=best_case, worst=worst_case, has_early_exit=has_early_exit)

    # ------------------------------------------------------
    # SUBRUTINAS (posible recursión)
    # ------------------------------------------------------

    def _subroutine(self, node):
        block = node.get("body")
        recursive = self._detect_recursion(node)

        body_result = self._analyze_node(block)

        if recursive == "simple":
            self.details["recursion"] = "T(n) = T(n-1) + cost"
            return ComplexityResult(best="n", worst="n")

        if recursive == "divide":
            self.details["recursion"] = "T(n) = 2T(n/2) + cost"
            return ComplexityResult(best="n log n", worst="n log n")

        return body_result

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
            text = str(block)

            if "/2" in text or "div 2" in text:
                return "divide"

            return "simple"

        return None