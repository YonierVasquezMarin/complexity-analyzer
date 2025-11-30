# complexity.py
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
        
        # Si best == worst, entonces existe Theta (cota fuerte)
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

        if nodetype == "subroutine":
            return self._subroutine(node)
        
        if nodetype == "var":
            # Analizar si la variable tiene acceso a rangos
            return self._analyze_variable(node)
        
        if nodetype == "array_decl":
            # Declarar un arreglo de tamaño n es O(n)
            return ComplexityResult(best="n", worst="n")
        
        if nodetype == "binop":
            # Operaciones binarias - analizar si involucran strings
            return self._analyze_binop(node)
        
        if nodetype == "graph_class":
            # Definir una clase de grafo es O(1)
            return ComplexityResult()
        
        if nodetype == "graph_instance":
            # Crear instancia de grafo es O(1) (solo declaración)
            return ComplexityResult()

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
    # Análisis de operaciones binarias
    # ------------------------------------------------------
    
    def _analyze_binop(self, node):
        """
        Analiza operaciones binarias. La concatenación de strings
        puede tener complejidad O(n) dependiendo del tamaño.
        """
        op = node.get("op")
        left = node.get("left")
        right = node.get("right")
        
        # Si es concatenación de strings (+), es O(n)
        # donde n es la longitud de los strings
        if op == "+":
            # Verificar si alguno de los operandos es string
            left_is_string = isinstance(left, dict) and left.get("type") == "string"
            right_is_string = isinstance(right, dict) and right.get("type") == "string"
            
            if left_is_string or right_is_string:
                # Concatenación de strings es O(n)
                return ComplexityResult(best="n", worst="n")
        
        # Operaciones matemáticas normales son O(1)
        return ComplexityResult()

    # ------------------------------------------------------
    # Análisis de variables con rangos
    # ------------------------------------------------------
    
    def _analyze_variable(self, node):
        """
        Analiza variables. Si tienen acceso a rangos (A[1..j]),
        esto implica operación sobre múltiples elementos.
        """
        access = node.get("access")
        
        if not access:
            return ComplexityResult()
        
        # Si access es una lista, revisar cada acceso
        if isinstance(access, list):
            for acc in access:
                if isinstance(acc, dict) and acc.get("type") == "array_access":
                    index = acc.get("index")
                    if isinstance(index, dict) and index.get("type") == "range":
                        # Acceso a rango implica operación O(n) sobre el subarreglo
                        # Nota: esto es una simplificación, la complejidad real
                        # depende de lo que se haga con el rango
                        return ComplexityResult(best="n", worst="n")
        
        # Acceso simple a elemento
        return ComplexityResult()

    # ------------------------------------------------------
    # SUBRUTINAS (posible recursión)
    # ------------------------------------------------------

    def _subroutine(self, node):
        block = node.get("body")
        name = node.get("name")
        
        # Detectar recursión
        recursive_type = self._detect_recursion(node)
        
        # Detectar si hay salida temprana (return antes de recursión)
        has_early_return = self._has_early_return_before_recursion(block, name)

        body_result = self._analyze_node(block)

        if recursive_type == "simple":
            self.details["recursion"] = "T(n) = T(n-1) + cost"
            if has_early_return:
                return ComplexityResult(best="1", worst="n")
            return ComplexityResult(best="n", worst="n")

        if recursive_type == "divide":
            # Contar cuántas llamadas recursivas hay realmente
            num_calls = self._count_recursive_calls(block, name)
            
            if num_calls == 1:
                # Una sola llamada con división: T(n) = T(n/2) + cost → O(log n)
                self.details["recursion"] = "T(n) = T(n/2) + cost"
                return ComplexityResult(best="log n", worst="log n")
            else:
                # Múltiples llamadas con división: T(n) = 2T(n/2) + cost → O(n log n)
                self.details["recursion"] = "T(n) = 2T(n/2) + cost"
                return ComplexityResult(best="n log n", worst="n log n")
        
        if recursive_type == "exponential":
            # La recursión ya fue registrada en _detect_recursion con el número exacto de llamadas
            return ComplexityResult(best="2^n", worst="2^n")

        return body_result

    # ------------------------------------------------------
    # Detectar salida temprana en recursión
    # ------------------------------------------------------
    
    def _has_early_return_before_recursion(self, block, function_name):
        """
        Detecta VERDADERAS salidas tempranas (opcionales), no casos base (obligatorios).
        
        Diferencia clave:
        - CASO BASE: if (condición_base) return → luego SIEMPRE hay recursión
          Ejemplo: if (n=1) return 1; CALL func(n-1)  ← Solo un camino ejecuta recursión
        
        - SALIDA TEMPRANA: if (encontrado) return → recursión en AMBOS caminos
          Ejemplo: if (arr[i]=x) return i; CALL func(...)  ← Puede evitar recursión
        """
        if not isinstance(block, dict):
            return False
        
        # Buscar patrón: if sin else con return, seguido de recursión fuera del if
        def analyze_block_structure(node):
            if not isinstance(node, dict):
                return False
            
            if node.get("type") == "block":
                body = node.get("body", [])
                
                # Buscar patrón secuencial: IF con return + llamada recursiva después
                has_if_return_without_else = False
                has_recursion_after = False
                
                for i, item in enumerate(body):
                    if isinstance(item, dict):
                        # Es un IF sin ELSE con return?
                        if item.get("type") == "if" and not item.get("else"):
                            then_block = item.get("then")
                            if then_block and self._contains_return(then_block):
                                has_if_return_without_else = True
                                
                                # Hay recursión DESPUÉS de este IF?
                                for j in range(i + 1, len(body)):
                                    if self._contains_call_to(body[j], function_name):
                                        has_recursion_after = True
                                        break
                
                # Si hay IF-return seguido de recursión, es CASO BASE (no salida temprana)
                if has_if_return_without_else and has_recursion_after:
                    return False  # NO es salida temprana
                
                # Si hay IF-return pero NO hay recursión después, ES salida temprana
                if has_if_return_without_else and not has_recursion_after:
                    return True  # SÍ es salida temprana
                
                # Buscar recursivamente en sub-bloques
                for item in body:
                    if analyze_block_structure(item):
                        return True
            
            return False
        
        return analyze_block_structure(block)
    
    def _contains_return(self, node):
        """Verifica si un nodo contiene return"""
        if isinstance(node, dict):
            if node.get("type") == "return":
                return True
            for value in node.values():
                if isinstance(value, (dict, list)) and self._contains_return(value):
                    return True
        elif isinstance(node, list):
            for item in node:
                if self._contains_return(item):
                    return True
        return False
    
    def _contains_call_to(self, node, function_name):
        """Verifica si un nodo contiene llamada a una función específica"""
        if isinstance(node, dict):
            if node.get("type") == "call" and node.get("name") == function_name:
                return True
            for value in node.values():
                if isinstance(value, (dict, list)) and self._contains_call_to(value, function_name):
                    return True
        elif isinstance(node, list):
            for item in node:
                if self._contains_call_to(item, function_name):
                    return True
        return False
    
    def _count_recursive_calls(self, block, function_name):
        """Cuenta el número total de llamadas recursivas en el bloque"""
        count = 0
        
        def count_calls(node):
            nonlocal count
            if isinstance(node, dict):
                if node.get("type") == "call" and node.get("name") == function_name:
                    count += 1
                for value in node.values():
                    if isinstance(value, (dict, list)):
                        count_calls(value)
            elif isinstance(node, list):
                for item in node:
                    count_calls(item)
        
        count_calls(block)
        return count

    # ------------------------------------------------------
    # Heurísticas básicas para detectar recursión
    # ------------------------------------------------------

    def _detect_recursion(self, node):
        """Revisa si dentro del bloque se llama a sí misma la función."""
        name = node.get("name")
        block = node.get("body")

        if not name or not block:
            return None

        # Contar llamadas recursivas Y detectar si están en ramas mutuamente excluyentes
        recursive_calls = []
        mutually_exclusive = False

        def search(n, path="", in_if_branch=False):
            nonlocal mutually_exclusive
            
            if isinstance(n, dict):
                # Detectar si estamos en un IF-ELSE con llamadas recursivas en ambas ramas
                if n.get("type") == "if":
                    then_block = n.get("then")
                    else_block = n.get("else")
                    
                    # Buscar llamadas en cada rama
                    then_calls = []
                    else_calls = []
                    
                    def count_calls(block, calls_list):
                        if isinstance(block, dict):
                            if block.get("type") == "call" and block.get("name") == name:
                                calls_list.append(True)
                            for value in block.values():
                                if isinstance(value, (dict, list)):
                                    count_calls(value, calls_list)
                        elif isinstance(block, list):
                            for item in block:
                                count_calls(item, calls_list)
                    
                    if then_block:
                        count_calls(then_block, then_calls)
                    if else_block:
                        count_calls(else_block, else_calls)
                    
                    # Si ambas ramas tienen llamadas recursivas, son mutuamente excluyentes
                    if then_calls and else_calls:
                        mutually_exclusive = True
                
                # Verificar si es una llamada con el mismo nombre
                if n.get("type") == "call":
                    call_name = n.get("name")
                    if call_name == name:
                        recursive_calls.append(path)
                        return True
                
                # Buscar recursivamente en todos los valores
                for key, value in n.items():
                    if key != "name":
                        if isinstance(value, (dict, list)):
                            search(value, path + f"/{key}")
            elif isinstance(n, list):
                for i, item in enumerate(n):
                    search(item, path + f"[{i}]")
            return False

        search(block)

        if len(recursive_calls) == 0:
            return None
        
        # Detectar tipo de recursión
        text = str(block).lower().replace(" ", "")
        
        # Buscar patrones de división por 2
        division_patterns = [
            "div2", "/2",
            "'op':'div','right':{'type':'number','value':'2'}",
            "'op':'/','right':{'type':'number','value':'2'}"
        ]
        
        has_division = any(pattern.replace(" ", "") in text for pattern in division_patterns)
        
        # Si hay múltiples llamadas pero son mutuamente excluyentes (if-else)
        # Y además divide el problema, es divide y conquista
        if len(recursive_calls) >= 2 and mutually_exclusive and has_division:
            self.details["recursion"] = "T(n) = T(n/2) + cost (búsqueda binaria)"
            return "divide"
        
        # Recursión múltiple NO excluyente (ambas se ejecutan) = Exponencial
        if len(recursive_calls) >= 2 and not mutually_exclusive:
            self.details["recursion"] = f"T(n) = {len(recursive_calls)}T(n-1) + cost (exponencial)"
            return "exponential"
        
        # Recursión con división = Divide y conquista
        if has_division:
            return "divide"

        # Recursión simple = Lineal
        return "simple"